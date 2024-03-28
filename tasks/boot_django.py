import os
import sys

import base

sys.path.append(str(base.PROJECT_ROOT_DIR))


def boot(load_admin=False, load_additional_apps=False):
    import django
    from django.conf import settings

    # Initialize a shell Django project - this creates a sqlite3 database
    INSTALLED_APPS = [
        base.APP_NAME,
        "django_extensions",
    ]
    if load_admin:
        INSTALLED_APPS += base.ADMIN_APPS
    if load_additional_apps:
        INSTALLED_APPS += base.APP_DEPENDENCIES

    settings.configure(
        BASE_DIR=base.APP_DIR,
        INSTALLED_APPS=INSTALLED_APPS,
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(base.TEST_DB_PATH),
            }
        },
        DEFAULT_AUTO_FIELD="django.db.models.AutoField",
        STATIC_URL="/static/",
        TIME_ZONE="UTC",
        USE_TZ=True,
        SECRET_KEY="aaazzz",
    )
    django.setup()
