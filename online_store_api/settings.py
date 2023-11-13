from pathlib import Path

import dj_database_url
from decouple import config
from django.utils.translation import gettext_lazy as _

from online_store_api.utils import is_production, is_test

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = config("DEBUG", default=False, cast=bool)
APP_ENVIRONMENT = config("APP_ENVIRONMENT", default="Development")
SECRET_KEY = config("SECRET_KEY")
ALLOWED_HOSTS = config("ALLOWED_HOSTS", "localhost").split(",")
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS").split(",")
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS").split(",")

DJANGO_APPS = (
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
)

THIRD_PARTY_APPS = (
    "rest_framework",
    "django_filters",
    "corsheaders",
    "rangefilter",
    "rest_framework.authtoken",
    "drf_yasg",
    "ckeditor",
    "ckeditor_uploader",
    "adminsortable2",
)

PROJECT_APPS = (
    "accounts",
    "catalog",
    "cms",
    "utils",
    "blog",
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}

ROOT_URLCONF = "online_store_api.urls"

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

WSGI_APPLICATION = "online_store_api.wsgi.application"


DATABASES = {"default": dj_database_url.config(default=config("DATABASE_URL"))}

# Password validation
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

# Internationalization
LANGUAGE_CODE = "en-us"
LANGUAGES = (
    ("en", _("English")),
    ("bg", _("Bulgarian")),
)
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
LOCALE_PATHS = [
    BASE_DIR / "locale/",
]
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [(BASE_DIR / "assets")]

MEDIA_ROOT = BASE_DIR / "media/"
MEDIA_URL = "/media/"

CKEDITOR_UPLOAD_PATH = "ckeditor/"  # Ckeditor uses AWS, see AWS_LOCATION
CKEDITOR_CONFIG_DEFAULT = "default"
CKEDITOR_CONFIG_SMALL = "small"
CKEDITOR_CONFIGS = {
    CKEDITOR_CONFIG_DEFAULT: {
        "toolbar": "Full",
        "height": 300,
        "width": "full",
        "extraPlugins": ["youtube"],
        "toolbar_Full": [
            ["Bold", "Italic", "Underline"],
            ["Format", "Font", "FontSize", "TextColor", "BGColor"],
            [
                "NumberedList",
                "BulletedList",
                "-",
                "Outdent",
                "Indent",
                "-",
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
                "JustifyBlock",
            ],
            ["Link", "Unlink"],
            ["RemoveFormat", "Source", "CodeSnippet", "Image", "Youtube"],
        ],
    },
    CKEDITOR_CONFIG_SMALL: {
        "toolbar": "Small",
        "height": 100,
        "width": "full",
        "extraPlugins": ["youtube"],
        "toolbar_Small": [
            ["Bold", "Italic", "Underline"],
            ["Font", "FontSize", "TextColor", "BGColor"],
            [
                "NumberedList",
                "BulletedList",
                "-",
                "Outdent",
                "Indent",
                "-",
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
                "JustifyBlock",
            ],
            ["Link", "Unlink"],
            ["RemoveFormat", "Source", "CodeSnippet", "Image", "Youtube"],
        ],
    },
}
ckeditor__external_plugin_resources = [
    (
        "youtube",
        "/static/ckeditor/youtube/",
        "plugin.js",
    )
]
CKEDITOR_CONFIGS[CKEDITOR_CONFIG_DEFAULT]["external_plugin_resources"] = ckeditor__external_plugin_resources
CKEDITOR_CONFIGS[CKEDITOR_CONFIG_SMALL]["external_plugin_resources"] = ckeditor__external_plugin_resources

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING_LEVEL = "DEBUG"
if is_production():
    LOGGING_LEVEL = "INFO"
elif is_test():
    LOGGING_LEVEL = "CRITICAL"

# Image limits
IMAGE_MAX_WIDTH = config("IMAGE_MAX_WIDTH", 800, cast=int)
IMAGE_MAX_HEIGHT = config("IMAGE_MAX_HEIGHT", 600, cast=int)
IMAGE_MAX_MB = config("IMAGE_MAX_MB", 3, cast=int)
IMAGE_VALID_EXTENSIONS = config("IMAGE_VALID_EXTENSIONS", "png,jpeg,jpg").lower().split(",")

# Video limits
VIDEO_MAX_MB = config("VIDEO_MAX_MB", 50, cast=int)
VIDEO_VALID_EXTENSIONS = config("VIDEO_VALID_EXTENSIONS", "mp4,avi").lower().split(",")
