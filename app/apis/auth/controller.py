# Import flask dependencies
from flask import Blueprint
from flask import request
from flask import render_template

from flask import session
from flask import redirect
from flask import url_for
from flask import jsonify
from flask import make_response
from jinja2 import TemplateNotFound

# Importing Project dependencies
from app import config
from app import language
from app.libs.decorators import AccessLogger
from app.libs.logger import Logger

# Define the account blueprint object
auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')

# Set language variable
lang = {}
lang = getattr(language, config.DEFAULT_LANG)

# Initiate logger an decorators
log = Logger()
log_access = AccessLogger()


# Set the route and accepted methods
@auth.route('/', methods=['GET', 'POST'])
@log_access.log_request
def home_page():
    try:
        print("In login page")
        # access session data (session['k']=v)
        try:
            cookie_id = request.cookies.get('{0}'.format(config.COOKIE_VALUE))  # GET previous cookies
        except Exception as e:
            cookie_id = None

        response = make_response(render_template("auth/index.html"))
        print("Medur ha")
        if cookie_id != None:
            session.pop(cookie_id, None)  # Clear existing session data
            response.set_cookie('{0}'.format(config.COOKIE_VALUE), '', expires=0)  # Expire existing cookie data
        return response
    except TemplateNotFound as e:
        print("--------------")
        print(e)
        raise e


@auth.route('forgotpassword', methods=['GET', 'POST'])
@log_access.log_request
def forgotPasswordPage():
    return render_template("auth/forgot-password.html")


@auth.route('set-password', methods=['GET', 'POST'])
@log_access.log_request
def setPasswordPage():
    return render_template("auth/confirm-password.html")


@auth.route('/logout', methods=['GET', 'POST'])
@log_access.log_request
def logout():
    print("In List of Users")
    try:
        cookie_id = request.cookies.get('{0}'.format(config.COOKIE_VALUE))
    except Exception as e:
        cookie_id = None

    print("Medur ha")
    if cookie_id != None:
        session_details = session['{0}'.format(cookie_id)]
        print("Session Data")
        print(session_details)
    else:
        return redirect(url_for("auth.home_page"))

    session.clear()
    return redirect(url_for("auth.home_page"))
