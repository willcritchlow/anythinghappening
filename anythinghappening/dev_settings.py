from settings import *

DEBUG=True
TEMPLATE_DEBUG=DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'anythinghappening',
        'USER': 'django',
        'PASSWORD': 'hard57pass',
        'HOST': '',
        'PORT': '',
    }
}
