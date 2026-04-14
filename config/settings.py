from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-g6gw7s=nab!!$22x^6w8^wavbbib)vz9%kq7sg*+5z)d$@_z*%"

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "forum",
    "datasets",
    "validation",
    "moderation",
    "dashboard",
    "exports",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files (profile images, etc.)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Custom User Model
AUTH_USER_MODEL = "accounts.User"

# Authentication Redirects
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
LOGIN_URL = "login"

# ─── Email / SMTP ───────────────────────────────────────────────────────────
# To send real password-reset emails via Gmail:
#   1. Go to your Google Account → Security → App Passwords
#   2. Generate an App Password for "Mail"
#   3. Fill in EMAIL_HOST_USER and EMAIL_HOST_PASSWORD below
#
# For local development without a Gmail account, comment out the SMTP block
# and uncomment the console backend instead — emails will print to terminal.

EMAIL_BACKEND     = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST        = 'smtp.gmail.com'
EMAIL_PORT        = 587
EMAIL_USE_TLS     = True
EMAIL_HOST_USER   = 'm.hammza.03@gmail.com'    # ← replace with your Gmail address
EMAIL_HOST_PASSWORD = 'xzgu pijf ojyd fsoe'     # ← replace with your Gmail App Password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Console fallback (uncomment to print emails to terminal instead of sending)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
