#!/usr/bin/python
import os
import importlib
from django.core.management import execute_manager

try:
    #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.production")
    settings_name = os.environ.get('DJANGO_SETTINGS_MODULE', 'config.production')
    settings = importlib.import_module(settings_name)

    #import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
