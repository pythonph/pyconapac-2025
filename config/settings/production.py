import environ
import os

from .base import *


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# False if not in os.environ because of casting above
DEBUG = env("DEBUG")

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = [
    "ph.pycon.org",
    "pycon-2024.python.ph",
    "pycon.python.ph",
    "localhost",
    "pycon-apac.python.ph",
]
CSRF_TRUSTED_ORIGINS = [
    "https://pycon-2024.python.ph",
    "https://pycon.python.ph",
    "https://pycon-apac.python.ph"
]

# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ
SECRET_KEY = env("SECRET_KEY")

# Parse database connection url strings
# like psql://user:pass@127.0.0.1:8458/db
DATABASES = {
    # read os.environ['DATABASE_URL'] and raises
    # ImproperlyConfigured exception if not found
    #
    # The db() method is an alias for db_url().
    "default": env.db(),
    # read os.environ['SQLITE_URL']
    "extra": env.db_url("SQLITE_URL", default="sqlite:////tmp/my-tmp-sqlite.db"),
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}

