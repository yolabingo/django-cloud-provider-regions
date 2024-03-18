# This file sets up and configures Django. It's used by scripts that need to
# execute as if running in a Django server.
# https://realpython.com/installable-django-app/#running-management-commands-with-your-installable-django-app

import os
import django
from django.conf import settings

from constants import APP_NAME, APP_DIR

BASE_DIR = APP_DIR


def boot_django():
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        },
        INSTALLED_APPS=(APP_NAME,),
        TIME_ZONE="UTC",
        USE_TZ=True,
    )
    django.setup()
