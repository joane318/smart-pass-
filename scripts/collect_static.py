"""Collect unchanged app/admin assets without connecting to D1."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "escola.settings")
import django
django.setup()
from django.conf import settings
from django.core.management import call_command

settings.STATIC_ROOT = settings.BASE_DIR / "public" / "static"
call_command("collectstatic", interactive=False, verbosity=0)
print("CSS e arquivos do administrador preparados.")

# Bundle exact copies of the existing Django packages in a clean module root.
# This keeps virtual environments, backups and private migration files outside
# the Worker module directory. The original source remains in its own location.
import shutil
root = settings.BASE_DIR
build = root / ".cloudflare-build"
build.mkdir(exist_ok=True)
for name in ("escola", "saidas"):
    shutil.copytree(root / name, build / name, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
shutil.copy2(root / "cloudflare_entry.py", build / "entry.py")
