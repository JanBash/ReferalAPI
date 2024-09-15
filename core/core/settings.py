from datetime import timedelta
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(pe158a2%ws9r+*^cu2%4hblfs$8+l#q1f9g@!$3$9&zg-^-yp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'mozilla_django_oidc',

    # Swagger
    'drf_yasg',
    
    # DRF Apps
    'rest_framework',
    'django_filters',
    
    #Custom Apps
    'user'
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'refer',  # Имя вашей базы данных
        'USER': 'janbash',      # Имя вашего пользователя
        'PASSWORD': '152020',  # Ваш пароль
        'HOST': 'db',   # Хост, на котором работает PostgreSQLos.path.join(BASE_DIR, 'templates')
        'PORT': '5432',            # Порт (по умолчанию 5432)
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'user.MyUser'

# Настройка срока действия Access Token и Refresh Token
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Продолжительность жизни Access Token
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),  # Продолжительность жизни Refresh Token при его использовании
    'SLIDING_TOKEN_LIFETIME': timedelta(days=7),  # Продолжительность жизни Refresh Token
    'SLIDING_TOKEN_REFRESH_REUSE_ALLOWS_REFRESH': False,  # Разрешить повторное использование Refresh Token для обновления
    'SLIDING_TOKEN_REFRESH_REUSE_RESETS': True,  # Сбрасывать Refresh Token после успешного обновления
    'ROTATE_REFRESH_TOKENS': False,  # Вращать Refresh Token (если True, предыдущий Refresh Token становится недействительным после обновления)
    'ALGORITHM': 'HS256',  # Алгоритм подписи токенов
    'SIGNING_KEY': 'your-signing-key',
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': 'http://keycloak:8080/realms/Django_Keycloak',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}


AUTHENTICATION_BACKENDS = (
    'core.auth.MyOIDCAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Применение настроек в DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

OIDC_RP_SIGN_ALGO = 'RS256'

# Настройки OIDC
OIDC_RP_CLIENT_ID = 'django-client'
OIDC_RP_CLIENT_SECRET = 'rcAYuVMHEC2fRxHeJ1J4Vyt6aUJKKFTB'
OIDC_OP_JWKS_ENDPOINT = 'http://kubernetes.docker.internal:8080/realms/Django_Keycloak/protocol/openid-connect/certs'
OIDC_OP_AUTHORIZATION_ENDPOINT = 'http://kubernetes.docker.internal:8080/realms/Django_Keycloak/protocol/openid-connect/auth'
OIDC_OP_TOKEN_ENDPOINT = 'http://kubernetes.docker.internal:8080/realms/Django_Keycloak/protocol/openid-connect/token'
OIDC_OP_USER_ENDPOINT = 'http://kubernetes.docker.internal:8080/realms/Django_Keycloak/protocol/openid-connect/userinfo'
OIDC_OP_LOGOUT_ENDPOINT = 'http://kubernetes.docker.internal:8080/realms/Django_Keycloak/protocol/openid-connect/logout'

# Логин и логаут
LOGIN_URL = '/oidc/authenticate/'
LOGOUT_URL = '/oidc/logout/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

OIDC_STORE_ID_TOKEN = True
OIDC_STORE_ACCESS_TOKEN = True
ALLOW_LOGOUT_GET_METHOD = True

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sakirovzanbolot48@gmail.com' # <-- You can change email instance here
EMAIL_HOST_PASSWORD = 'obco otih izyc lzqu ' # <-- Code from Google
