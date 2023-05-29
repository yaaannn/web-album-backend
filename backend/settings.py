from datetime import timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
MY_APPS_DIR = BASE_DIR / "app"
UPLOAD_DIR = BASE_DIR / "media" / "upload"

DEBUG = True
SHOWSQL = True

# 数据库配置
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "album",
        "USER": "root",
        "PASSWORD": "heyan5201314",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}

# 日志配置
LOGGING = {
    "version": 1,  # 指明dictConfig的版本
    "disable_existing_loggers": False,  # 表示是否禁用所有的已经存在的日志配置
    "formatters": {  # 格式器
        "standard": {"format": "[%(asctime)s] %(message)s"},  # 标准
        "debug": {  # 调试
            "format": "[%(asctime)s] [%(process)d:%(thread)d] %(filename)s[line:%(lineno)d] (%(name)s)[%(levelname)s] %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "standard",
        },
        "debug_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "debug",
            "level": "DEBUG",
            "encoding": "utf8",
            "filename": "./log/debug.log",
            "mode": "w",
        },
        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "level": "INFO",
            "encoding": "utf8",
            "filename": "./log/info.log",
            "mode": "w",
        },
        "error_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "debug",
            "level": "ERROR",
            "encoding": "utf8",
            "filename": "./log/error.log",
            "mode": "w",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
    # 设置默认的root handle 用于将开发手动输出的日志输出到指定文件中
    "root": {
        "level": "DEBUG",
        "handlers": ["debug_file_handler", "info_file_handler", "error_file_handler"],
    },
}

# 密钥配置
SECRET_KEY = "django-insecure-z#6nawjbm$@&=rpy_m77xil=qz*k0+1#-!4sk-o#w*@v*5g$xg"

# 应用配置
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "app.user",
    "app.public",
    "app.album",
    "app.photo",
    "app.comment",
    "app.archive",
    "app.admin",
    "app.partition",
]

# 中间件配置
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "extension.middleware.cors.CorsMiddleware",  # 解决跨域中间件
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "extension.middleware.log.LogMiddleware",
]

# 根路由配置
ROOT_URLCONF = "backend.urls"

WSGI_APPLICATION = "backend.wsgi.application"

# 静态文件配置
STATIC_URL = "/static/"


# 默认主键配置
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# redis 配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "api": {
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
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    # DRF异常定制处理方法
    "EXCEPTION_HANDLER": "extension.exception_handle_ext.base_exception_handler",
    # 配置分页
    "DEFAULT_PAGINATION_CLASS": "extension.pagination_ext.Pagination",
    "PAGE_SIZE": 2,
}

# JWT 配置
JWT_SETTINGS = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),  # 指定token有效期
    "ALGORITHMS": ["HS256"],  # 指定加密的哈希函数
    "SIGNING_KEY": SECRET_KEY,  # jwt的密钥
    "VERIFY_SIGNATURE": True,  # 开启验证密钥
    "VERIFY_EXP": True,  # 开启验证token是否过期
    "REQUIRE": ["exp"],  # 指定token中必须要有的字段
    "AUTH_HEADER_TYPES": "Bearer",  # 指定请求头中的类型
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",  # 指定请求头的名称
}

# 密码加密配置
ENCODE_PASSWORD_SETTINGS = {
    "ALGORITHM": "pbkdf2_sha256",
    "SALT": "123456",
    "ITERATIONS": 100000,
}


# 邮件配置
# 如果不发送邮件，只让邮件显示在控制台中，设置下面这个环境变量
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
