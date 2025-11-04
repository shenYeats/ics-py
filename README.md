# 全栈项目 - Django + React

这是一个完整的全栈项目，包含 Django 后端和 React 前端，支持 PostgreSQL 数据库、权限管理系统和现代化的用户界面。

## 项目特性

### 后端特性
- ✅ Django 5.2.7
- ✅ PostgreSQL 数据库
- ✅ 数据库连接池
- ✅ JWT 认证
- ✅ 自定义权限系统
- ✅ 角色管理
- ✅ RESTful API

### 前端特性
- ✅ React 18 + Vite
- ✅ Material-UI (MUI) 组件库
- ✅ 响应式设计
- ✅ JWT 认证集成
- ✅ 现代化用户界面
- ✅ 前后端完全分离

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
├── frontend/               # React 前端项目
│   ├── src/
│   │   ├── components/     # React 组件
│   │   │   ├── Login.jsx  # 登录页面
│   │   │   └── Dashboard.jsx  # 仪表板
│   │   ├── services/      # API 服务
│   │   │   └── api.js     # 前后端交互接口
│   │   └── App.jsx        # 主应用组件
│   ├── package.json       # 前端依赖配置
│   └── vite.config.js     # Vite 配置
├── manage.py              # Django 管理脚本
├── .env.example           # 环境变量示例
└── README.md             # 项目文档
```

## 后端安装和配置

### 1. 安装后端依赖

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

## 前端安装和配置

### 1. 创建 React 项目

```bash
# 使用 Vite 创建 React 项目
npx create-vite frontend --template react
```

### 2. 安装前端依赖

```bash
# 进入前端目录
cd frontend

# 安装 Material-UI 和 axios
npm install @mui/material @emotion/react @emotion/styled @mui/icons-material axios
```

### 3. 启动前端开发服务器

```bash
# 开发模式启动
npm run dev
```

前端服务器将在 http://localhost:5173 启动。

## 运行项目

### 启动后端服务器

```bash
# 在后端目录中
python manage.py runserver
```

后端服务器将在 http://127.0.0.1:8000 启动。

### 启动前端服务器

```bash
# 在前端目录中
npm run dev
```

前端服务器将在 http://localhost:5173 启动。

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

## 前端功能

### 主要组件

- **Login**: 用户登录页面，支持邮箱密码认证
- **Dashboard**: 登录后的主仪表板，显示用户信息和系统功能
- **API Service**: 完整的 RESTful API 交互服务

### 前端特性

- **Material-UI 设计**: 使用 Material Design 设计语言
- **响应式布局**: 适配桌面和移动设备
- **JWT 认证**: 自动处理 token 刷新和过期
- **状态管理**: 使用 React Hooks 管理应用状态
- **错误处理**: 完善的错误提示和处理机制

### 前后端交互

前端通过 `src/services/api.js` 与后端进行通信，包含：

- **认证 API**: 登录、登出、token 刷新
- **用户管理 API**: 用户列表、详情、创建、更新、删除
- **权限管理 API**: 权限列表、角色权限管理

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

### 后端开发

#### 添加新的权限

1. 在 `auth_app/permissions.py` 的 `PermissionCodes` 类中添加新的权限代码
2. 在 `auth_app/management/commands/init_permissions.py` 中添加权限定义
3. 运行 `python manage.py init_permissions` 初始化新权限

#### 自定义权限使用

在视图类中使用自定义权限：

```python
from auth_app.permissions import IsAdmin, HasPermission, PermissionCodes

class MyView(APIView):
    permission_classes = [IsAdmin]  # 仅管理员可访问
    
class AnotherView(APIView):
    permission_classes = [HasPermission(PermissionCodes.DATA_WRITE)]  # 需要特定权限
```

### 前端开发

#### 添加新的 API 接口

在 `frontend/src/services/api.js` 中添加新的 API 方法：

```javascript
export const newAPI = {
  getData: () => api.get('/api/new-endpoint/'),
  createData: (data) => api.post('/api/new-endpoint/', data),
};
```

#### 创建新的组件

在 `frontend/src/components/` 目录中创建新的 React 组件：

```javascript
import React from 'react';
import { Button, Typography } from '@mui/material';

const NewComponent = ({ data }) => {
  return (
    <div>
      <Typography variant="h6">新组件</Typography>
      <Button variant="contained">操作按钮</Button>
    </div>
  );
};

export default NewComponent;
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

### 后端问题

#### 数据库连接问题

1. 确保 PostgreSQL 服务正在运行
2. 检查 `.env` 文件中的数据库配置
3. 验证数据库用户权限

#### 权限初始化问题

1. 确保已运行数据库迁移
2. 检查 `init_permissions` 命令输出
3. 验证权限数据是否正确创建

### 前端问题

#### 依赖安装问题

1. 确保 Node.js 版本 >= 16
2. 删除 `node_modules` 和 `package-lock.json` 后重新安装
3. 检查网络连接是否正常

#### API 连接问题

1. 确保后端服务器正在运行
2. 检查 `frontend/src/services/api.js` 中的 baseURL 配置
3. 查看浏览器控制台错误信息

#### CORS 问题

如果遇到跨域问题，需要在 Django 设置中添加：

```python
# backend/settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

并安装 `django-cors-headers` 包。

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License
