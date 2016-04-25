from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

for template_engine in TEMPLATES:
    template_engine['OPTIONS']['debug'] = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1jq7oz7z&swi1e&m9&+qies7!))e%yitvz=o)72dxk9(p@p&mv'

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
