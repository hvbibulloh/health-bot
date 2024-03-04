from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-khla#*j1xe$p=1d#2&_h80@f9ak7prn5inc#k2jcq1pq*@67^%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'health'
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

ROOT_URLCONF = 'sozlamalar.urls'

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

WSGI_APPLICATION = 'sozlamalar.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lines_db',
        'USER': 'postgres',
        'PASSWORD': '1',
        'HOST': 'localhost',
        'PORT': 5432
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

LANGUAGE_CODE = 'uz-uz'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
import os

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
# STATICFILES_DIRS = [BASE_DIR / 'static']

import os

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    "site_title": "Health",

    "site_header": "Health",

    "site_brand": "Health",

    "site_logo": None,

    "login_logo": None,

    "login_logo_dark": None,

    "site_logo_classes": "img-circle",

    "site_icon": None,

    "welcome_sign": "Welcome to the Yec",

    "copyright": "Health MCHJ",

    "search_model": ['auth.User', 'health.User', 'health.Vakansiya', 'health.VakansiyaRU'],

    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index",
         "permissions": ["auth.view_user"]},

        {"name": "Support", "url": "https://t.me/hvbibulloh", "new_window": True},

        {"model": "auth.User"},

        {"app": "health"},
    ],

    "usermenu_links": [
        {"name": "Support", "url": "https://t.me/hvbibulloh", "new_window": True},
        {"model": "auth.user"},
    ],

    "show_sidebar": True,

    "navigation_expanded": True,

    "hide_apps": [],

    "hide_models": ['auth.Group'],

    "order_with_respect_to": ["auth", "books", "books.author", "books.book"],

    "custom_links": {
        "books": [{
            "name": "Make Messages",
            "url": "make_messages",
            "icon": "fas fa-comments",
            "permissions": ["books.view_book"]
        }]
    },

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "products.Product": "fas fa-cube",
        "products.Category": 'fas fa-tags',
        "products.Subcategory": 'fas fa-folder-open'
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    "related_modal_active": False,
    "show_ui_builder": False,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,

    "changeform_format": "vertical_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "health.Vakansiya": "vertical_tabs"},
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "simplex",
    "light_mode_theme": "light",
}
