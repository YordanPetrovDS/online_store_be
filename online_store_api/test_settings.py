from online_store_api.settings import *

MEDIA_ROOT = Path(BASE_DIR, "tmp/tests/")
MEDIA_URL = "/tmp/tests/"

DATABASES = {"default": dj_database_url.config(default=config("TEST_DATABASE_URL"))}
