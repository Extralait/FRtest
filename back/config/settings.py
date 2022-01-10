import logging.config
import os
from datetime import timedelta

from pathlib import Path
from envparse import env

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = os.path.join(BASE_DIR.parent, "project_config/.env.back")

if os.path.isfile(dotenv_file):
    env.read_envfile(dotenv_file)

# Базовые настройки приложения
SECRET_KEY = env.str("SECRET_KEY")

DATA_UPLOAD_MAX_NUMBER_FIELDS = env.int("DATA_UPLOAD_MAX_NUMBER_FIELDS")

SECURE_PROXY_SSL_HEADER = env.tuple("SECURE_PROXY_SSL_HEADER")

DEBUG = env.bool("DEBUG")

PRODUCTION = env.bool("PRODUCTION")

ROOT_URLCONF = "config.urls"

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Настройки языка и времени
LANGUAGE_CODE = env.str("LANGUAGE_CODE")

TIME_ZONE = env.str("TIME_ZONE")

USE_I18N = env.bool("USE_I18N")

USE_L10N = env.bool("USE_L10N")

USE_TZ = env.bool("USE_TZ")

# Базовые настройки базы данных
DB_USER = env.str("DB_USER")

DB_USER_PASSWORD = env.str("DB_USER_PASSWORD")

DB_HOST = env.str("DB_HOST")

DB_NAME = env.str("DB_NAME")

DB_PORT = env.str("DB_PORT")

CONN_MAX_AGE = env.int("CONN_MAX_AGE")

# Настройки CORS
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS")

CORS_ALLOW_CREDENTIALS = env.bool("CORS_ALLOW_CREDENTIALS")

CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST")

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

# Настройки аккаунта админитратора
ADMINS = [
    {
        "email": env.str("ADMIN_EMAIL"),
        "first_name": env.str("ADMIN_FIRST_NAME"),
        "last_name": env.str("ADMIN_LAST_NAME"),
        "password": env.str("ADMIN_PASSWORD"),
    }
]

# Установленные приложения
INSTALLED_APPS = [
    # Admin tools
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    # Defaults
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Api
    "djoser",
    "rest_framework",
    # Own apps
    "users",
    "quiz",
    # CORS
    "whitenoise.runserver_nostatic",
    "corsheaders",
]

# Промежуточные слои
MIDDLEWARE = [
    # Defaults
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

# Настройка шаблонизатора
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            'loaders': [
                # Loads templates from admin_tools setting:
                "admin_tools.template_loaders.Loader",
                # Loads templates from DIRS setting:
                "django.template.loaders.filesystem.Loader",
                # Loads templates from your installed apps:
                "django.template.loaders.app_directories.Loader",
            ],

        },
    },
]

# Настройка запуска приложения
ASGI_APPLICATION = "config.asgi.application"

# Настройка базы данных
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_USER_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
    }
}

# Настройки кэша
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'local_caching',
    },
    'snowflake': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 5 * 60,  # 5*60 = 5 minutes
    },
    'longhorn': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache',
        'TIMEOUT': 1 * 60 * 60,  # 1*60*60 = 1 hour
    },
}

# Модель пользователя
AUTH_USER_MODEL = "users.User"

# Путь к статическим файлам
STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

FIXTURE_DIRS = [
    "/fixtures/"
]

# Настройки DRF
REST_FRAMEWORK = {
    # Права доступа поумолчанию
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly",
    ],
    # Тип токенов и авторизации
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication"
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "url_filter.integrations.drf.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}

# Настройки djoser
DJOSER = {
    "SEND_ACTIVATION_EMAIL": False,
    "SEND_CONFIRMATION_EMAIL": False,
    "TOKEN_MODEL": None,
    "HIDE_USERS": False,
    "SERIALIZERS": {
        # "current_user": "users.api.serializers.CurrentUserDetailsSerializer",
    },
    "PERMISSIONS": {
        "activation": ["rest_framework.permissions.AllowAny"],
        "password_reset": ["rest_framework.permissions.AllowAny"],
        "password_reset_confirm": ["rest_framework.permissions.AllowAny"],
        "set_password": ["djoser.permissions.CurrentUserOrAdmin"],
        "username_reset": ["rest_framework.permissions.AllowAny"],
        "username_reset_confirm": ["rest_framework.permissions.AllowAny"],
        "set_username": ["djoser.permissions.CurrentUserOrAdmin"],
        "user_create": ["rest_framework.permissions.AllowAny"],
        "user_delete": ["djoser.permissions.CurrentUserOrAdmin"],
        "user": ["djoser.permissions.CurrentUserOrAdmin"],
        "user_list": ["djoser.permissions.CurrentUserOrAdmin"],
        "token_create": ["rest_framework.permissions.AllowAny"],
        "token_destroy": ["rest_framework.permissions.IsAuthenticated"],
    }
}

# Настройки JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,

    "AUTH_HEADER_TYPES": ("JWT",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(days=2),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=5),
}

# # Настройка графического вывода базы данных
# GRAPH_MODELS = {
#     "all_applications": True,
#     "group_models": True,
# }

# Настройки почты
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

EMAIL_HOST = env.str("EMAIL_HOST")

EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")

EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')

DEFAULT_FROM_EMAIL = env.str("EMAIL_HOST_USER")

EMAIL_PORT = env.str("EMAIL_PORT")

EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")

# Логгироваине
LOGGING_CONFIG = None

LOGLEVEL = env.str("DJANGO_LOGLEVEL").upper()

logging.config.dictConfig = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
                '%(asctime)s [%(levelname)s] %(ip)s %(email)s '
                '%(pathname)s:%(lineno)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', ],
            'level': LOGLEVEL,
            'propagate': True,
        },
    }
}
