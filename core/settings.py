
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
    # Для JWT-авторизации
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


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

# ПРОВЕРКИ ПАРОЛЕЙ (какие правила для паролей)
AUTH_PASSWORD_VALIDATORS = [
    # Пароль не должен быть похож на имя пользователя
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    # Минимальная длина пароля
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    # Запрещенные простые пароли
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    # Пароль не должен состоять только из цифр
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Папка для статических файлов в режиме разработки

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# МЕДИА-ФАЙЛЫ (загружаемые пользователями)
MEDIA_URL = '/media/'  # URL для доступа к загруженным файлам
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Папка для хранения загруженных файлов

# НАСТРОЙКИ DRF (Django REST Framework)
REST_FRAMEWORK = {
    # КАК ПРОВЕРЯТЬ АВТОРИЗАЦИЮ
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Используем JWT-токены
        'rest_framework.authentication.SessionAuthentication',  # Добавьте эту строку для сессий
    ),
    
    # КАКИЕ ПРАВА ДОСТУПА ПО УМОЛЧАНИЮ
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Чтение - всем, изменение - только авторизованным
    ],
    
    # КАК ДЕЛИТЬ НА СТРАНИЦЫ (пагинация)
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # 10 записей на страницу

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # Этот рендерер делает красивый интерфейс
    ],

}

# НАСТРОЙКИ JWT-ТОКЕНОВ
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # Access-токен живет 1 день
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Refresh-токен живет 7 дней
}  

# НАСТРОЙКИ CORS (Cross-Origin Resource Sharing)
# Разрешаем фронтенду на другом порту общаться с нашим бэкендом
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React/Vue.js приложение
    "http://127.0.0.1:3000",  # Альтернативный адрес
]

# Указываем Django использовать нашу кастомную модель пользователя
AUTH_USER_MODEL = 'users.CustomUser'

# Where to redirect after login/logout
LOGIN_REDIRECT_URL = '/posts/'
LOGOUT_REDIRECT_URL = '/posts/'



