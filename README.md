# Django PostgreSQL 项目

这是一个使用 Django 和 PostgreSQL 构建的后端项目，包含完整的权限管理系统和数据库连接池。

## 项目特性

- ✅ Django 5.2.7
- ✅ PostgreSQL 数据库
- ✅ 数据库连接池
- ✅ JWT 认证
- ✅ 自定义权限系统
- ✅ 角色管理
- ✅ RESTful API

## 项目结构

```
.
├── backend/                 # Django 项目配置
│   ├── settings.py         # 项目配置
│   ├── urls.py            # 主路由配置
│   └── ...
├── auth_app/               # 权限管理应用
│   ├── models.py          # 数据模型
│   ├── views.py           # API 视图
│   ├── permissions.py     # 权限类
│   ├── serializers.py     # 序列化器
│   ├── urls.py           # 应用路由
│   └── management/commands/
│       └── init_permissions.py  # 权限初始化命令
├── frontend/               # 前端项目
├── manage.py              # Django 管理脚本
├── .env.example           # 环境变量示例
└── README.md             # 项目文档
```

## 安装和配置

### 1. 安装依赖

```bash
# 安装 Python 依赖
pip install django psycopg2-binary django-db-connections-pool djangorestframework djangorestframework-simplejwt
```

### 2. 创建 Django 项目

```bash
# 创建 Django 项目（已在当前目录）
django-admin startproject backend .
```

### 3. 创建权限管理应用

```bash
# 创建 auth_app 应用
django-admin startapp auth_app
```

### 4. 配置数据库

确保 PostgreSQL 服务正在运行，然后创建数据库：

```sql
CREATE DATABASE ics_db;
```

### 5. 环境配置

复制环境变量文件并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置正确的数据库连接信息：

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here

# Database Settings
DB_NAME=ics_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### 6. 数据库迁移

```bash
# 创建数据库迁移文件
python manage.py makemigrations

# 应用数据库迁移
python manage.py migrate
```

### 7. 初始化权限数据

```bash
# 初始化权限和角色数据
python manage.py init_permissions
```

### 8. 创建超级用户

```bash
# 创建管理员账户
python manage.py createsuperuser
```

按照提示输入邮箱和密码。

## 运行项目

### 启动开发服务器

```bash
python manage.py runserver
```

服务器将在 http://127.0.0.1:8000 启动。

## API 文档

### 认证接口

#### 用户登录
- **URL**: `POST /api/auth/login/`
- **参数**:
  ```json
  {
    "email": "user@example.com",
    "password": "password"
  }
  ```
- **响应**:
  ```json
  {
    "access": "jwt_access_token",
    "refresh": "jwt_refresh_token",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "role": "admin",
      "is_active": true
    }
  }
  ```

#### 刷新令牌
- **URL**: `POST /api/auth/token/refresh/`
- **参数**:
  ```json
  {
    "refresh": "jwt_refresh_token"
  }
  ```

#### 用户登出
- **URL**: `POST /api/auth/logout/`
- **参数**:
  ```json
  {
    "refresh_token": "jwt_refresh_token"
  }
  ```

### 用户管理接口

#### 获取用户列表
- **URL**: `GET /api/auth/users/`
- **权限**: 仅管理员

#### 创建用户
- **URL**: `POST /api/auth/users/`
- **权限**: 仅管理员
- **参数**:
  ```json
  {
    "email": "newuser@example.com",
    "password": "password",
    "password_confirm": "password",
    "role": "user",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```

#### 获取用户详情
- **URL**: `GET /api/auth/users/{id}/`
- **权限**: 管理员或用户本人

#### 获取当前用户信息
- **URL**: `GET /api/auth/profile/`
- **权限**: 已认证用户

### 权限管理接口

#### 获取权限列表
- **URL**: `GET /api/auth/permissions/`
- **权限**: 仅管理员

#### 检查权限
- **URL**: `GET /api/auth/check-permission/{permission_code}/`
- **权限**: 已认证用户

#### 获取用户权限
- **URL**: `GET /api/auth/user-permissions/`
- **权限**: 已认证用户

## 权限系统

### 用户角色

- **admin**: 管理员，拥有所有权限
- **user**: 普通用户，可读写数据
- **viewer**: 只读用户，仅可查看数据

### 权限代码

- `user_read`: 用户读取权限
- `user_write`: 用户写入权限
- `user_delete`: 用户删除权限
- `data_read`: 数据读取权限
- `data_write`: 数据写入权限
- `data_delete`: 数据删除权限
- `system_config`: 系统配置权限

### 自定义权限类

- `IsAdmin`: 检查用户是否为管理员
- `IsOwnerOrAdmin`: 检查用户是否为对象所有者或管理员
- `HasPermission`: 检查用户是否具有特定权限
- `IsViewerReadOnly`: 只读用户权限检查

## 数据库连接池配置

项目使用 Django 内置的 `CONN_MAX_AGE` 配置数据库连接池：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'ics_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'CONN_MAX_AGE': 300,  # 连接池保持时间（秒）
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}
```

## 开发说明

### 添加新的权限

1. 在 `auth_app/permissions.py` 的 `PermissionCodes` 类中添加新的权限代码
2. 在 `auth_app/management/commands/init_permissions.py` 中添加权限定义
3. 运行 `python manage.py init_permissions` 初始化新权限

### 自定义权限使用

在视图类中使用自定义权限：

```python
from auth_app.permissions import IsAdmin, HasPermission, PermissionCodes

class MyView(APIView):
    permission_classes = [IsAdmin]  # 仅管理员可访问
    
class AnotherView(APIView):
    permission_classes = [HasPermission(PermissionCodes.DATA_WRITE)]  # 需要特定权限
```

## 部署说明

### 生产环境配置

1. 设置 `DEBUG=False`
2. 配置安全的 `SECRET_KEY`
3. 设置正确的数据库连接
4. 配置 `ALLOWED_HOSTS`
5. 配置静态文件服务

### Docker 部署

项目包含 `docker-compose.yml` 文件，可用于快速部署：

```bash
docker-compose up -d
```

## 故障排除

### 数据库连接问题

1. 确保 PostgreSQL 服务正在运行
2. 检查 `.env` 文件中的数据库配置
3. 验证数据库用户权限

### 权限初始化问题

1. 确保已运行数据库迁移
2. 检查 `init_permissions` 命令输出
3. 验证权限数据是否正确创建

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License
