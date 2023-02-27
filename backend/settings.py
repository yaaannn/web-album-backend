"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from datetime import timedelta
from pathlib import Path

# environment
CURRENT_ENV = "dev"
if CURRENT_ENV == "dev":
    from config.dev.settings import *
else:
    from config.prod.settings import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MY_APPS_DIR = BASE_DIR / "app"
UPLOAD_DIR = BASE_DIR / "media" / "upload"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-z#6nawjbm$@&=rpy_m77xil=qz*k0+1#-!4sk-o#w*@v*5g$xg"

# os.uranomd(32).hex()
AES_KEY = "c453001319efc1fa5f38c2052e07cedb"

ALLOWED_HOSTS = []

# CORS settings
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
    "VIEW",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "app.user",
    "app.public",
    "app.album",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # 解决跨域中间件
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "extension.middleware_ext.LogMiddleware",
    "extension.middleware.log.LogMiddleware",
]

ROOT_URLCONF = "backend.urls"

# RuntimeError: You called this URL via POST, but the URL doesn't end in a slash and you have APPEND_SLASH set.
APPEND_SLASH = False

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
# # 指定文件目录，BASE_DIR指的是项目目录，static是指存放静态文件的目录。
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# 迁移静态文件的目录,这个是线上是需要使用的 python manage.py collectstatic
STATIC_ROOT = BASE_DIR / "static/static"

# 媒体文件位置
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# redis 配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "SERIALIZER": "django_redis.serializers.msgpack.MSGPackSerializer",
            # "PASSWORD": ""
        },
    },
    "redis_cli": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

# Django Rest Framework 配置
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_RENDERER_CLASSES": (
        "extension.render_response_ext.BaseJsonRenderer",  # 自定义返回格式
        # "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        # "drf_renderer_xlsx.renderers.XLSXRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    # 格式化时间
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DATETIME_INPUT_FORMATS": ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"),
    "DATE_FORMAT": "%Y-%m-%d",
    "DATE_INPUT_FORMATS": ("%Y-%m-%d",),
    "TIME_FORMAT": "%H:%M:%S",
    "TIME_INPUT_FORMATS": ("%H:%M:%S",),
    # DRF异常定制处理方法
    "EXCEPTION_HANDLER": "extension.exception_handle_ext.base_exception_handler",
    # 配置分页
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}

# JWT 配置
JWT_SETTINGS = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),  # 指定token有效期
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # 指定刷新token有效期
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHMS": ["HS256"],  # 指定加密的哈希函数
    "SIGNING_KEY": SECRET_KEY,  # jwt的密钥
    "VERIFY_SIGNATURE": True,  # 开启验证密钥
    "VERIFY_EXP": True,  # 开启验证token是否过期
    "AUDIENCE": None,
    "ISSUER": None,
    "LEEWAY": 0,
    "REQUIRE": ["exp"],
    "AUTH_HEADER_TYPES": "Bearer",
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
}

# 图像文件大小配置
IMAGE_FILE_SIZE = 1024 * 1024 * 64

# 图像文件格式限制
IMAGE_FORMAT = ["jpg", "jpeg", "png", "gif"]
IMAGE_FILE_CHECK = ("png", "jpg", "jpeg", "gif", "svg")

# 限制接口访问频率
MINUTE_HZ = 30

ENCODE_PASSWORD_SETTINGS = {
    "ALGORITHM": "pbkdf2_sha256",
    "SALT": "123456",
    "ITERATIONS": 100000,
}


# 邮件配置
# 如果不发送邮件，只让邮件显示在控制台中，设置下面这个环境变量
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "smtp.163.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = "heyanah@163.com"
EMAIL_HOST_PASSWORD = "OUNLZEPFWZXFPYKS"
EMAIL_USE_SSL = False

SERVER_NAME = ""
