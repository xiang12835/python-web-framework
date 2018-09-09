#!/usr/bin/env python
import os
import sys


PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "base", "site-packages")))
sys.path.insert(1, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "base", "site-packages","django_admin_bootstrapped")))


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "content_settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
