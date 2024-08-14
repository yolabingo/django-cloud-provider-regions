import os
import sys

import constants

sys.path.append(str(constants.PROJECT_ROOT_DIR))


def boot(load_admin=False, load_additional_apps=False):
    import django
    from django.conf import settings

    # Initialize a shell Django project - this creates a sqlite3 database
    INSTALLED_APPS = [
        constants.APP_NAME,
        "django_extensions",
    ]
    if load_admin:
        INSTALLED_APPS += constants.ADMIN_APPS
    if load_additional_apps:
        INSTALLED_APPS += constants.APP_DEPENDENCIES

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
        DEFAULT_AUTO_FIELD="django.db.models.AutoField",
        STATIC_URL="/static/",
        TIME_ZONE="UTC",
        USE_TZ=True,
        SECRET_KEY="aaazzz",
    )
    django.setup()
