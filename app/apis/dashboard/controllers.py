from flask import Blueprint
from flask import request
from flask import session
from flask import render_template
from flask import redirect
from flask import url_for

from jinja2 import TemplateNotFound

from app import config
from app import language
from app.apis.dashboard.services import dashboardServices

# Define the blueprint: 'auth', set its url prefix: app.url/auth
dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard', template_folder='templates')
cookie_jar = config.COOKIE_VALUE

# Set language variable
lang = {}
lang = getattr(language, config.DEFAULT_LANG)

# Set the route and accepted methods


@dashboard.route('/', methods=['GET', 'POST'])
def dashboard_page():
    try:
        print("In Dashboard Page.")
        # access session data (session['k']=v)
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

        dsh = dashboardServices(session_details)
        dashboardDetails = dsh.get_dashboard_info()

        if request.method == 'POST':
            print("In POST")

        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])

        return render_template("dashboard/dashboard.html", lang=user_lang, main_menu="Dashboard",
                               menu_item="Dashboard", userdata=session_details, dashboardDetails=dashboardDetails)

    except TemplateNotFound as e:
        raise e
