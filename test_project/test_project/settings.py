import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'database.db')
    }
}

STATIC_ROOT = ''
STATIC_URL = '/static/'

SECRET_KEY = 'not-so-secret'

ROOT_URLCONF = 'test_project.urls'

WSGI_APPLICATION = 'test_project.wsgi.application'

TIME_ZONE = 'Europe/Berlin'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'command_scheduler',
    'testapp',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
