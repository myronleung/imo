# -*- coding: utf-8 -*-
from .base import *
from django.core.exceptions import ImproperlyConfigured

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
        'PASSWORD': 'vjus84gcKpV5',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# if 'SECRET_KEY' in os.environ:
SECRET_KEY = 'fl_v9(iu_qm_+mq^7c)bm0qcue(j%3=n63zx-6^&#17^)(ba5f'
# SECRET_KEY = 'SECRET_KEY' in os.environ

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['174.129.139.15']

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

CSRF_COOKIE_HTTPONLY = True

X_FRAME_OPTIONS = 'DENY'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
