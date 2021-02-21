import os
import logging


def get_env_variable(var_name, default=None):
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "The environment variable {} was missing, abort...".format(
                var_name
            )
            raise EnvironmentError(error_msg)


SUPERSET_WEBSERVER_TIMEOUT = 90
MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY', '')

CACHE_DEFAULT_TIMEOUT = 60 * 60 * 24

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST = []
# A CSRF token that expires in 1 year
WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365


from flask_appbuilder.security.manager import (
    AUTH_DB,
    AUTH_LDAP,
    AUTH_OAUTH,
    #    AUTH_OID,
    #    AUTH_REMOTE_USER
)

if get_env_variable("AUTH_TYPE") == 'AUTH_LDAP':
    AUTH_TYPE = AUTH_LDAP
else:
    AUTH_TYPE = AUTH_DB

AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Gamma"

AUTH_LDAP_USE_TLS = False

# Fix for "There was an issue fetching the favorite status of this dashboard"
ENABLE_PROXY_FIX = True

ENABLE_TIME_ROTATE = True
FILENAME = os.path.join("/var/log/superset", "superset.log")