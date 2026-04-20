"""
Django settings for waste_management project.
"""

from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def get_env_variable(var_name, default=None):
    """Get environment variable or return default."""
    try:
        return os.environ.get(var_name, default)
    except KeyError:
        if default is None:
            error_msg = f"Set the {var_name} environment variable"
            raise ImproperlyConfigured(error_msg)
        return default


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('SECRET_KEY', 'django-insecure-change-this-in-production-12345')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_env_variable('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = get_env_variable('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Allow CSRF for same-origin requests
CSRF_TRUSTED_ORIGINS = get_env_variable(
    'CSRF_TRUSTED_ORIGINS',
    'http://127.0.0.1:8000,http://localhost:8000'
).split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'contoler',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'waste_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'waste_management.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Use PostgreSQL in production if DATABASE_URL is set
if get_env_variable('DATABASE_URL'):
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = get_env_variable('TIME_ZONE', 'UTC')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# Security Settings (production / DEBUG=False)
# LAN or http://localhost deploys: leave USE_SSL unset or false so /static/ is not redirected to https://
# Real HTTPS deployment: set environment USE_SSL=true (or 1/yes)
_use_ssl = get_env_variable('USE_SSL', 'false').lower() in ('1', 'true', 'yes')

if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REDIRECT_EXEMPT = []
    X_FRAME_OPTIONS = 'DENY'
    if _use_ssl:
        SECURE_HSTS_INCLUDE_SUBDOMAINS = True
        SECURE_HSTS_SECONDS = 31536000
        SECURE_SSL_REDIRECT = True
        SESSION_COOKIE_SECURE = True
        CSRF_COOKIE_SECURE = True
    else:
        SECURE_HSTS_SECONDS = 0
        SECURE_SSL_REDIRECT = False
        SESSION_COOKIE_SECURE = False
        CSRF_COOKIE_SECURE = False

# Logging Configuration (ensure logs dir exists so FileHandler does not fail)
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': LOG_DIR / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'contoler': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}

# Session Settings
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# ---------------------------------------------------------------------------
# Email (SMTP) – waste detection alerts to authorities (all hardcoded, no .env needed)
# Run: python manage.py test_email
# ---------------------------------------------------------------------------
EMAIL_HOST_USER = 'jeethudaniel88@gmail.com'
EMAIL_HOST_PASSWORD = 'dtljlsbuohpixriz'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'jeethudaniel88@gmail.com'

# Recipient for waste detection alerts
WASTE_ALERT_EMAIL_RECIPIENTS = ['sallydaniel05@gmail.com']
