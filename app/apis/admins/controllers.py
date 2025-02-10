import json
import uuid
import datetime

from flask import Blueprint
from flask import request
from flask import session
from flask import url_for
from flask import make_response
from flask import redirect
from flask import render_template
from flask import jsonify
from jinja2 import TemplateNotFound

# Importing project dependencies
from app import config
from app import language
from app.apis.admins.services import adminServices

from app.libs.decorators import AccessLogger
from app.libs.logger import Logger

# Define the admins blueprint object
admins = Blueprint('admins', __name__, url_prefix='/admins', template_folder='templates')

# Set language variable
lang = {}
lang = getattr(language, config.DEFAULT_LANG)

# Initiate logger an decorators
log = Logger()
log_access = AccessLogger()


# set the route and accepted methods for admins


@admins.route('/login', methods=['GET', 'POST'])
@log_access.log_request
def admins_login():
    try:
        print("In Admin Login")
        session_details = {}
        try_var = None
        #
        print(session_details)
        request_data = request.form.to_dict()
        print("Request Data is: {}".format(request_data))
        print(request_data)

        print(session)

        if 'trying_{0}'.format(request_data['username']) in session:
            try_var = session['trying_{0}'.format(request_data['username'])]

        if "username" not in request_data and "password" not in request_data:
            return make_response(language.CODES['FAIL'], "00",
                                 language.en['login']['params_required'], [])

        svc = adminServices(session_details)
        result = svc.adminLogin(request_data, try_var)

        print("The result: {}".format(result))

        if result['code'] == '00':
            cookie_value = str(uuid.uuid4()).replace('-', '')[:15]  # Generate a session token value
            session['{0}'.format(cookie_value)] = dict(result['data'])
            session['trying_{0}'.format(result['username'])] = None
            # Render Response and browser cookie value
            expire_date = datetime.datetime.now()
            expire_date = expire_date + datetime.timedelta(days=1)
            # response = make_response(jsonify(**result))

            if "date_created" in result["data"] and result["data"]["date_created"] is not None:
                result["data"]["date_created"] = result["data"]["date_created"].strftime("%Y-%m-%d %H:%M:%S")
            if "last_login" in result["data"] and result["data"]["last_login"] is not None:
                result["data"]["last_login"] = result["data"]["last_login"].strftime("%Y-%m-%d %H:%M:%S")

            if "pass_date" in result["data"] and result["data"]["pass_date"] is not None:
                result["data"]["pass_date"] = result["data"]["pass_date"].strftime("%Y-%m-%d %H:%M:%S")

            print(type(result))
            print(json.dumps(result))
            response = make_response(json.dumps(result))
            response.set_cookie('{0}'.format(config.COOKIE_VALUE), cookie_value, expires=expire_date)

            # Return response for successful login
            return response
        elif result['code'] == '01' and result['data'] == 1:
            if 'trying_{0}'.format(result['username']) in session and session[
               'trying_{0}'.format(result['username'])] is not None:
                session['trying_{0}'.format(result['username'])] = session['trying_{0}'.format(result['username'])] + 1
            else:
                session['trying_{0}'.format(result['username'])] = 1
        elif result['code'] == '01' and result['data'] == 2:
            session['trying_{0}'.format(result['username'])] = None
        print("dsd-----------------")
        return jsonify(**result)
    except TemplateNotFound as e:
        print("Login Exception: {}".format(e))
        raise e
