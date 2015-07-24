import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = os.path.join(BASE_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)
DATABASE_PATH = os.path.join(PROJECT_PATH, 'backup_pdxdjango.db')
TEMPLATES = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
STATIC_DIRS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'static'))
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), ".."),
)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

BOWER_COMPONENTS_ROOT = os.path.join(PROJECT_ROOT, 'components')

BOWER_INSTALLED_APPS = (
    'jquery',
    'd3#3.3.13',
    'nvd3#1.7.1',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_PATH,
        #'ATOMIC_REQUESTS': True
    }
}

TEMPLATE_DIRS = (TEMPLATES,)

STATIC_ROOT = '../staticfiles/'

STATICFILES_DIRS = (
    STATIC_DIRS,
)

STATIC_URL = '/static/'

MEDIA_ROOT = '../../media/'
MEDIA_URL = '/media/'

PYBB_ATTACHMENT_UPLOAD_TO = '../../media/attachments/'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'chris.charles.jones@gmail.com'

EMAIL_PORT = 587
EMAIL_USE_TLS = True

try:
    from noupload import *
except ImportError:
    pass