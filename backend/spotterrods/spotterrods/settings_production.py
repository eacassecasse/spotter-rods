import json
import dj_database_url
from datetime import timedelta
from . import ENV

SECRET_KEY = ENV.get('DRF_SECRET_KEY')
DEBUG = bool(ENV.get('DRF_DEBUG')) == 'False'
ALLOWED_HOSTS = json.loads(ENV.get('DRF_ALLOWED_HOSTS', []))
SESSION_COOKIE_SECURE = bool(ENV.get('DRF_SESSION_COOKIE_SECURE'))
CSRF_COOKIE_SECURE = bool(ENV.get('DRF_CSRF_COOKIE_SECURE'))
SESSION_COOKIE_DOMAIN = ENV.get('DRF_SESSION_COOKIE_DOMAIN')
CSRF_COOKIE_DOMAIN = ENV.get('DRF_CSRF_COOKIE_DOMAIN')
SESSION_COOKIE_SAMESITE = ENV.get('DRF_SESSION_COOKIE_SAMESITE')
CSRF_COOKIE_SAMESITE = ENV.get('DRF_CSRF_COOKIE_SAMESITE')
SESSION_COOKIE_HTTPONLY = bool(ENV.get('DRF_SESSION_COOKIE_HTTPONLY'))
CSRF_COOKIE_HTTPONLY = bool(ENV.get('DRF_CSRF_COOKIE_HTTPONLY'))
SECURE_HSTS_SECONDS = int(ENV.get('DRF_SECURE_HSTS_SECONDS'))
SECURE_HSTS_PRELOAD = bool(ENV.get('DRF_SECURE_HSTS_PRELOAD'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = bool(ENV.get('DRF_SECURE_HSTS_INCLUDE_SUBDOMAINS'))
SECURE_SSL_REDIRECT = bool(ENV.get('DRF_SECURE_SSL_REDIRECT'))
CORS_ALLOWED_ORIGINS = json.loads(ENV.get('DRF_CORS_ALLOWED_ORIGINS', []))
CORS_EXPOSE_HEADERS = json.loads(ENV.get('DRF_CORS_EXPOSE_HEADERS', []))
CORS_ALLOW_CREDENTIALS = bool(ENV.get('DRF_CORS_ALLOW_CREDENTIALS'))
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

print(CORS_ALLOWED_ORIGINS)
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'django_seed',
    'corsheaders',
    'rest_framework',
    'drf_spectacular',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'core.apps.CoreConfig',
    'fleet.apps.FleetConfig',
    'users.apps.UsersConfig',
    'compliance.apps.ComplianceConfig',
    'shipping.apps.ShippingConfig',
    'logs.apps.LogsConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'spotterrods.urls'

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

WSGI_APPLICATION = 'spotterrods.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.parse(
        ENV.get('DATABASE_URL', '')
    )
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKEND = [
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Default permission
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

SPECTACULAR_SETTINGS = {
    'AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,  
    },
}

JWT_CONFIG = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(ENV.get('DRF_ACCESS_TOKEN_LIFETIME'))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(ENV.get('DRF_REFRESH_TOKEN_LIFETIME'))),
    'ROTATE_REFRESH_TOKENS': bool(ENV.get('DRF_ROTATE_REFRESH_TOKENS')),
    'BLACKLIST_AFTER_ROTATION': bool(ENV.get('DRF_BLACKLIST_AFTER_ROTATION')),
    'AUTH_HEADER_TYPES': (ENV.get('DRF_AUTH_HEADER_TYPES')),
    'AUTH_COOKIE': ENV.get('DRF_AUTH_COOKIE'),
    'AUTH_COOKIE_DOMAIN': ENV.get('DRF_AUTH_COOKIE_DOMAIN'),
    'AUTH_COOKIE_SECURE': bool(ENV.get('DRF_AUTH_COOKIE_SECURE')),
    'AUTH_COOKIE_HTTP_ONLY': bool(ENV.get('DRF_AUTH_COOKIE_HTTP_ONLY')),
    'AUTH_COOKIE_SAMESITE': ENV.get('DRF_AUTH_COOKIE_SAMESITE')
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": ENV.get('DRF_UPSTASH_REDIS_URL'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'SSL': True,
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'IGNORE_EXCEPTIONS': True,
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 20,
                'retry_on_timeout': True,
            }
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
