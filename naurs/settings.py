from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # added application
    'widget_tweaks',
    'tinymce',
    'stripe',
    'account.apps.AccountConfig', # to handle authentication and user logics
    'home.apps.HomeConfig', # to handle home page contents and functionality
    'program.apps.ProgramConfig', # to handle program page contents and functionality
    'about.apps.AboutConfig', # to handle about page contents and functionality
    'contact.apps.ContactConfig', # to handle contact page contents and functionality
    'dashboard.apps.DashboardConfig', # to handle dashboard page contents and functionality
    'offer.apps.OfferConfig', # to handle offer page contents and functionality
    'instructor.apps.InstructorConfig', # to handle instructor page contents and functionality
    'student.apps.StudentConfig', # to handle student page contents and functionality
    'finance.apps.FinanceConfig', # to handle finance page contents and functionality
]

# custom authentication user model
AUTH_USER_MODEL = 'account.User'

#authentication backends
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'naurs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path.joinpath(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'home.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'naurs.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'naursdb',
    #     'USER': 'naursdbadmin',
    #     'PASSWORD': 'Naurs2022Admin',
    #     'HOST': 'Naurs-2672.postgres.pythonanywhere-services.com',
    #     'PORT': 12672,
    # }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/assets/'
STATIC_ROOT = Path.joinpath(BASE_DIR, 'assets')
STATICFILES_DIRS = [Path.joinpath(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = Path.joinpath(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# defining email host
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'naursfitnessandart@gmail.com'
EMAIL_HOST_PASSWORD = 'frgddpydlmvvruvw' # private app password to use for gmail emailing
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL='(Naurs) Naurs Support <no-reply@naurs.me>' 