import datetime
import os
import platform

import firebase_admin
from django.urls import reverse_lazy
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _
from environ import Env
from firebase_admin import credentials
from import_export.formats.base_formats import XLSX

# Build paths inside the project.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# django-environ allows you to use Twelve-factor methodology
# to configure your Django application with environment variables.
# https://django-environ.readthedocs.io/en/latest/
env = Env(DEBUG=(bool, False))
Env.read_env(os.path.join(BASE_DIR, '.env'))

# A secret key for a particular Django installation.
# This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.
# Django will refuse to start if SECRET_KEY is not set.
# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-SECRET_KEY
SECRET_KEY = env('SECRET_KEY')


# A boolean that turns on/off debug mode.
# Never deploy a site into production with DEBUG turned on.
# One of the main features of debug mode is the display of detailed error pages.
# If your app raises an exception when DEBUG is True,
# Django will display a detailed traceback, including a lot of metadata about your environment,
# such as all the currently defined Django settings (from settings.py).
# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-DEBUG
DEBUG = env('DEBUG')

# A list of all the people who get code error notifications.
# When DEBUG=False and AdminEmailHandler is configured in LOGGING (done by default),
# Django emails these people the details of exceptions raised in the request/response cycle.
# https://docs.djangoproject.com/en/4.1/ref/settings/#admins
ADMINS = []

# A list of strings representing the host/domain names that this Django site can serve.
# This is a security measure to prevent HTTP Host header attacks,
# which are possible even under many seemingly-safe web server configurations.
# https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]

# Application definition
# A list of strings designating all applications that are enabled in this Django installation.
# Each string should be a dotted Python path to:
# an application configuration class (preferred), or
# a package containing an application.
# https://docs.djangoproject.com/en/4.1/ref/settings/#installed-apps
INSTALLED_APPS = [
    # External apps that need to go before django's
    'storages',
    'modeltranslation',

    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.gis',
    'django.contrib.postgres',

    # External apps
    'django_celery_beat',
    'django_celery_results',
    'rest_framework',
    "rest_framework_api_key",
    'django_filters',
    'phonenumber_field',
    'sort_order_field',
    'tinymce',
    'tz_detect',
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_email',
    'two_factor',
    'two_factor.plugins.phonenumber',
    'two_factor.plugins.email',
    'django_countries',
    'mptt',
    'import_export',
    'corsheaders',

    # Local apps
    'apps.core',
    'apps.user',
    'apps.supervisor',
    'apps.editor',
    'apps.auth',
    'apps.tag',
    'apps.client',
    'apps.category',
    'apps.program',
    'apps.search',
    'apps.episode',
    'apps.importer',

    # External apps that need to go last django's
    'django_cleanup',
]

# Middleware is a framework of hooks into Django’s request/response processing.
# It’s a light, low-level “plugin” system for globally altering Django’s input or output.
# Each middleware component is responsible for doing some specific function.
# For example, Django includes a middleware component, AuthenticationMiddleware,
# that associates users with requests using sessions.
# https://docs.djangoproject.com/en/4.1/topics/http/middleware/
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'apps.core.middleware.LocaleMiddleware',
    'apps.core.middleware.ForceDefaultLanguagePrefixMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.core.middleware.TimezoneMiddleware',
    'apps.core.middleware.RequestMiddleware',
]

# A string representing the full Python importer path to your root URLconf,
# for example "app.urls". Can be overridden on a per-request basis by setting
# the attribute urlconf on the incoming HttpRequest object.
# https://docs.djangoproject.com/en/4.1/ref/settings/#root-urlconf
ROOT_URLCONF = 'project.urls'

# A list containing the settings for all template engines to be used with Django.
# Each item of the list is a dictionary containing the options for an individual engine.
# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# The full Python path of the WSGI application object that Django’s built-in servers (e.g. runserver) will use.
# The django-admin startproject management command will create a standard wsgi.py file
# with an application callable in it, and point this setting to that application.
# https://docs.djangoproject.com/en/4.1/ref/settings/#wsgi-application
WSGI_APPLICATION = 'project.wsgi.application'

# A dictionary containing the settings for all databases to be used with Django.
# It is dictionary contents map a database alias to a dictionary containing the options for an individual database.
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": env.str('SQL_ENGINE', default='django.db.backends.sqlite3'),
        "NAME": env.str('SQL_DATABASE', default=os.path.join(BASE_DIR, 'db.sqlite3')),
        "USER": env.str('SQL_USER', default='user'),
        "PASSWORD": env.str('SQL_PASSWORD', default='password'),
        "HOST": env.str('SQL_HOST', default='localhost'),
        "PORT": env.str('SQL_PORT', default='5432'),
    }
}

# The list of validators that are used to check the strength of user’s passwords.
# By default, no validation is performed and all passwords are accepted.
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Whether to use a secure cookie for the session cookie. If this is set to True, the cookie will be marked as “secure”,
# which means browsers may ensure that the cookie is only sent under an HTTPS connection.
# Leaving this setting off isn’t a good idea because an attacker could capture an unencrypted session cookie
# with a packet sniffer and use the cookie to hijack the user’s session.
# https://docs.djangoproject.com/en/4.1/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True

# Internationalization
# A list of all available languages.
# This list is continually growing and including a copy here would inevitably become rapidly out of date.
# You can see the current list of translated languages by looking in django/conf/global_settings.py.
# The list is a list of two-tuples in the format (language code, language name) – for example, ('ja', 'Japanese').
# This specifies which languages are available for language selection. See Internationalization and localization.
# Generally, the default value should suffice.
# Only set this setting if you want to restrict language selection to a subset of the Django-provided languages.
# https://docs.djangoproject.com/en/4.1/ref/settings/#languages
LANGUAGES = [
    ('en', _('English')),
    ('ar', _('العربية')),
]

# A string representing the language code for this installation.
# This should be in standard language ID format.
# For example, U.S. English is "en-us".
# https://docs.djangoproject.com/en/4.1/ref/settings/#language-code
LANGUAGE_CODE = 'en'

# A list of directories where Django looks for translation files. See How Django discovers translations.
# https://docs.djangoproject.com/en/3.2/ref/settings/#locale-paths
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# A string representing the time zone for this installation. See the list of time zones.
# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-TIME_ZONE
TIME_ZONE = 'UTC'

# A boolean that specifies whether Django’s translation system should be enabled.
# This provides a way to turn it off, for performance.
# If this is set to False, Django will make some optimizations so as not to load the translation machinery.
# https://docs.djangoproject.com/en/4.1/ref/settings/#use-i18n
USE_I18N = True

# A boolean that specifies if localized formatting of data will be enabled by default or not.
# If this is set to True, e.g. Django will display numbers and dates using the format of the current locale.
# https://docs.djangoproject.com/en/4.1/ref/settings/#use-l10n
USE_L10N = False

# A boolean that specifies if datetimes will be timezone-aware by default or not.
# If this is set to True, Django will use timezone-aware datetimes internally.
# When USE_TZ is False, Django will use naive datetimes in locale time,
# except when parsing ISO 8601 formatted strings, where timezone information will always be retained if present.
# https://docs.djangoproject.com/en/4.1/ref/settings/#use-tz
USE_TZ = True

# The default formatting to use for displaying date fields in any part of the system.
# Note that if USE_L10N is set to True,
# then the locale-dictated format has higher precedence and will be applied instead.
# See allowed date format strings.
# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-DATETIME_FORMAT
DATE_FORMAT = "Y-m-d"

# When set to True,
# if the request URL does not match any of the patterns in the URLconf and it doesn’t end in a slash,
# an HTTP redirect is issued to the same URL with a slash appended. Note that the redirect may cause any data submitted in a POST request to be lost.
APPEND_SLASH = False

# Static files (CSS, JavaScript, Images) and Media Files
# https://docs.djangoproject.com/en/3.2/howto/static-files/
# https://overiq.com/django-1-10/handling-media-files-in-django/
# https://docs.djangoproject.com/en/2.2/topics/files/
USE_S3 = env.bool('USE_S3', default=False)

if USE_S3:
    # Alibaba Cloud OSS settings
    ALIYUN_OSS_ACCESS_KEY_ID = env('ALIYUN_OSS_ACCESS_KEY_ID')
    ALIYUN_OSS_ACCESS_KEY_SECRET = env('ALIYUN_OSS_ACCESS_KEY_SECRET')
    ALIYUN_OSS_BUCKET_NAME = env('ALIYUN_OSS_BUCKET_NAME')
    ALIYUN_OSS_ENDPOINT = env('ALIYUN_OSS_ENDPOINT')  # e.g., 'oss-cn-shanghai.aliyuncs.com'

    # Static files settings
    ALIYUN_STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{ALIYUN_OSS_BUCKET_NAME}.{ALIYUN_OSS_ENDPOINT}/{ALIYUN_STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'project.storage_backends.StaticStorage'

    # Media files settings
    ALIYUN_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{ALIYUN_OSS_BUCKET_NAME}.{ALIYUN_OSS_ENDPOINT}/{ALIYUN_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'project.storage_backends.MediaStorage'

else:
    # URL to use when referring to static files located in STATIC_ROOT.
    # https://docs.djangoproject.com/en/4.1/ref/settings/#static-url
    STATIC_URL = '/static/'

    # The absolute path to the directory where collectstatic will collect static files for deployment.
    # Example: "/var/www/example.com/static/"
    # If the staticfiles contrib app is enabled (as in the default project template),
    # the collectstatic management command will collect static files into this directory.
    # See the how-to on managing static files for more details about usage.
    # https://docs.djangoproject.com/en/4.1/ref/settings/#static-root
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    # URL that handles the media served from MEDIA_ROOT,
    # used for managing stored files. It must end in a slash if set to a non-empty value.
    # You will need to configure these files to be served in both development and production environments.
    MEDIA_URL = '/media/'

    # Absolute filesystem path to the directory that will hold user-uploaded files.
    # Example: "/var/www/example.com/media/"
    # https://docs.djangoproject.com/en/4.1/ref/settings/#media-root
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# This setting defines the additional locations
# the staticfiles app will traverse if the FileSystemFinder finder is enabled,
# e.g. if you use the collect static or find static management command or use the static file serving view.
# https://docs.djangoproject.com/en/4.1/ref/settings/#staticfiles-dirs
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# This variable is used to return the absolute url for default user image.

# Default primary key field type
# Default primary key field type to use for models that don’t have a field with primary_key=True.
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# The SITE_ID setting specifies the database ID of the Site object
# associated with that particular settings file.
# https://docs.djangoproject.com/en/4.1/ref/contrib/sites/
SITE_ID = 1

# Although Python provides a mail sending interface via the smtplib module,
# Django provides a couple of light wrappers over it.
# These wrappers are provided to make sending email extra quick, to help test email sending during development,
# and to provide support for platforms that can’t use SMTP.
# https://docs.djangoproject.com/en/3.2/topics/email/
EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_PORT = 465
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Celery is a task queue with batteries included.
# It’s easy to use so that you can get started without learning the full complexities of the problem it solves.
# It’s designed around best practices so that your product can scale and integrate with other languages,
# and it comes with the tools and support you need to run such a system in production.
# https://docs.celeryq.dev/en/stable/getting-started/introduction.html#get-started
CELERY_BACKEND = 'redis://localhost:6379/3'
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_ENABLE_UTC = True

# The modeltranslation application is used to translate dynamic content of existing Django models
# to an arbitrary number of languages without having to change the original model classes.
# It uses a registration approach (comparable to Django’s admin app) to be able to add translations to existing
# or new projects and is fully integrated into the Django admin backend.
# https://django-modeltranslation.readthedocs.io/en/latest/index.html
MODELTRANSLATION_DEFAULT_LANGUAGE = LANGUAGE_CODE

# Resizes image origin to specified size. Compatible with sorl-thumbnail. Inherits from ImageField.
# Configuration (optional)
# https://github.com/un1t/django-resized
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 100
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {
    'PNG': '.png',
    'JPG': '.jpg',
    'JPEG': '.jpg'
}

# django-notifications is a GitHub notification alike app for Django, it was derived from django-activity-stream
# The major difference between django-notifications and django-activity-stream:
# django-notifications is for building something like GitHub "Notifications"
# While django-activity-stream is for building GitHub "News Feed"
# https://github.com/django-notifications/django-notifications
DJANGO_NOTIFICATIONS_CONFIG = {'USE_JSONFIELD': True, 'SOFT_DELETE': True}

# Django Random ID Model
# This module provides a base class for Django models that gives them a random primary key id.
# https://github.com/samirelanduk/django-random-id-model
ID_DIGITS_LENGTH = 12

# A Django library which interfaces with python-phonenumbers to validate,
# pretty print and convert phone numbers. python-phonenumbers is a port of
# Google’s lib phonenumber library, which powers Android’s phone number handling.
# https://django-phonenumber-field.readthedocs.io/en/latest/
PHONENUMBER_DEFAULT_REGION = 'SA'

# Pagination allows you to control how many objects per page are returned.
# This variable is used to determine the number of objects that will be returned with each page.
PAGINATION_PAGE_SIZE = 10

# Django REST framework
#  is a powerful and flexible toolkit for building Web APIs.
# The Web browsable API is a huge usability win for your developers.
# https://www.django-rest-framework.org/
REST_FRAMEWORK = {
    'SEARCH_PARAM': 'search',
    'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.Pagination',
    'PAGE_SIZE': PAGINATION_PAGE_SIZE,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.auth.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
}

# A datetime.timedelta object which specifies how long access tokens are valid.
# This timedelta value is added to the current UTC time during token generation
# to obtain the token’s default “exp” claim value.
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html#access-token-lifetime
ACCESS_TOKEN_LIFETIME = datetime.timedelta(days=365)

# A datetime.timedelta object which specifies how long refresh tokens are valid.
# This timedelta value is added to the current UTC time during token generation
# to obtain the token’s default “exp” claim value.
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html#refresh-token-lifetime
REFRESH_TOKEN_LIFETIME = datetime.timedelta(days=400)

# Simple JWT provides a JSON Web Token authentication backend for the Django REST Framework.
# It aims to cover the most common use cases of JWTs by offering a conservative set of default features.
# It also aims to be easily extensible in case a desired feature is not present.
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': ACCESS_TOKEN_LIFETIME,
    'REFRESH_TOKEN_LIFETIME': REFRESH_TOKEN_LIFETIME,
    'AUTH_HEADER_TYPES': ('Bearer', 'JWT',),
}
# This project brings a declaritive, organized approach to managing access control in Django REST Framework projects.
# Each ViewSet or function-based view can be assigned an explicit privacy_policy for the exposed resources.
# No more digging through views or seralizers to understand access logic
# it's all in one place in a format that less technical stakeholders can understand.
# If you're familiar with other declaritive access models, such as AWS' IAM, the syntax will be familiar.
DRF_ACCESS_POLICY = {"reusable_conditions": ["project.global_access_conditions"]}

# Substituting a custom User model
# Some kinds of projects may have authentication requirements for which Django’s built-in User model
# is not always appropriate.
# For instance, on some sites it makes more sense to use an email address as your identification token
# instead of a username.
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#substituting-a-custom-user-model
AUTH_USER_MODEL = 'user.User'

# A list of authentication backend classes (as strings) to use when attempting to authenticate a user.
# https://docs.djangoproject.com/en/4.1/ref/settings/#authentication-backends
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#authentication-backends
AUTHENTICATION_BACKENDS = [
    'apps.auth.backends.UsernameOrPhoneNumberOrEmailBackend',
]

# The URL or named URL pattern where requests are redirected after login when the LoginView doesn’t get
# a next GET parameter.
# https://docs.djangoproject.com/en/4.1/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = reverse_lazy('redirect')

# The URL or named URL pattern where requests are redirected for login when using the login_required() decorator,
# LoginRequiredMixin, or AccessMixin.
# https://docs.djangoproject.com/en/4.1/ref/settings/#login-url
LOGIN_URL = LOGIN_REDIRECT_URL

# The default value for the X-Frame-Options header used by XFrameOptionsMiddleware.
# https://docs.djangoproject.com/en/4.1/ref/settings/#x-frame-options
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Complete Two-Factor Authentication for Django.
# Built on top of the one-time password framework django-otp and Django’s built-in authentication framework
# django.contrib.auth for providing the easiest integration into most Django projects.
# Inspired by the user experience of Google’s Two-Step Authentication,
# allowing users to authenticate through call,
# text messages (SMS) or by using a token generator app like Google Authenticator.




# Resend is a reliable platform for email communication and customer engagement.
# It ensures secure and efficient email delivery.
TWO_FACTOR_EMAIL_GATEWAY = 'apps.plugins.email.gateway.Resend'

# Store credentials like Resend API Key securely to prevent unauthorized access.
RESEND_API_KEY = env("RESEND_API_KEY")
RESEND_DOMAIN_KEY = env("RESEND_DOMAIN_KEY")

# Prints the tokens to the logger.
# You will have to set the message level of the two_factor logger to INFO for them to appear in the console.
# Useful for local development.
# You should configure your logging like this:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'two_factor': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

# The Google Maps API key is a unique identifier that is used to authenticate and
# authorize access to the Google Maps API services.
# It allows you to make requests to the API and track your usage.
GOOGLE_MAP_API_KEY = env('GOOGLE_MAP_API_KEY')

# A Django App that adds Cross-Origin Resource Sharing (CORS) headers to responses.
# This allows in-browser requests to your Django application from other origins.
# CORS_ALLOW_ALL_ORIGINS: bool
# If True, all origins will be allowed. Other settings restricting allowed origins will be ignored. Defaults to False.
# https://github.com/adamchainz/django-cors-headers
CORS_ALLOW_ALL_ORIGINS = True

# Redis cache backend for Django
# django-redis is a BSD licensed, full featured Redis cache and session backend for Django.
USE_REDIS_CACHE = env.bool('USE_REDIS_CACHE', default=False)

if USE_REDIS_CACHE:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }

# importer-export is available on the Python Package Index (PyPI),
IMPORT_EXPORT_FORMATS = [XLSX]
EXPORT_FORMATS = [XLSX]

# Check if the system is Windows or macOS
# If it is, set the GDAL_LIBRARY_PATH and GEOS_LIBRARY_PATH using the environment variable.
# Otherwise, it will default to an empty string.
if platform.system() == 'Windows':
    GDAL_LIBRARY_PATH = r'C:\Projects\backend\django\rakez\rakez\venv\Lib\site-packages\osgeo\gdal304.dll'
elif platform.system() == 'Darwin':
    GDAL_LIBRARY_PATH = '/opt/homebrew/Cellar/gdal/3.10.1_1/lib/libgdal.36.3.10.1.dylib'
    GEOS_LIBRARY_PATH = '/opt/homebrew/Cellar/geos/3.13.0/lib/libgeos_c.1.19.0.dylib'


SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY", "")
