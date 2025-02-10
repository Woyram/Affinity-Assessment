
from flask import Blueprint
from flask import request
from flask import session
from flask import render_template
from flask import redirect
from flask import url_for

from jinja2 import TemplateNotFound

from app import config
from app import language
from app.apis.customers.services import customerServices

# Define the blueprint: 'auth', set its url prefix: app.url/auth
customers = Blueprint('customers', __name__, url_prefix='/customers', template_folder='templates')
cookie_jar = config.COOKIE_VALUE

# Set language variable
lang = {}
lang = getattr(language, config.DEFAULT_LANG)

# Set the route and accepted methods


@customers.route('/', methods=['GET', 'POST'])
def customers_page():
    try:
        print("In Coupons Page.")
        try:
            cookie_id = request.cookies.get('{0}'.format(cookie_jar))
        except Exception as e:
            cookie_id = None

        if cookie_id is not None:
            session_details = session.get(cookie_id)
            print("Session Data..........")
            print(session_details)
            if not session_details:
                return redirect(url_for("auth.home_page"))
        else:
            return redirect(url_for("auth.home_page"))

        cus = customerServices(session_details)
        customersResponse = cus.get_customers()

        if request.method == 'POST':
            print("In POST")

        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])

        return render_template("customers/customers.html", lang=user_lang, main_menu="Customers",
                               menu_item="Customers", userdata=session_details, customers=customersResponse)

    except TemplateNotFound as e:
        raise e
