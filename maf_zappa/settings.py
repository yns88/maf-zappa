"""
Django settings for maf_zappa project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IS_ZAPPA = False

# HACK zappa moves the settings file into the BASE_DIR
if os.path.basename(__file__) == 'zappa_settings.py':
    BASE_DIR = os.path.dirname(__file__)
    IS_ZAPPA = True


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

SECRETS = {}
with open(os.path.join(BASE_DIR, 'secret.env')) as secret_file:
    for line in secret_file:
        k, v = line.split('=')
        SECRETS[k] = v.strip()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRETS['SECRET_KEY']


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not IS_ZAPPA

# TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

ALLOWED_HOSTS = ['.myanimefigures.moe', 'redqxxwq67.execute-api.us-east-1.amazonaws.com']

SESSION_COOKIE_SECURE = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_zappa',
    'anime',
    'storages',
)

MIDDLEWARE_CLASSES = (
    'django_zappa.middleware.ZappaMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# TODO multiple environments
ZAPPA_SETTINGS = {
    'dev': {
        's3_bucket': 'myanimefigures_2',
        'settings_file': './maf_zappa/settings.py',
        'keep_warm': True,
        'domain': 'myanimefigures.moe',
    }
}

ROOT_URLCONF = 'maf_zappa.urls'

WSGI_APPLICATION = 'maf_zappa.wsgi.application'

DEFAULT_FILE_STORAGE = 'libs.storages.S3Storage.S3Storage'
AWS_ACCESS_KEY_ID = SECRETS['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = SECRETS['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = SECRETS['AWS_STORAGE_BUCKET_NAME']
"""
AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}
"""

# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# This is used by the `static` template tag from `static`, if you're using that. Or if anything else
# refers directly to STATIC_URL. So it's safest to always set it.
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

SECURE_HSTS_SECONDS = 3600
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': SECRETS['DB_NAME'],
        'USER': SECRETS['DB_USER'],
        'PASSWORD': SECRETS['DB_PASS'],
        'HOST': SECRETS['DB_HOST'],
        'PORT': SECRETS['DB_PORT'],
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False
