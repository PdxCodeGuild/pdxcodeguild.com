import os
import stripe
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMINS = (
    ('Christopher Jones', 'chris@pdxcodeguild.com'),
)
MANAGERS = ADMINS

SECRET_KEY = open(os.path.expanduser('~/.gallery-secret')).read().strip()



ALLOWED_HOSTS = [
    'pdxcodeguild.com',
    'www.pdxcodeguild.com',
]


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_comments',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'pdxcodeguild',
    'crispy_forms',
    'south',
    'sekizai',
    'markdown',
    'pybb',
    'compressor',
    'django.contrib.sitemaps',
    'tagging',
    'mptt',
    'zinnia_bootstrap',
    'zinnia',
    'captcha'
)

COMPRESS_ENABLED = False

COMPRESS_CSS_FILTERS = ['compressor.filters.cssmin.CSSMinFilter',
    ]

COMPRESS_JS_FILTERS = ['compressor.filters.template.TemplateFilter',
                       'compressor.filters.jsmin.JSMinFilter',
                       ]

COMPRESS_REBUILD_TIMEOUT = [60]

MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': True})

MARKITUP_SET = 'markitup/sets/markdown'

MARKITUP_SKIN = 'markitup/skins/markitup'

JQUERY_URL = None


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pybb.middleware.PybbMiddleware',
)

TEMPLATE_LOADERS = (
    'app_namespace.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.static',
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    'pybb.context_processors.processor',
    'zinnia.context_processors.version',
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

PYBB_ATTACHMENT_SIZE_LIMIT = 40960 * 40960
PYBB_ATTACHMENT_ENABLE = True

ROOT_URLCONF = 'pdxcg.urls'

WSGI_APPLICATION = 'pdxcg.wsgi.application'


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
SITE_ID = 1

LOGIN_REDIRECT_URL = 'mainpage'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

AKISMET_API_KEY = '96824e9c0145'

ZINNIA_SPAM_CHECKER_BACKENDS = (
    'zinnia_akismet.akismet',
)

RECAPTCHA_PRIVATE_KEY = 'SKDJFGNSLKDJF'
RECAPTCHA_PUBLIC_KEY = 'SFDJSODFJ'
try:
    from local_settings import *
except ImportError:
    pass

