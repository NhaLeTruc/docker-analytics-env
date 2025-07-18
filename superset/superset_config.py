FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
    "ENABLE_EXPLORE_JSON_CSRF_PROTECTION": True,
    "ALERT_REPORTS": True,
}
SECRET_KEY = "this_is_a_default_secret_key"
SESSION_COOKIE_NAME = "superset_session"
WTF_CSRF_ENABLED = True
WTF_CSRF_EXEMPT_LIST = []
WTF_CSRF_TIME_LIMIT = None
ENABLE_PROXY_FIX = True

WEBDRIVER_BASEURL = "http://localhost:8088/" 

# TODO: Add master user authentication