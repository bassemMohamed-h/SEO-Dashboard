from .base import *

DEBUG = True

SECRET_KEY = "django-insecure-%a8+d#ff0kk*urd!)-g^j1r1yyt6w(y)pqhyenu!^8*tkc^qn5"

ALLOWED_HOSTS = ["*"]

# SQLite for local dev — no database setup needed
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

WAGTAILADMIN_BASE_URL = "http://localhost:8000"

try:
    from .local import *
except ImportError:
    pass
