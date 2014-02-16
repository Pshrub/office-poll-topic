## 
## This is the settings file that you use when you're working on the project locally. 
## Local development-specific settings include DEBUG mode, log level, and 
## activation of developer tools like django-debug-toolbar. 
##

# settings/local.py
from .base import *
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i@de#z&xhk6^v-9joseaxc55fq*s*x&-d#yg8hs^ii@%w74w)$'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'office_poll_topic',
        'USER': 'root',
        'PASSWORD': 'suse71OS!',
        'PORT': 3306,
        'HOST': 'localhost'
#        ),
    }
}

# EMAIL_HOST = "localhost"
# EMAIL_PORT = 1025

# }
# INSTALLED_APPS += ("debug_toolbar", )
# INTERNAL_IPS = ("127.0.0.1",)

# MIDDLEWARE_CLASSES += \
# ("debug_toolbar.middleware.DebugToolbarMiddleware", )

