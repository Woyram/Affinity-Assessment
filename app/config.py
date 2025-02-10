DEBUG = True

# Database Credentials
MYSQL_HOST = "bringme-food-do-user-16890763-0.l.db.ondigitalocean.com"
MYSQL_PORT = 25060
MYSQL_USER = 'affinity'
MYSQL_PASSWD = 'AVNS_qAwN_GbLrMLt9MTE9uv'
MYSQL_DATABASE = 'affinity'


# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2
THREAD_POOL_SIZE = 5

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True
APPLICATION_NAME = "AFFINITY ASSESSMENT"

APP_MODE = "DEV"

# Use a secure, unique and absolutely secret key for
CSRF_SESSION_KEY = "secret_key"

# SMS CONFIG
BASIC_SMS_BASE_URL = "https://3v4k8j.api.infobip.com/sms/2/text/advanced"
SMS_API_KEY = "App 3949c35622f5afd9055addcd249d21b0-c8d97cb7-b5b0-4504-b6b1-739655ee067b"

# Secret key for signing cookies
SECRET_KEY = "QELr08j/3yX Y~XHH!jmN]LWX/,?RT"

# Flask-session configs
SESSION_TYPE = 'filesystem'
COOKIE_VALUE = 'sess'

# Directories
UPLOAD_FOLDER = "/app/app/static/customerFiles/"
# UPLOAD_FOLDER = "/Users/wgbotsyo/Documents/Development/Personal/affinity/app/static/customerFiles/"

# Multi-Language Configurations
DEFAULT_LANG = "en"

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
MAX_FILE_SIZE = 2 * 1024 * 1024

# USER TYPES
ADMIN = "101"
SYSTEM = "102"
USER = "105"

# LOG PATHS
ACCESS_LOG_PATH = "log/access"
EVENT_LOG_PATH = "log/event"
ERROR_LOG_PATH = "log/error"
CS_REQ_LOG_PATH = "log/cs_requests"
AD_REQ_LOG_PATH = "log/ad_requests"
USER_ACCESS_LOG_PATH = "log/user_access"
