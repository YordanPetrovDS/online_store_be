import os
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
    "unfold",
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
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
    "drf_spectacular",
    "drf_yasg",
    "ckeditor",
    "ckeditor_uploader",
    "django_ckeditor_youtube_plugin",
    "adminsortable2",
    "mptt",
)

PROJECT_APPS = (
    "accounts",
    "cms",
    "taxes",
    "catalog",
    "utils",
    "blog",
    "geo",
    "localize",
    "stores",
    "newsletter",
    "carts",
    "shipping_methods",
    "orders",
    "payments_methods",
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
    # Disables browsable api (we have swagger already)
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "utils.exception_handling.custom_api_exception_handler",
}


IS_SWAGGER_UI_ENABLED = config("IS_SWAGGER_UI_ENABLED", default=True, cast=bool)

SPECTACULAR_SETTINGS = {
    "TITLE": "Online Store API",
    "DESCRIPTION": "Online Store API",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": "/api/",
    "COMPONENT_SPLIT_REQUEST": True,
}

# Storage settings
STORAGE_BACKEND_FS = "django.core.files.storage.FileSystemStorage"
STORAGE_BACKEND_AWS = "storages.backends.s3boto3.S3Boto3Storage"
DEFAULT_FILE_STORAGE = config("DEFAULT_FILE_STORAGE", default=STORAGE_BACKEND_FS)
if DEFAULT_FILE_STORAGE == STORAGE_BACKEND_AWS:
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME")
    AWS_S3_FILE_OVERWRITE = False
    AWS_QUERYSTRING_AUTH = False
    if config("AWS_S3_CUSTOM_DOMAIN", ""):
        AWS_S3_CUSTOM_DOMAIN = config("AWS_S3_CUSTOM_DOMAIN")

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

# User model
AUTH_USER_MODEL = "accounts.User"

# CKEditor settings
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
        "/static/ckeditor/ckeditor/plugins/youtube/",
        "plugin.js",
    )
]
CKEDITOR_CONFIGS[CKEDITOR_CONFIG_DEFAULT]["external_plugin_resources"] = ckeditor__external_plugin_resources
CKEDITOR_CONFIGS[CKEDITOR_CONFIG_SMALL]["external_plugin_resources"] = ckeditor__external_plugin_resources

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGS_DIR = "logs/"
# Check if the folder exists
if not os.path.exists(LOGS_DIR):
    # Create the folder
    os.makedirs(LOGS_DIR)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "error_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": Path(BASE_DIR, LOGS_DIR, "error.log"),
        },
        "system_events_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": Path(BASE_DIR, LOGS_DIR, "system_events.log"),
        },
    },
    "loggers": {
        "": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": True,
        },
        # Log for system background events
        "system_events": {
            "handlers": ["system_events_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

IS_SYSTEM_EVENTS_LOGGING_ENABLED = config("IS_SYSTEM_EVENTS_LOGGING_ENABLED", True, cast=bool)

# Image limits
IMAGE_MAX_MB = config("IMAGE_MAX_MB", 5, cast=int)
IMAGE_VALID_EXTENSIONS = config("IMAGE_VALID_EXTENSIONS", "png,jpeg,jpg").lower().split(",")

# Video limits
VIDEO_MAX_MB = config("VIDEO_MAX_MB", 50, cast=int)
VIDEO_VALID_EXTENSIONS = config("VIDEO_VALID_EXTENSIONS", "mp4").lower().split(",")

# Document file limits
DOCUMENT_MAX_MB = config("DOCUMENT_MAX_MB", 5, cast=int)
DOCUMENT_VALID_EXTENSIONS = config("DOCUMENT_VALID_EXTENSIONS", "pdf,doc,docx,txt,ppt,xls,xlsx").lower().split(",")

# Download file limits
DOWNLOAD_FILE_MAX_MB = config("FILE_MAX_MB", 5, cast=int)
DOWNLOAD_FILE_VALID_EXTENSIONS = (
    config("FILE_VALID_EXTENSIONS", "pdf,doc,docx,txt,ppt,xls,xlsx,zip,rar,mp3,mp4,avi,mov,jpg,jpeg,gif,png")
    .lower()
    .split(",")
)

# WebP, JPEG or PNG images compression
TINIFY_API_KEY = config("TINIFY_API_KEY", default="")
TINIFY_COMPRESSION_ENABLED = config("TINIFY_COMPRESSION_ENABLED", cast=bool, default=False)
