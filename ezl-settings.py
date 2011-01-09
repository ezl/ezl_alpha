from settings import *
import logging

DEBUG = True

INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        # 'spaciety.apps.profiling.ProfilerMiddleware',
        # 'spaciety.apps.profiling.DatabaseProfilerMiddleware',
)

def debug_toolbar_callback(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': debug_toolbar_callback,
}

DATABASES = {
    'default':{
        'ENGINE': 'postgresql_psycopg2',
        'NAME': 'leasely-ezl',
    }
}

EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

