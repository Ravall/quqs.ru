# -*- coding: utf-8 -*-
from support.settings import *

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'sancta_quqs',
            'USER': 'sancta_quqs_user',
            'PASSWORD': 'sancta_quqs_user_password',
            'HOST': '127.0.0.1',
            'PORT': '',
        }
    }
else:
    # этот файл будет на бою
    # в git-e его не будет
    from production import DATABASES

SECRET_KEY = 'gfvfnw6-2&8d^9#gy=b*vxon7a*5jr*g@*5p*^lt$47lcl-7(6'

ROOT_URLCONF = 'quqs.urls'
WSGI_APPLICATION = 'quqs.wsgi.application'

INSTALLED_APPS += (
    'django_ajax',
    'quqs',
    'front',
    'templated_email'
)

ALLOWED_HOSTS = ['quqs.ru']

TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django'
TEMPLATED_EMAIL_TEMPLATE_DIR = 'emails/' #use '' for top level template dir, ensure there is a trailing slash
TEMPLATED_EMAIL_FILE_EXTENSION = 'html'
