"""
Django settings for cadasta project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@=fy$)xx+6yjo*us@&+m6$14@l-s6#atg(msm=9%)9@%b7l%h('

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'accounts.User'

SITE_ID = 1

# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.gis',
    'corsheaders',

    'core',
    'geography',
    'accounts',
    'organization',
    'spatial',
    'questionnaires',
    'resources',
    'buckets',
    'party',
    'xforms',

    'crispy_forms',
    'parsley',
    'widget_tweaks',
    'django_countries',
    'leaflet',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework.authtoken',
    'rest_framework_docs',
    'djoser',
    'tutelary',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'sass_processor',
    'simple_history',
    'jsonattrs',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'audit_log.middleware.UserLoggingMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_VERSIONING_CLASS':
    'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_VERSION': 'v1',
    'EXCEPTION_HANDLER': 'core.views.api.exception_handler'
}

SITE_NAME = 'Cadasta'

BASE_TEMPLATE_DIR = os.path.join(os.path.dirname(BASE_DIR), 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_TEMPLATE_DIR,
                 os.path.join(BASE_TEMPLATE_DIR, 'allauth')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    'core.backends.Auth',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

DJOSER = {
    'SITE_NAME': SITE_NAME,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_URL':
    'account/password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'account/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
}

CORS_ORIGIN_ALLOW_ALL = False

LOGIN_REDIRECT_URL = '/dashboard/'
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'

WSGI_APPLICATION = 'config.wsgi.application'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_URL
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
ACCOUNT_FORMS = {
    'signup': 'accounts.forms.RegisterForm',
    'profile': 'accounts.forms.ProfileForm',
}
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_REDIRECT_URL = LOGIN_URL

OSM_ATTRIBUTION = _(
    "Base map data &copy; <a href=\"http://openstreetmap.org\">"
    "OpenStreetMap</a> contributors under "
    "<a href=\"http://opendatacommons.org/licenses/odbl/\">ODbL</a>"
)
DIGITALGLOBE_ATTRIBUTION = _("Imagery &copy; DigitalGlobe")
DIGITALGLOBE_TILESET_URL_FORMAT = (
    'https://{{s}}.tiles.mapbox.com/v4/digitalglobe.{}'
    '/{{z}}/{{x}}/{{y}}.png?access_token='
    'pk.eyJ1IjoiZGlnaXRhbGdsb2JlIiwiYSI6ImNpaHhtenBmZjAzYW1'
    '1a2tvY2p3MnpjcGcifQ.vF1gH0mGgK31yeHC1k1Tqw'
)

LEAFLET_CONFIG = {
    'TILES': [
        (
            _("OpenStreetMap"),
            'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            {'attribution': OSM_ATTRIBUTION,
             'maxZoom': 19}
        ),
        (
            _("+Vivid imagery"),
            DIGITALGLOBE_TILESET_URL_FORMAT.format('n6ngnadl'),
            {'attribution': DIGITALGLOBE_ATTRIBUTION,
             'maxZoom': 22}
        ),
        (
            _("Recent imagery"),
            DIGITALGLOBE_TILESET_URL_FORMAT.format('nal0g75k'),
            {'attribution': DIGITALGLOBE_ATTRIBUTION,
             'maxZoom': 22}
        ),
        (
            _("+Vivid imagery with OpenStreetMap"),
            DIGITALGLOBE_TILESET_URL_FORMAT.format('n6nhclo2'),
            {'attribution': (OSM_ATTRIBUTION, DIGITALGLOBE_ATTRIBUTION),
             'maxZoom': 22}
        ),
        (
            _("Recent imagery with OpenStreetMap"),
            DIGITALGLOBE_TILESET_URL_FORMAT.format('nal0mpda'),
            {'attribution': (OSM_ATTRIBUTION, DIGITALGLOBE_ATTRIBUTION),
             'maxZoom': 22}
        ),
    ],
    'RESET_VIEW': False,
    'PLUGINS': {
        'draw': {
            'js': '/static/leaflet/draw/leaflet.draw.js'
        },
        'groupedlayercontrol': {
            'js': '/static/js/leaflet.groupedlayercontrol.min.js',
            'css': '/static/css/leaflet.groupedlayercontrol.min.css'
        }
    }
}

# Invalid names for Cadasta organizations, projects, and usernames
CADASTA_INVALID_ENTITY_NAMES = ['add', 'new']

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
LANGUAGES = [
    # ('ar', _('Arabic')),    (hiding until RTL support fixed)
    ('en', _('English')),
    # ('fr', _('French')),    (hiding until translation coverage >= 75%)
    # ('de', _('German')),    (hiding until translation coverage >= 75%)
    # ('es', _('Spanish')),   (hiding until translation coverage >= 75%)
    ('id', _('Indonesian')),
    ('pt', _('Portuguese')),
    # ('sw', _('Swahili')),   (hiding until translation coverage >= 75%)
]

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

SASS_PROCESSOR_INCLUDE_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), 'core/node_modules'),
)

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
)

JSONATTRS_SCHEMA_SELECTORS = {
    'spatial.spatialunit': (
        'project.organization.pk',
        'project.pk', 'project.current_questionnaire'
    ),
    'spatial.spatialrelationship': (
        'project.organization.pk', 'project.pk',
        'project.current_questionnaire'
    ),
    'party.party': (
        'project.organization.pk', 'project.pk',
        'project.current_questionnaire',
        'type'
    ),
    'party.partyrelationship': (
        'project.organization.pk', 'project.pk',
        'project.current_questionnaire'
    ),
    'party.tenurerelationship': (
        'project.organization.pk', 'project.pk',
        'project.current_questionnaire'
    )
}

ATTRIBUTE_GROUPS = {
    'location_attributes': {
        'app_label': 'spatial',
        'model': 'spatialunit'
    },
    'location_relationship_attributes': {
        'app_label': 'spatial',
        'model': 'spatialrelationship'
    },
    'party_attributes': {
        'app_label': 'party',
        'model': 'party'
    },
    'party_relationship_attributes': {
        'app_label': 'party',
        'model': 'partyrelationship'
    },
    'tenure_relationship_attributes': {
        'app_label': 'party',
        'model': 'tenurerelationship'
    }
}

ICON_URL = ('https://s3-us-west-2.amazonaws.com/cadasta-platformprod'
            '-bucket/icons/{}.png')

MIME_LOOKUPS = {
    'application/pdf': 'pdf',
    'audio/1d-interleaved-parityfec': '1d-interleaved-parityfec',
    'audio/32kadpcm': '32kadpcm',
    'audio/3gpp': '3gpp',
    'audio/3gpp2': '3gpp2',
    'audio/ac3': 'ac3',
    'audio/aac': 'aac',
    'audio/aacp': 'aacp',
    'audio/amr': 'amr',
    'audio/amr-wb': 'amr-wb',
    'audio/amr-wb+': 'amr-wb+',
    'audio/aptx': 'aptx',
    'audio/asc': 'asc',
    'audio/ATRAC-ADVANCED-LOSSESS': 'ATRAC-ADVANCED-LOSSLESS',
    'audio/ATRAC-X': 'ATRAC-X',
    'audio/ATRAC3': 'ATRAC3',
    'audio/basic': 'basic',
    'audio/BV16': 'BV16',
    'audio/BV32': 'BV32',
    'audio/clearmode': 'clearmode',
    'audio/CN': 'CN',
    'audio/DAT12': 'DAT12',
    'audio/dls': 'dls',
    'audio/dsr-es201108': 'dsr-es201108',
    'audio/dsr-es202050': 'dsr-es202050',
    'audio/dsr-es202211': 'dsr-es202211',
    'audio/dsr-es202212': 'dsr-es202212',
    'audio/DV': 'DV',
    'audio/DV14': 'DV14',
    'audio/eac3': 'eac3',
    'audio/encaprtp': 'encaprtp',
    'audio/EVRC': 'EVRC',
    'audio/EVRC-QCP': 'EVRC-QCP',
    'audio/EVRC0': 'EVRC0',
    'audio/EVRC1': 'EVRC1',
    'audio/EVRCB': 'EVRCB',
    'audio/EVRCB0': 'EVRCB0',
    'audio/EVRCB1': 'EVRCB1',
    'audio/EVRCNW': 'EVRCNW',
    'audio/EVRCNW0': 'EVRCNW0',
    'audio/EVRCNW1': 'EVRCNW1',
    'audio/EVRCWB': 'EVRCWB',
    'audio/EVRCWB0': 'EVRCWB0',
    'audio/EVRCWB1': 'EVRCWB1',
    'audio/EVS': 'EVS',
    'audio/example': 'example',
    'audio/fwdred': 'fwdred',
    'audio/G711-0': 'G711-0',
    'audio/G719': 'G719',
    'audio/G7221': 'G7221',
    'audio/G722': 'G722',
    'audio/G723': 'G723',
    'audio/G726-16': 'G726-16',
    'audio/G726-24': 'G726-24',
    'audio/G726-32': 'G726-32',
    'audio/G726-40': 'G726-40',
    'audio/G728': 'G728',
    'audio/G729': 'G729',
    'audio/G7291': 'G7291',
    'audio/G729D': 'G729D',
    'audio/G729E': 'G729E',
    'audio/GSM': 'GSM',
    'audio/GSM-EFR': 'GSM-EFR',
    'audio/GSM-HR-08': 'GSM-HR-08',
    'audio/iLBC': 'iLBC',
    'audio/ip-mr_v2.5': 'ip-mr_v2.5',
    'audio/L8': 'L8',
    'audio/L16': 'L16',
    'audio/L20': 'L20',
    'audio/L24': 'L24',
    'audio/LPC': 'LPC',
    'audio/mobile-xmf': 'mobile-xmf',
    'audio/MPA': 'MPA',
    'audio/MP4A-LATM': 'MP4A-LATM',
    'audio/mpa-robust': 'mpa-robust',
    'audio/m4a': 'm4a',
    'audio/midi': 'midi',
    'audio/mpeg1': 'mpeg1',
    'audio/MPA2': 'MPA2',
    'audio/mpa-robust3': 'mpa-robust3',
    'audio/mpeg3': 'mp3',
    'audio/mpeg': 'mp3',
    'audio/mp3': 'mp3',
    'audio/mp4': 'mp4',
    'audio/mpeg4-generic': 'mp4',
    'audio/ogg': 'ogg',
    'audio/opus': 'opus',
    'audio/parityfec': 'parityfec',
    'audio/PCMA': 'PCMA',
    'audio/PCMA-WB': 'PCMA-WB',
    'audio/PCMU': 'PCMU',
    'audio/PCMU-WB': 'PCMU-WB',
    'audio/QCELP': 'QCELP',
    'audio/raptorfec': 'raptorfec',
    'audio/RED': 'RED',
    'audio/rtp-enc-aescm128': 'rtp-enc-aescm128',
    'audio/rtploopback': 'rtploopback',
    'audio/rtp-midi': 'rtp-midi',
    'audio/rtx': 'rtx',
    'audio/SMV': 'SMV',
    'audio/SMV0': 'SMV0',
    'audio/SMV-QCP': 'SMV-QCP',
    'audio/sp-midi': 'sp-midi',
    'audio/speex': 'speex',
    'audio/t140c': 't140c',
    'audio/t38': 't38',
    'audio/telephone-event': 'telephone-event',
    'audio/tone': 'tone',
    'audio/UEMCLIP': 'UEMCLIP',
    'audio/ulpfec': 'ulpfec',
    'audio/VDVI': 'VDVI',
    'audio/VMR-WB': 'VMR-WB',
    'audio/vorbis': 'vorbis',
    'audio/vorbis-config': 'vorbis-config',
    'audio/wav': 'wav',
    'audio/wave': 'wave',
    'audio/x-flac': 'x-flac',
    'audio/x-mpeg-3': 'mp3',
    'audio/x-midi': 'x-midi',
    'audio/x-wav': 'x-wav',
    'video/mpeg': 'mp3',
    'video/x-mpeg': 'mp3',
    'video/mp4': 'mp4',
    'application/msword': 'doc',
    'application/vnd.openxmlformats-officedocument.'
    'wordprocessingml.document': 'docx',
    'application/msexcel': 'xls',
    'application/vnd.ms-excel': 'xls',
    'application/vnd.openxmlformats-'
    'officedocument.spreadsheetml.sheet': 'xlsx',
    'text/xml': 'xml',
    'application/xml': 'xml',
    'text/csv': 'csv',
    'text/plain': 'csv',
    'image/jpeg': 'jpg',
    'image/png': 'png',
    'image/gif': 'gif',
    'image/tif': 'tiff',
    'image/tiff': 'tiff'
}

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# the first hasher in this list is the preferred algorithm.  any
# password using different algorithms will be converted automatically
# upon login
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]
