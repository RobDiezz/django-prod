"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import logging.config

from django.urls import reverse_lazy

from django.utils.translation import gettext_lazy as trans
import sentry_sdk

from config import settings

sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",  # Нужно зарегистрироваться на
    # сайте, что бы получить ключ
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(exist_ok=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = settings.secret_key_django

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = settings.django_debug == "1"

ALLOWED_HOSTS = [
    "0.0.0.0",
    "127.0.0.1",
] + settings.allowed_hosts.split(",")
INTERNAL_IPS = [
    "127.0.0.1",
]

if DEBUG:
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS.append("10.0.0.2")
    INTERNAL_IPS.extend([ip[: ip.rfind(".")] + ".1" for ip in ips])

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admindocs",
    "django.contrib.sitemaps",
    # Сторонние приложения
    # "debug_toolbar",
    "rest_framework",
    "django_filters",
    "widget_tweaks",
    "drf_spectacular",
    # Программы продукта
    "shopapp.apps.ShopappConfig",
    "requestdataapp.apps.RequestdataappConfig",
    "myauth.apps.MyauthConfig",
    "myapiapp.apps.MyapiappConfig",
    "blogapp.apps.BlogappConfig",
]

MIDDLEWARE = [
    # "django.middleware.cache.UpdateCacheMiddleware",  # Обязательно должен быть вверху списка
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
    # Мидлвар проекта
    "requestdataapp.middlewares.set_useragent_on_request_middleware",
    "requestdataapp.middlewares.CountRequestMiddleware",
    "requestdataapp.middlewares.ThrottlingRequestMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    # "django.middleware.cache.FetchFromCacheMiddleware",  # Это нужно писать в конце, что бы
    # отработали все middleware
]

ROOT_URLCONF = "mysite.urls"

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

WSGI_APPLICATION = "mysite.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DATABASE_DIR / "db.sqlite3",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",  # Использовать при
        # создании приложения, она позволяет обращаться к кэшу в функциях но реально не
        # кэширеут
        # "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        # "LOCATION": "/var/tmp/django_cache",
        # "LOCATION": "c:/foo/bar", # настройка для Windows
        # "TIMEOUT": 60,
        # "OPTIONS": {"MAX_ENTRIES": 300},
    },
}

CACHE_MIDDLEWARE_SECONDS = 200  # Время кэширования в секундах

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

USE_L10N = True

LOCALE_PATHS = [
    BASE_DIR / "locale/",
]

LANGUAGES = [
    ("en", trans("English")),
    ("ru", trans("Russian")),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "uploads"
# DEFAULT_FILE_STORAGE =

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = reverse_lazy("shopapp:product_list")
LOGIN_URL = reverse_lazy("myauth:login")

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "My Site Project API",
    "DESCRIPTION": "My site with shopp app and custom auth",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

LOGFILE_NAME = BASE_DIR / "logfile.txt"
LOGFILE_SIZE = 5 * 1024 * 1024
# LOGFILE_SIZE = 400  # bytes
LOGFILE_COUNT = 3

DJANGO_LOGLEVEL = settings.loglevel

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        "": {
            "level": DJANGO_LOGLEVEL,
            "handlers": ["console",],
        },
    },

})

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "verbose": {
#             "format": "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
#         },
#     },
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "formatter": "verbose",
#         },
#         "logfile": {
#             # "class": "logging.handlers.RotatingFileHandler",  # используется для сохранения
#             # логов в битах
#             "class": "logging.handlers.TimedRotatingFileHandler",  # используется для
#             # сохранения логов в днях
#             "filename": LOGFILE_NAME,
#             # "maxBytes": LOGFILE_SIZE,
#             "when": "midnight",  # параметр для TimedRotatingFileHandler
#             "interval": 1,  # параметр для TimedRotatingFileHandler
#             "backupCount": LOGFILE_COUNT,
#             "formatter": "verbose",
#             "encoding": "utf-8",
#         },
#     },
#     "root": {
#         "handlers": [
#             # "console",
#             "logfile"
#         ],
#         "level": "INFO",
#     },
# }


# LOGGING = {
#     "version": 1,
#     "filters": {
#         "require_debug_true": {
#             "()": "django.utils.log.RequireDebugTrue",
#         },
#     },
#     "handlers": {
#         "console": {
#             "level": "DEBUG",
#             "filters": ["require_debug_true"],
#             "class": "logging.StreamHandler",
#         },
#     },
#     "loggers": {
#         "django.db.backends": {
#             "level": "DEBUG",
#             "handlers": ["console"],
#         }
#     },
# }
