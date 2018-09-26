#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
Django settings for Newcmdb project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vgw-uodk7qyzm%84v66rdmf4k2yku16px*(u+^ptr&^l%y3s_*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.43.50', '127.0.0.1', '192.168.1.50']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cmdb.apps.CmdbConfig',
    'rest_framework',
    # 'corsheaders',
    'django_celery_beat',
]

MIDDLEWARE = [
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cmdb.Middle.CORSMiddleware',
]

ROOT_URLCONF = 'Newcmdb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'Newcmdb.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
# from rest_framework.parsers import FormParser
# upload files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
REST_FRAMEWORK = {
    # 版本控制
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": 'v1',
    "ALLOWED_VERSIONS": ['v1', 'v2'],
    "VERSION_PARAM": 'version',
    # 请求头控制,解析器
    "DEFAULT_PARSER_CLASSES": ['rest_framework.parsers.JSONParser',
                               'rest_framework.parsers.FormParser',
                               'rest_framework.parsers.MultiPartParser',
                               'rest_framework.parsers.FileUploadParser', ],
    # 渲染器 控制,序列化了
    "DEFAULT_RENDERER_CLASSES": [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.AdminRenderer',
    ],
    # 分页多少大小
    "PAGE_SIZE": 10,

}
# from corsheaders.middleware import CorsMiddleware
AUTH_USER_MODEL = 'cmdb.UserProfile'
CSRF_COOKIE_NAME = "XCSRF-TOKEN"
# CORS_ORIGIN_ALLOW_ALL=True
# ALLOWED_HOSTS = ['*']
# CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOW_CREDENTIALS = True
# CORS_EXPOSE_HEADERS = (
#     'Access-Control-Allow-Origin: *',
# )
# CORS_ORIGIN_ALLOW_ALL = True

CELERY_BROKER_URL = 'redis://127.0.0.1/2'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1/2'
