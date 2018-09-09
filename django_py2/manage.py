#!/usr/bin/env python
import sys
import os.path


PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "base", "site-packages")))
sys.path.insert(1, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "base", "site-packages","django_admin_bootstrapped")))


from base.settings import execute


if __name__ == "__main__":

    execute('python-web-framework.base', 'python-web-framework.django_py2')
