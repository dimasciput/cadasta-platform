import os
from .default import *  # NOQA

INSTALLED_APPS += (
    'opbeat.contrib.django',
)

MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'opbeat.contrib.django.middleware.Opbeat404CatchMiddleware',
) + MIDDLEWARE_CLASSES

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

DEFAULT_FILE_STORAGE = 'buckets.storage.S3Storage'

AWS = {
    'BUCKET': os.environ['S3_BUCKET'],
    'ACCESS_KEY': os.environ['S3_ACCESS_KEY'],
    'SECRET_KEY': os.environ['S3_SECRET_KEY'],
    'REGION': 'us-west-2'
}

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'cadasta',
        'USER': 'cadasta',
        'PASSWORD': 'cadasta',
        'HOST': os.environ['DB_HOST']
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': [
            os.environ['MEMCACHED_HOST'],
        ],
        'OPTIONS': {'distribution': 'consistent'}
    },
    'jsonattrs': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': [
            os.environ['MEMCACHED_HOST'],
        ],
        'OPTIONS': {'distribution': 'consistent'}
    }
}

OPBEAT = {
    'ORGANIZATION_ID': os.environ['OPBEAT_ORGID'],
    'APP_ID': os.environ['OPBEAT_APPID'],
    'SECRET_TOKEN': os.environ['OPBEAT_TOKEN'],
    'ASYNC': True,
}

DJOSER.update({  # NOQA
    'DOMAIN': os.environ['DOMAIN'],
})

# Adding localhost here for uWSGI debugging!
ALLOWED_HOSTS = [os.environ['API_HOST'], os.environ['DOMAIN'], 'localhost']

ADMINS = [('Cadasta platform admins', 'platform-admin@cadasta.org')]
EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
SERVER_EMAIL = 'platform@cadasta.org'
DEFAULT_FROM_EMAIL = 'platform@cadasta.org'
ROOT_URLCONF = 'config.urls.production'

STATIC_URL = '/static/'
STATIC_ROOT = '/opt/cadasta/cadasta-platform/cadasta/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/opt/cadasta/cadasta-platform/cadasta/media/'

# Debug logging...
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/debug.log',
            'formatter': 'simple'
        },
        'email_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'opbeat': {
            'level': 'WARNING',
            'class': 'opbeat.contrib.django.handlers.OpbeatHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'email_admins', 'opbeat'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'xform.submissions': {
            'handlers': ['file', 'email_admins', 'opbeat'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # Log errors from the Opbeat module to the console
        'opbeat.errors': {
            'level': 'ERROR',
            'handlers': ['file', 'email_admins'],
            'propagate': False,
        },
    },
}
