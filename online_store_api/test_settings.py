from online_store_api.settings import *

MEDIA_ROOT = Path(BASE_DIR, "tmp/tests/")
MEDIA_URL = "/tmp/tests/"

DATABASES = {"default": dj_database_url.config(default=config("TEST_DATABASE_URL"))}

DEFAULT_FILE_STORAGE = STORAGE_BACKEND_FS  # Test files are always uploaded locally

# Not needed for tests
IS_SYSTEM_EVENTS_LOGGING_ENABLED = False
