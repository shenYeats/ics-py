"""
Django settings for backend project with SQLite for testing.
"""

from .settings import *

# 使用 SQLite 数据库进行测试
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 移除数据库连接池配置
DATABASE_POOL_ARGS = {}
