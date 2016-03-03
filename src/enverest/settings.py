"""
Django settings for enverest project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from os.path import dirname, join, exists
from django.utils.translation import gettext_lazy as _


THEME_CONTACT_EMAIL = 'contact@enverest.com'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATICFILES_DIRS = [join(BASE_DIR, 'static')]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(^lbak@7d!0m-vqbll15t%xk29*9_un*k+rkvdq)t05+m&px-('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'hangfeilin@gmail.com'
EMAIL_HOST_PASSWORD = 'ybosbiqjdtpzrtqk'
EMAIL_PORT = 587

# Application definition

INSTALLED_APPS = [
    'common',
    'homepage',
    'consultant',
    'account',
    'search',
    'project',
    'userprofile',
    'pinax_theme_bootstrap',
    'bootstrapform',
    'postman',
    'payment',
    'upload',
    'storages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "account.middleware.LocaleMiddleware",
    "account.middleware.TimezoneMiddleware",
]

ROOT_URLCONF = 'enverest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(BASE_DIR, 'templates'),
            # insert more TEMPLATE_DIRS here
        ],
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

TEMPLATE_CONTEXT_PROCESSORS = [
    "account.context_processors.account",
]

WSGI_APPLICATION = 'enverest.wsgi.application'

# static files for deployment
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = "/home/ec2-user/myproject/Raccoon/static_files"

#If the request URL does not match any of the pattern in the URLconf,
#HTTPredirect is issued to the same URL appended.
APPEND_SLASH = True

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'raccoon',
        'USER': 'admin',
        'PASSWORD': 'raccoonadmin',
        'HOST': 'raccoon.cswqi4vryc9n.us-west-2.rds.amazonaws.com',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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



##################################################################
#                        AWS SECTION
##################################################################
DEFAULT_FILE_STORAGES = 'storages.backends.s3boto.S3BotoStorage'
# AWS keys
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAJOJ4LB2LY4U7KR4Q'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'hnlin-godjango-episode-46'

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

#                        AWS SECTION END
##################################################################

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGES = (
    ('en', _('English')),
    ('zh-hans', _('Chinese')),
)

# A list of directories where Django looks for translation files.
LOCALE_PATHS = ['locale']

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Postman configuration
POSTMAN_AUTO_MODERATE_AS = True # no moderator

# The URL where requests are redirected for login, especially when using the login_required() decorator.
LOGIN_URL = '/account/login/'

##################################################################
#                        LOGGING SECTION
##################################################################

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '../logs/enverest.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'project': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}
#                     LOGGING SECTION END
##################################################################