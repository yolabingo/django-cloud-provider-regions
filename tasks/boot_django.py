#!/usr/bin/env python
# This file sets up and configures Django. It's used by scripts that need to
# execute as if running in a Django server.
# https://realpython.com/installable-django-app/#running-management-commands-with-your-installable-django-app

import os

import django
from django.conf import settings

import constants

INSTALLED_APPS = [
    constants.APP_NAME,
]


def boot():
    # Initialize a shell Django project - this creates a sqlite3 database
    settings.configure(
        BASE_DIR=constants.APP_DIR,
        INSTALLED_APPS=INSTALLED_APPS,
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(constants.TEST_DB_PATH),
            }
        },
        TIME_ZONE="UTC",
        USE_TZ=True,
    )
    django.setup()
