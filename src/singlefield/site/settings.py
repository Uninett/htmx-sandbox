from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
SITE_DIR = Path(__file__).resolve().parent
BASE_DIR = SITE_DIR.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r)3+$(zwl3yl_=wlnk$&jvk=5y=f9w*t(fx1c1(s9ev*tz%_hx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # Django's included apps
    'django.contrib.staticfiles',
    'django.forms',

    # 3rd party Django apps
    'debug_toolbar',

    # Our stuff
    'singlefield.app',
]

ROOT_URLCONF = 'singlefield.site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [SITE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'singlefield.site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Minimal middleware

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
]

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}

# For django-debug-toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html

STATIC_URL = "static/"

INTERNAL_IPS = [
    '127.0.0.1',
]

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
