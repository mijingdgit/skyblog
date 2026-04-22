"""
Django settings for SkyBlog backend project.
"""

from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


def csv_config(name: str, default: str = "") -> list[str]:
    """Read comma-separated environment values while ignoring empty items."""
    raw_value = config(f"SKYBLOG_{name}", default=default)
    return [item.strip() for item in raw_value.split(",") if item.strip()]


def bool_config(name: str, default: bool = False) -> bool:
    raw_value = config(f"SKYBLOG_{name}", default=str(default))
    if isinstance(raw_value, bool):
        return raw_value

    value = str(raw_value).strip().lower()
    if value in {"1", "true", "yes", "on", "dev", "development", "local"}:
        return True
    if value in {"0", "false", "no", "off", "prod", "production", "release"}:
        return False
    return default


def int_config(name: str, default: int) -> int:
    raw_value = config(f"SKYBLOG_{name}", default=str(default))
    try:
        return int(raw_value)
    except (TypeError, ValueError):
        return default


def path_config(name: str, default: str) -> Path:
    raw_value = config(f"SKYBLOG_{name}", default=default)
    path = Path(raw_value)
    return path if path.is_absolute() else BASE_DIR / path


SECRET_KEY = config("SKYBLOG_SECRET_KEY", default="django-insecure-skyblog-dev-key-change-in-production")

DEBUG = bool_config("DEBUG", default=True)

ALLOWED_HOSTS = csv_config("ALLOWED_HOSTS", "localhost,127.0.0.1")

SITE_URL = config("SKYBLOG_SITE_URL", default="http://127.0.0.1:5173").rstrip("/")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'users',
    'articles',
    'projects',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'skyblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'skyblog.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

STATIC_URL = config("SKYBLOG_STATIC_URL", default="/static/")
STATIC_ROOT = path_config("STATIC_ROOT", "staticfiles")
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = config("SKYBLOG_MEDIA_URL", default="/media/")
MEDIA_ROOT = path_config("MEDIA_ROOT", "media")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS / CSRF
DEV_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174"
CORS_ALLOWED_ORIGINS = csv_config("CORS_ALLOWED_ORIGINS", DEV_ORIGINS)
CORS_ALLOW_CREDENTIALS = bool_config("CORS_ALLOW_CREDENTIALS", default=True)
CSRF_TRUSTED_ORIGINS = csv_config("CSRF_TRUSTED_ORIGINS", DEV_ORIGINS)
CSRF_COOKIE_SAMESITE = config("SKYBLOG_CSRF_COOKIE_SAMESITE", default="Lax")
SESSION_COOKIE_SAMESITE = config("SKYBLOG_SESSION_COOKIE_SAMESITE", default="Lax")

# Production security toggles. Keep these disabled locally and enable them behind HTTPS.
SECURE_SSL_REDIRECT = bool_config("SECURE_SSL_REDIRECT", default=False)
SESSION_COOKIE_SECURE = bool_config("SESSION_COOKIE_SECURE", default=not DEBUG)
CSRF_COOKIE_SECURE = bool_config("CSRF_COOKIE_SECURE", default=not DEBUG)
SECURE_PROXY_SSL_HEADER = (
    ("HTTP_X_FORWARDED_PROTO", "https")
    if bool_config("USE_X_FORWARDED_PROTO", default=False)
    else None
)
SECURE_HSTS_SECONDS = int_config("SECURE_HSTS_SECONDS", default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = bool_config("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False)
SECURE_HSTS_PRELOAD = bool_config("SECURE_HSTS_PRELOAD", default=False)
SECURE_CONTENT_TYPE_NOSNIFF = bool_config("SECURE_CONTENT_TYPE_NOSNIFF", default=True)
SECURE_REFERRER_POLICY = config("SKYBLOG_SECURE_REFERRER_POLICY", default="same-origin")
SECURE_CROSS_ORIGIN_OPENER_POLICY = config(
    "SKYBLOG_SECURE_CROSS_ORIGIN_OPENER_POLICY",
    default="same-origin",
)
X_FRAME_OPTIONS = config("SKYBLOG_X_FRAME_OPTIONS", default="DENY")
SESSION_COOKIE_HTTPONLY = bool_config("SESSION_COOKIE_HTTPONLY", default=True)

# Upload limits protect the Django process from oversized form submissions.
DATA_UPLOAD_MAX_MEMORY_SIZE = int_config("DATA_UPLOAD_MAX_MEMORY_SIZE", default=20 * 1024 * 1024)
FILE_UPLOAD_MAX_MEMORY_SIZE = int_config("FILE_UPLOAD_MAX_MEMORY_SIZE", default=10 * 1024 * 1024)

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# 自定义用户模型
AUTH_USER_MODEL = 'users.User'
