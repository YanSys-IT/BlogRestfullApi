

import os
from datetime import timedelta
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)()a@%b$gz!!*-@3r&@wh$rh-a#&_%*ub92=arylggeew$g9x0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Сторонние приложения
    'rest_framework',
    'rest_framework_simplejwt',
    # Чтобы фронтенд мог общаться с бэкендом
    'corsheaders',

    'users',
    'posts',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Фильтр для CORS (должен быть первым)
    'django.middleware.security.SecurityMiddleware',  # Фильтр безопасности
    'django.contrib.sessions.middleware.SessionMiddleware',  # Работа с сессиями
    'django.middleware.common.CommonMiddleware',  # Общие настройки
    'django.middleware.csrf.CsrfViewMiddleware',  # Защита от CSRF-атак
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Проверка авторизации
    'django.contrib.messages.middleware.MessageMiddleware',  # Работа с сообщениями
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Защита от кликджекинга
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Папка для шаблонов
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Используем SQLite (простая файловая БД)
        'NAME': BASE_DIR / 'db.sqlite3',  # Файл БД будет в корне проекта
    }
}
AUTH_PASSWORD_VALIDATORS = [
    
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],

}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}  

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

AUTH_USER_MODEL = 'users.CustomUser'

# Where to redirect after login/logout
LOGIN_REDIRECT_URL = '/posts/'
LOGOUT_REDIRECT_URL = '/posts/'



