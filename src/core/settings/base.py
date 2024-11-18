from pathlib import Path
import environ
from django.core.management.utils import get_random_secret_key
from django.utils.translation import gettext_lazy as _

# See https://docs.djangoproject.com/en/4.2/

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

env = environ.Env()
env.read_env(BASE_DIR / '.env')

DEBUG_TOOLBAR = env.bool('DEBUG_TOOLBAR')
SECRET_KEY = env.str('DJANGO_SECRET_KEY', get_random_secret_key())
ALLOWED_HOSTS = env.str('ALLOWED_HOSTS').split(',')
CSRF_TRUSTED_ORIGINS = env.str('CSRF_TRUSTED_ORIGINS').split(',')

ASGI_APPLICATION = 'core.asgi.application'
WSGI_APPLICATION = 'core.wsgi.application'

INSTALLED_APPS = [
    'adminactions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'rest_framework',
    # Apps
    'main',
    'users',
    'booking',
    'api',
]

if DEBUG_TOOLBAR:
    INSTALLED_APPS.insert(0, 'debug_toolbar')

INSTALLED_APPS += [
    # Libs
    'django_extensions',
    'drf_spectacular',
    'django_bootstrap5',
    'compressor',
    'colorfield',
    'phonenumber_field',
    'image_uploader_widget',
    'django_recaptcha',
    'admin_extra_buttons',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG_TOOLBAR:
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'core.urls'

TEMPLATE_DIRS = [BASE_DIR / 'templates']
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATE_DIRS,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.base_processors',
            ]
        }
    }
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / env.str('SQLITE_DB_PATH'),
    }
}

REDIS_HOST = env.str('REDIS_HOST')
REDIS_PORT = env.int('REDIS_PORT')
REDIS_DB = env.int('REDIS_DB')
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL
    }
}

LANGUAGE_CODE = 'uk'
LANGUAGES = (
    ('uk', _('Ukrainian')),
    ('en', _('English'))
)
LANGUAGE_COOKIE_NAME = 'site_language'
LOCALE_PATHS = (BASE_DIR / 'src/locale',)
TIME_ZONE = env.str('TIME_ZONE')
USE_TZ = True
USE_L10N = True
USE_I18N = True

APPEND_SLASH = env.bool('APPEND_SLASH')
LOGIN_URL = '/login'
LOGOUT_REDIRECT_URL = '/'

LOG_PATH = BASE_DIR / 'logs'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = (BASE_DIR / 'static',)

INTERNAL_IPS = [env.str('INTERNAL_IPS')]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'user:login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.str('EMAIL_HOST')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_USE_TLS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'full_formatter': {
            'format': '{levelname} {asctime} {module} {process} {thread} {message}',
            'style': '{'
        },
        'base_formatter': {
            'format': '{levelname} {asctime} ({module}) {process} [{thread}] {message}',
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'full_formatter'
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_PATH / 'requests.log',
            'formatter': 'base_formatter'
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOG_PATH / 'requests.log',
            'formatter': 'base_formatter'
        },
        'mail_error': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        },
        'mail_critical': {
            'level': 'CRITICAL',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        }
    },
    'loggers': {
        'django.debug': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django': {
            'handlers': ['file_info', 'file_error', 'mail_critical'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema'
}

RECAPTCHA_PUBLIC_KEY = env.str('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env.str('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_DOMAIN = env.str('RECAPTCHA_DOMAIN')

# Custom vars
APP_NAME = env.str('APP_NAME', 'Site')
DOMAIN = env.str('DOMAIN')
ADMIN_PATH = env.str('ADMIN_PATH')
SITE_SUPPORT_EMAIL = env.str('SITE_SUPPORT_EMAIL')
MIN_USER_AGE = env.int('MIN_USER_AGE')
TOKEN_LIFETIME = env.int('TOKEN_LIFETIME')

MIN_RESERVATION_TIME = 15
MAX_RESERVATION_TIME = 15

SITE_ID = 1
ADMINS = [(APP_NAME, EMAIL_HOST_USER)]
DIRECTORY = ''
FILEBROWSER_DIRECTORY = ''
FILEBROWSER_EXTENSIONS = {
    'Image': ['.jpg', '.jpeg', '.png', '.webp', '.gif'],
    'Document': ['.txt', '.pdf', '.doc', '.rtf', '.xls', '.csv', '.py'],
    'Video': ['.mov', '.wmv', '.mpeg', '.mpg', '.avi', '.rm'],
    'Audio': ['.mp3', '.mp4', '.wav', '.aiff', '.midi', '.m4p']
}

CELERY_TIMEZONE = env.str('TIME_ZONE')
CELERY_BROKER_URL = env.str('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND')
CELERY_RESULT_EXTENDED = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BEAT_SHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json']
