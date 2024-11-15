"""
Django settings for django_workflow_items project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from decouple import config
import os
from datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True # 配置跨域,允许所有访问

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # Django REST Framework
    'rest_framework_simplejwt.token_blacklist',  # Simple JWT 的黑名单功能
    'corsheaders', # 跨域配置
    'storages',  # Django Storages
    'accounts', # 用户管理模块
    
]

# 设置Django AUTH 用户认证系统所需用户模型
# 格式: 子应用名.模型名  -- 必须在数据第一次迁移时配置完成
AUTH_USER_MODEL = "accounts.CustomUser"


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # 跨域配置中间件
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',  # 确保位于 CorsMiddleware 之后
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS 配置
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173/",  # Vue 前端开发地址
    # "https://your-production-domain.com",  # 生产环境前端地址
]

# CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'django_workflow_items.urls'

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

WSGI_APPLICATION = 'django_workflow_items.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            # 数据库连接高级选项
            # init_command 初始化连接时执行的 SQL 语句
            # STRICT_TRANS_TABLES 模式要求 MySQL 在插入无效数据时抛出错误，而不是进行数据截断
            'init_command':"SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4', # 指定数据库的字符集为 utf8mb4
            'connect_timeout': 10, # 连接超时(秒)
            'read_timeout': 30, # 读取超时(秒)
            'write_timeout': 30, # 写入超时(秒)
            'ssl': {'ssl-mode': 'DISABLED'},  # 禁用 SSL 验证
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Django REST Framework 配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # 使用 JWT 认证
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # 默认需要认证
    ],
}

# Simple JWT 配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # 访问令牌有效期
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # 刷新令牌有效期
    'ROTATE_REFRESH_TOKENS': True,  # 刷新令牌后轮换
    'BLACKLIST_AFTER_ROTATION': True,  # 刷新令牌轮换后加入黑名单

    'ALGORITHM': 'HS256', # 使用HS256签名算法
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',

    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    
    # 可选配置
    'JTI_CLAIM': 'jti',  # 默认的 JWT ID 声明
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',  # 滑动令牌刷新过期时间声明
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# 静态文件配置
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Azure Blob 容器 django-storages 配置
AZURE_ACCOUNT_NAME = 'p5datablob' # 存储账户名称
AZURE_CONTAINER = 'workflow-items' # 容器名称
AZURE_ACCOUNT_KEY = config('AZURE_ACCOUNT_KEY') # 存储账户密钥
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'

# 使用 Azure Blob Storage 作为默认文件存储后端
DEFAULT_AUTO_STORAGE = 'storages.backends.azure_storage.AzureStorage'

AZURE_SSL = True # 使用HTTPS

# 构建完整 MEDIA_URL
MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/'

# 雪花算法配置
SNOWFLAKE_WORKER_ID = 1 # 每个工作节点的唯一ID, 范围通常0-31
SNOWFLAKE_DATACENTER_ID = 1 # 每个数据中心唯一ID