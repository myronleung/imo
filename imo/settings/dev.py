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
