# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
    'templated_email',
    'constance',
    'constance.backends.database',
)

ALLOWED_HOSTS = ['quqs.ru']

TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django'
TEMPLATED_EMAIL_TEMPLATE_DIR = 'emails/' #use '' for top level template dir, ensure there is a trailing slash
TEMPLATED_EMAIL_FILE_EXTENSION = 'html'


TEMPLATE_CONTEXT_PROCESSORS += (
    'constance.context_processors.config',
)

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'LEFT_TEXT': (
        'Открытки с картинками иностранных и российских иллюстраторов. Цена 150-200 рублей. Размер как у стандартной почтовой открытки, плотный картон.',
        'текст слева'
    ),
    'MY_PHONE': ('+7 964 500-25-33', 'Номер телефона'),
    'MY_EMAIL': ('nikita@quqs.ru', 'еmail'),

}