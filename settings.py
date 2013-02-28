import os
PROJECT_DIR = os.path.dirname(__file__)

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media', 'uploads/')

MEDIA_URL = '/uploads/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'media'),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'jeepblog.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'jeepblog.blog',
    'jeepblog.comments',
    'jeepblog.contactform',
    'jeepblog.resources',
)

TEMPLATE_DIRS = (os.path.join(PROJECT_DIR, 'templates/'),)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
)

CACHES = {
    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Import settings for specific site from ./localsettings.py:
from localsettings import *



# Example localsettings.py settings
# Paste these these settings into a file called localsettings.py in the root
# of your project and edit to suit

#DEBUG = False
#TEMPLATE_DEBUG = DEBUG
#
#ADMINS = (
#    ('philsmith', 'phil.smith@example.com'),
#)
#
#MANAGERS = ADMINS
#
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'HOST': 'localhost',
#        'NAME': 'your_db_name',
#        'USER': 'your_db_username',
#        'PASSWORD': 'your_db_password',
#    }
#}
#
## See http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
#TIME_ZONE = 'Europe/London'
#
## See http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-GB'
#
#SECRET_KEY = 'your secret key'
#
#RECAPTCHA_PUB_KEY = "your-recaptcha-pub-key"
#RECAPTCHA_PRIVATE_KEY = "your-recaptcha-private-key"
#ALLOWED_HOSTS = [
#    ".yourwebsite.com",
#]
