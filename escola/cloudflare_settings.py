"""Production settings only; local Django settings remain unchanged."""
import os

from .settings import *  # noqa: F403

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = False
ALLOWED_HOSTS = [".workers.dev", "localhost", "127.0.0.1"]
DATABASES = {
    "default": {
        "ENGINE": "django_cf.db.backends.d1",
        "CLOUDFLARE_BINDING": "smart_pass_db",
    }
}
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "public" / "static"  # noqa: F405
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
