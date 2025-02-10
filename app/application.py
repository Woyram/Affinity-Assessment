"""
These file contains all the initialisations and configurations for the application
"""

# Standard Library Dependencies

import flask_excel as excel

from datetime import datetime

from flask import Flask
from flask import redirect
from flask import render_template
from flask import url_for
from app import config
from app.apis.admins.controllers import admins
from app.apis.auth.controller import auth
from app.apis.coupons.controllers import coupons
from app.apis.customers.controllers import customers
from app.apis.dashboard.controllers import dashboard

from flask_session import Session

from app.libs.decorators import AccessLogger
from app.libs.logger import Logger

log = Logger()
log_access = AccessLogger()

# Creating flask application instance
app = Flask(__name__)
excel.init_excel(app)

# Configurations
app.config['SESSION_TYPE'] = config.SESSION_TYPE
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['PROPAGATE_EXCEPTIONS'] = True
Session(app)
app.config.from_object(__name__)


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Sample HTTP error handling
@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
@log_access.log_request
def root_route():
    return redirect(url_for('auth.home_page'))

@app.template_filter('datetimeformat')
def datetimeformat(value, format="%d %B %Y %I:%M %p"):
    dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
    return dt.strftime(format)


# Registering blueprints
app.register_blueprint(auth)
app.register_blueprint(admins)
app.register_blueprint(dashboard)
app.register_blueprint(coupons)
app.register_blueprint(customers)


decor = "AFFINITY ASSESSMENT"
log.write_log(msg=decor)
