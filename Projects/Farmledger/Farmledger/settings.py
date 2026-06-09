"""
Django settings for Farmledger project.

Configuration focuses on production-ready defaults while keeping
development convenience via environment variables.
"""

from pathlib import Path
import os
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'change-me-in-production')
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',

    # Local apps
    'apps.accounts',
    'apps.farms',
    'apps.crops',
    'apps.expenses',
    'apps.harvests',
    'apps.weather',
    'apps.analytics',
    'apps.notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Farmledger.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Farmledger.wsgi.application'


# Database (Postgres by default)
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('POSTGRES_DB', 'farmledger'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}


# Auth
AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/min',
        'user': '100/min',
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
}

# If drf-spectacular is available, configure DRF to use its AutoSchema
try:
    import drf_spectacular  # type: ignore
    REST_FRAMEWORK['DEFAULT_SCHEMA_CLASS'] = 'drf_spectacular.openapi.AutoSchema'
except (ImportError, ModuleNotFoundError):
    # drf-spectacular is optional in some environments (CI/local). Catch import errors explicitly.
    pass

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.environ.get('JWT_ACCESS_MINUTES', '15'))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.environ.get('JWT_REFRESH_DAYS', '7'))),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.environ.get('DJANGO_TIME_ZONE', 'UTC')
USE_I18N = True
USE_TZ = True


# Static and media
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# CORS
CORS_ALLOW_ALL_ORIGINS = os.environ.get('CORS_ALLOW_ALL', 'True') == 'True'


# Celery / Redis
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/1')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# drf-spectacular OpenAPI settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'FarmLedger API',
    'DESCRIPTION': 'API documentation for FarmLedger (Agritech SaaS)',
    'VERSION': '1.0.0',
}

# Security hardening defaults (environment-controlled)
# In production set DJANGO_DEBUG=False and adjust the following env vars.
SECURE_SSL_REDIRECT = os.environ.get('DJANGO_SECURE_SSL_REDIRECT', 'False') == 'True'
SESSION_COOKIE_SECURE = os.environ.get('DJANGO_SESSION_COOKIE_SECURE', 'True') == 'True'
CSRF_COOKIE_SECURE = os.environ.get('DJANGO_CSRF_COOKIE_SECURE', 'True') == 'True'

# HTTP Strict Transport Security
SECURE_HSTS_SECONDS = int(os.environ.get('DJANGO_SECURE_HSTS_SECONDS', '31536000')) if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True') == 'True'
SECURE_HSTS_PRELOAD = os.environ.get('DJANGO_SECURE_HSTS_PRELOAD', 'True') == 'True'

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = os.environ.get('DJANGO_X_FRAME_OPTIONS', 'DENY')

# Referrer policy
REFERRER_POLICY = os.environ.get('DJANGO_REFERRER_POLICY', 'no-referrer-when-downgrade')

# Recommended secure password hashers (leave as default unless argon2 is installed)
# PASSWORD_HASHERS = [
#     'django.contrib.auth.hashers.Argon2PasswordHasher',
#     'django.contrib.auth.hashers.PBKDF2PasswordHasher',
#     'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
#     'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
# ]

# Default from email
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'no-reply@localhost')

# Content Security Policy (django-csp)
# Adjust sources as necessary for external CDNs and inline usage.
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", 'https:',)
CSP_SCRIPT_SRC = ("'self'", 'https:',)
CSP_IMG_SRC = ("'self'", 'data:', 'https:')
CSP_FONT_SRC = ("'self'", 'https:')
CSP_CONNECT_SRC = ("'self'", 'https:')
CSP_FRAME_ANCESTORS = ("'none'",)
CSP_REPORT_URI = os.environ.get('CSP_REPORT_URI', '')



# Only enable drf_spectacular when it's importable in the environment
try:
    import drf_spectacular  # type: ignore
    INSTALLED_APPS.append('drf_spectacular')
except (ImportError, ModuleNotFoundError):
    # Optional third-party; explicit import error handling to avoid broad except
    pass

