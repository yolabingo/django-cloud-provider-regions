#!/usr/bin/env python

from django.core.management import call_command
from boot_django import boot_django

from constants import APP_NAME

boot_django()
call_command("makemigrations", APP_NAME)
