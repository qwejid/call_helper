from datetime import timedelta
import os
import environ
import sentry_sdk

root = environ.Path(__file__) - 2
env = environ.Env()

environ.Env.read_env(env.str(root(), '.env'))

BASE_DIR = root()

SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.str('ALLOWED_HOSTS', default='').split(' ')

# base
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# packages
INSTALLED_APPS += [
    'auditlog',  # Регистрация изменений в моделях
    'rest_framework',  # REST framework для создания API
    'django_filters',  # Фильтры для REST framework
    'corsheaders',  # Заголовки CORS для управления междоменными запросами
    'djoser',  # Djoser для обработки аутентификации и управления пользователями через REST API
    'phonenumber_field',  # Поле для ввода телефонных номеров
    'django_generate_series',  # Генерация временных рядов и последовательностей в PostgreSQL
    "debug_toolbar",  # Инструмент отладки Django
]

# apps
INSTALLED_APPS += [
    'api',
    'common',
    'users',
    'breaks',
    'organisations',
]

# after apps
INSTALLED_APPS += [
    'drf_spectacular',
]


MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "crum.CurrentRequestUserMiddleware",
    "auditlog.middleware.AuditlogMiddleware",
    'request_logging.middleware.LoggingMiddleware',
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env.str('PG_DATABASE', 'postgres'),
        "USER": env.str('PG_USER', 'postgres'),
        "PASSWORD": env.str('PG_PASSWORD', 'postgres'),
        "HOST": env.str('DB_HOST', 'localhost'),
        "PORT": env.int('DB_PORT', 5432),
    },
    'extra': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = ('users.backends.AuthBackend',)

#####################################
# DJANGO REST FRAMEWORK
#####################################
REST_FRAMEWORK = {
    "DEFAULT_PERMISSIONS_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",),

    "DEFAULT_AUTHENTICATION_CLASSES": [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',

    ],

    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FileUploadParser",
    ],

    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    "DEFAULT_SCHEMA_CLASS": 'drf_spectacular.openapi.AutoSchema',
    "DEFAULT_PAGINATION_CLASS": "common.pagination.BasePagination",
}


# AUTH_PASSWORD_VALIDATORS = [
#     {
#         "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
#     },
# ]


#####################################
# LOCALIZATION
#####################################
LANGUAGE_CODE = "ru-RU"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

#####################################
# STATIC AND MEDIA CONFIGURATION
#####################################

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#####################################
# CORS HEADERS
#####################################

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['*']
CSRF_COOKIE_SECURE = False

#####################################
# DRF SPECTACULAR
#####################################

SPECTACULAR_SETTINGS = {
    "TITLE": 'Call Helper',
    "DESCRIPTION": 'Call Helper Documentation',
    "VERSION": '1.0.0',

    "SERVE_PERMISIONS": [
        'rest_framework.permissions.IsAuthenticated',
    ],

    "SERVE_AUTHENTICATION": [
        'rest_framework.authentication.BasicAuthentication'],

    "SWAGGER_UI_SETTINGS": {
        'deepLinking': True,
        "displayOperationId": True,
        "syntaxHighlight.active": True,
        "syntaxHighlight.theme": "arta",
        "defaultModelsExpandDepth": -1,
        "displayRequestDuration": True,
        "filter": True,
        "requestSnippetsEnabled": True,
    },

    "COMPONENT_SPLIT_REQUEST": True,
    "SORT_OPERATIONS": False,

    'ENABLE_DJANGO_DEPLOY_CHECK': False,
    'DISABLE_ERRORS_AND_WARNINGS': True,

}

#######################
# DJOSER
#######################
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'SERIALIZERS': {},
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
}


################################
# SENTRY
################################
if DEBUG:
    sentry_sdk.init(
        dsn=env.str('SENTRY_DSN', ''),
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

    # Настройка Django Debug Toolbar
    INTERNAL_IPS = [
        '127.0.0.1',
    ]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',  # change debug level as appropiate
            'propagate': False,
        },
    },
}
