
from flask import Blueprint
from flask import request
from flask import session
from flask import render_template
from flask import redirect
from flask import url_for

from jinja2 import TemplateNotFound

from app import config
from app import language
from app.apis.coupons.services import CouponsServices

# Define the blueprint: 'auth', set its url prefix: app.url/auth
coupons = Blueprint('coupons', __name__, url_prefix='/coupons', template_folder='templates')
cookie_jar = config.COOKIE_VALUE

# Set language variable
lang = {}
lang = getattr(language, config.DEFAULT_LANG)

# Set the route and accepted methods


@coupons.route('/', methods=['GET', 'POST'])
def coupons_page():
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

        cps = CouponsServices(session_details)
        getUploads = cps.getUploads()

        if request.method == 'POST':
            print("In POST")

        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])

        return render_template("coupons/coupons.html", lang=user_lang, main_menu="Coupons",
                               menu_item="Coupons", userdata=session_details, uploads=getUploads)

    except TemplateNotFound as e:
        raise e


@coupons.route('/generate-coupons', methods=['GET', 'POST'])
def add_coupons_page():
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

        cps = CouponsServices(session_details)

        if request.method == 'POST':
            print("In POST")

            csv_file = request.files['csv_file']
            print(csv_file)

            generated_coupons = cps.generate_coupons(session_details, csv_file)
            return generated_coupons

    except TemplateNotFound as e:
        print(e)
        raise e


@coupons.route('/details/<upload_id>', methods=['GET', 'POST'])
def get_coupons(upload_id):
    try:
        print("In Get Coupons Page.")
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

        cps = CouponsServices(session_details)
        getCoupons = cps.get_upload_coupons(upload_id)

        if request.method == 'POST':
            print("In POST")

        return render_template("coupons/coupons-details.html", userdata=session_details,
                               main_menu="Coupons", sub_menu="Coupons Details", coupons=getCoupons)

    except TemplateNotFound as e:
        print(e)
        raise e