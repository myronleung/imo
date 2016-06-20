# -*- coding: utf-8 -*-
from .base import *
from django.core.exceptions import ImproperlyConfigured

import json

SECRET_KEY = ''
AWS_SECRET_ACCESS_KEY = ''

with open ('/opt/bitnami/apps/django/django_projects/Project/keys.json') as data_file:
    data = json.load(data_file)
    SECRET_KEY = data['django_key']
    AWS_SECRET_ACCESS_KEY = data['aws_key']
    MYSQL_KEY = data['mysql_key']


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'imo_db',
        'USER': 'root',
        'PASSWORD': MYSQL_KEY,
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# if 'SECRET_KEY' in os.environ:
# SECRET_KEY = 'fl_v9(iu_qm_+mq^7c)bm0qcue(j%3=n63zx-6^&#17^)(ba5f'
# SECRET_KEY = 'SECRET_KEY' in os.environ

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['54.234.253.36']

CSRF_COOKIE_SECURE = False

SESSION_COOKIE_SECURE = False

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

CSRF_COOKIE_HTTPONLY = True

X_FRAME_OPTIONS = 'DENY'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#AWS S3
DEFAULT_FILE_STORAGE = 'aws_storage_classes.MediaStorage'
AWS_ACCESS_KEY_ID = 'AKIAJ4ZZXFKWDLNIZZKQ'
AWS_STORAGE_BUCKET_NAME = 'imo-s3'
STATICFILES_STORAGE = 'aws_storage_classes.StaticStorage'
AWS_S3_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = "https://%s/static/" % AWS_S3_DOMAIN
MEDIA_URL = "https://%s/media/" % AWS_S3_DOMAIN
