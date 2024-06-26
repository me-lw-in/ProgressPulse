"""
Django settings for AttendanceProject project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-66h6a1u&cg-rjb+z^7s+j*i0yz+6i-wglh8(65&lqrvx*8=&jc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'mailtrap',                                 # manually added which is not necessary
    'academics.apps.AcademicsConfig',           # Academics app  
    'accounts.apps.AccountsConfig',             # Accounts app
    'attendances.apps.AttendancesConfig',       # Attendaces app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
]

AUTH_USER_MODEL = 'accounts.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'AttendanceProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR ],                                                       # added manually                            
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

WSGI_APPLICATION = 'AttendanceProject.wsgi.application'


# Database configuration -> for localhost
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'progresspulse',
#         'USER': 'postgres',
#         'PASSWORD':'Melwin@123',
#         'HOST':'localhost',   # I am using a local server
#         'PORT':'5432',      # PostgreSQL uses port 5432
#     }
# }

# Database configuration -> for AWS
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ugi',
        'USER': 'melwin',
        'PASSWORD':'Melwinadmin3',
        'HOST':'progresspulse.c3acskoi4xb6.ap-south-1.rds.amazonaws.com',   # I am using a local server
        'PORT':'5432',      # PostgreSQL uses port 5432
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
     os.path.join(BASE_DIR, 'static'),            # added manually 
    ]
             
# collects all the static files and stores it in static_root 
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ========below code is used to send email using gmail account ============

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'manishmendonca12@gmail.com'
EMAIL_HOST_PASSWORD = 'yuoq bptb mafv plqg'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# =========below code is used for testing purpose using mailtrap==========

# EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
# EMAIL_HOST_USER = '6ee78f4ba4bc8d'
# EMAIL_HOST_PASSWORD = 'e8833f0d5715f9'
# EMAIL_PORT = '2525'
# EMAIL_USE_TLS = True


# ========regular login page authenticates with custom user model and admin login page authenticates with built-in user model========

# AUTHENTICATION_BACKENDS = [
#     # 'accounts.backends.CustomUserBackend',        #use this when i should have backends.py in accounts app
#     'django.contrib.auth.backends.ModelBackend',
# ]

#AWS S3 bucket configuration
AWS_ACCESS_KEY_ID = 'AKIAQ3EGUWPYAQK2OADL '
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'progresspulse'
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = ' ap-south-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
