# coding=utf-8
import os, sys
import random

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "site-packages"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "..", ".."))

# from menu import FRESH_MENU
BASE_DIR = os.path.join(PROJECT_ROOT, '..', 'base', "site-packages", "django_admin_bootstrapped")


def load_settings(settings, debug=False, **kwargs):
    ugettext = lambda s: s
    settings.update(
        {
            'TEMPLATE_LOADERS': (
                (
                    # 'django.template.loaders.cached.Loader',
                    # (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    # )
                ),
            ),

            'DEBUG': debug,
            'TEMPLATE_DEBUG': debug,
            'TEST': False,
            'DATABASE_ROUTERS': ['django_py2.db_router.MainRouter'],
            'DATABASE_MAPPING': {"django_db": "django_db"},
            'DATABASE_READ_MAPPING': {"django_db": "django_db"},

            'DATABASES': {
                'default': {
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': 'django_db',  # Or path to database file if using sqlite3.
                    'USER': 'root',  # Not used with sqlite3.
                    'PASSWORD': '',  # Not used with sqlite3.
                    'HOST': 'localhost',  # Set to sempty string for localhost. Not used with sqlite3.
                    'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
                    'CHARSET': 'utf8',
                    'OPTIONS': {
                        # 'init_command': 'SET storage_engine=INNODB; SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;set autocommit=1;',
                        # 'charset':'utf8mb4',
                    },
                },
            },

            'APK_UPLOAD_PATH': "/tmp/data/download",
            'PROJECT_ROOT': PROJECT_ROOT,
            'ANONYMOUS_USER_ID': -1,

            'TEMPLATE_DIRS': (
                os.path.join(PROJECT_ROOT, "templates"),
                os.path.join(PROJECT_ROOT, "content/templates"),
                os.path.join(PROJECT_ROOT, "statics/edit_demo/js/modules"),
                os.path.join(BASE_DIR, "templates"),
            ),
            'ROOT_URLCONF': 'django_py2.urls',
            'STATICFILES_FINDERS': [
                'django.contrib.staticfiles.finders.FileSystemFinder',
                'django.contrib.staticfiles.finders.AppDirectoriesFinder',
            ],
            'STATICFILES_DIRS': (
                os.path.join(PROJECT_ROOT, 'statics'),
            ),
            # "STATIC_ROOT": os.path.join(PROJECT_ROOT, 'statics'),
            'TEMPLATE_CONTEXT_PROCESSORS': (
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.request",
                'django.core.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                "django.contrib.auth.context_processors.auth",),

            'MIDDLEWARE_CLASSES': [
                'django.middleware.common.CommonMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                # 'app.permission.middleware.PermMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
                'django.middleware.transaction.TransactionMiddleware',
                # 'app.middleware.profile_middleware.ProfileMiddleware',
                # 'app.middleware.user_path_middleware.UserPathMiddleware',
            ],

            # 'AUTH_USER_MODEL': 'user.User',

            'INSTALLED_APPS': [
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                # 'django.contrib.sites',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'django_admin_bootstrapped',
                'django.contrib.admin',
                'django.contrib.admindocs',
                'django.contrib.admin',
                'django.contrib.admindocs',
                'django_py2.content',
                # 'django_py2.user',
            ],
            "LOGIN_URL": "/signin",
            "LOGIN_REDIRECT_URL": "/",
            "MENU_CONFIG": [],
            "NEW_MENU_CONFIG": [],
            # "FRESH_MENU_CONFIG": FRESH_MENU,
            "FUNC_INIT_DOWNLOAD_AMOUNT": lambda: random.randint(5000, 9999),
            "ALWAYS_ALLOWED_PERMS": ("signout/$", "signin/$"),
            'COUNT_KEY': 'down:count:key',
            'memcache_code': ["127.0.0.1:11211"],
            'redis_count': {'host': '127.0.0.1', 'port': 6379, 'db': 0},
            'SESSION_EXPIRE_AT_BROWSER_CLOSE': True,
            'SESSION_COOKIE_AGE': 24*60*60,
            'DEFAULT_APP_LOGO': "/static/img/xTransforms1.png",
            'RESOURCE_STATIC': '/tmp/winlesson/orders/',

        }
    )


def check_settings(settings):
    pass

