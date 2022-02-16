"""
Django settings for church_app project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
from .myenv import get_envvars

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read environments variables in PROD
get_envvars(BASE_DIR / '.env', ignore_not_found_error=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-0ve2!lo58y1z89q)&&e=_dg!y$elr+rb+50h$nj(xmm(b&@%u)'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'background_task',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'church_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'church_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_NAME'),
        'USER': os.getenv('MYSQL_USER'),
        'PASSWORD': os.getenv('MYSQL_PASS'),
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# https://djbook.ru/rel1.9/topics/logging.html
# https://docs.djangoproject.com/en/4.0/howto/logging/#naming-loggers
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)-8s %(asctime)s module: %(module)s proc: %(process)d thread: %(thread)d\n         %(message)s',
            'datefmt': "%d.%b %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    # По умолчанию все сообщения, прошедшие проверку уровня логгирования, будут переданы в обработчик.
    # Добавив фильтры вы можете определить дополнительные правила проверки при обработке сообщений.
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # Как и логгеры, обработчики имеют уровень логгирования.
    # Если уровень логгирования сообщения ниже уровня логгирования обработчика, сообщение будет проигнорировано.
    # Логгер может содержать несколько обработчиков, которые могут иметь различный уровень логгирования.
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'django-file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(os.getenv('DJANGO_LOG_DIRECTORY', BASE_DIR), 'django.log'),
            'when': 'D',  # this specifies the interval
            'interval': 1,  # defaults to 1, only necessary for other values
            'backupCount': 10,  # how many backup file to keep, 10 days
            'formatter': 'verbose',
        },
        'church-app-file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(os.getenv('DJANGO_LOG_DIRECTORY', BASE_DIR), 'main.log'),
            'when': 'D',  # this specifies the interval
            'interval': 1,  # defaults to 1, only necessary for other values
            'backupCount': 10,  # how many backup file to keep, 10 days
            'formatter': 'verbose'
        },
        'church-app-jobs-file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(os.getenv('DJANGO_LOG_DIRECTORY', BASE_DIR), 'main-jobs.log'),
            'when': 'D',  # this specifies the interval
            'interval': 1,  # defaults to 1, only necessary for other values
            'backupCount': 10,  # how many backup file to keep, 10 days
            'formatter': 'verbose'
        },
    },
    # Когда сообщение передается в логгер, уровень логгирования сообщения сравнивается с уровнем логгирования логгера.
    # Если уровень логгирования сообщения равен или выше уровню логгирования логгера, сообщение будет обработано, иначе - проигнорировано.
    # После того, как логгер принял сообщение на обработку, оно передается в Handler(Обработчик).
    'loggers': {
        'django': {
            'handlers': ['django-file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'django.request': {
            'handlers': ['django-file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'main': {
            'handlers': ['church-app-file', 'console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'main.jobs': {
            'handlers': ['church-app-jobs-file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
