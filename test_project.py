#!/usr/bin/env python
"""
项目功能测试脚本
用于验证Django项目的基本功能
"""

import os
import django
import sys

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from auth_app.models import User, Permission, RolePermission
from auth_app.permissions import PermissionCodes

def test_models():
    """测试数据模型"""
    print("=== 测试数据模型 ===")
    
    # 测试权限模型
    permissions = Permission.objects.all()
    print(f"权限数量: {permissions.count()}")
    for perm in permissions:
        print(f"  - {perm.name} ({perm.code})")
    
    # 测试角色权限
    role_perms = RolePermission.objects.all()
    print(f"角色权限数量: {role_perms.count()}")
    for rp in role_perms:
        print(f"  - {rp.role} -> {rp.permission.name}")
    
    print()

def test_user_creation():
    """测试用户创建"""
    print("=== 测试用户创建 ===")
    
    # 检查是否已有用户
    user_count = User.objects.count()
    print(f"当前用户数量: {user_count}")
    
    if user_count == 0:
        print("请先创建超级用户: python manage.py createsuperuser")
    else:
        users = User.objects.all()
        for user in users:
            print(f"  - {user.email} (角色: {user.role})")
    
    print()

def test_permission_system():
    """测试权限系统"""
    print("=== 测试权限系统 ===")
    
    # 检查权限代码
    print("预定义权限代码:")
    for attr in dir(PermissionCodes):
        if not attr.startswith('_'):
            value = getattr(PermissionCodes, attr)
            print(f"  - {attr}: {value}")
    
    print()

def test_api_endpoints():
    """测试API端点"""
    print("=== 测试API端点 ===")
    print("可用的API端点:")
    print("  - POST /api/auth/login/ - 用户登录")
    print("  - POST /api/auth/logout/ - 用户登出")
    print("  - POST /api/auth/token/refresh/ - 刷新令牌")
    print("  - GET /api/auth/users/ - 用户列表 (需要管理员权限)")
    print("  - GET /api/auth/profile/ - 当前用户信息")
    print("  - GET /api/auth/permissions/ - 权限列表 (需要管理员权限)")
    print("  - GET /api/auth/check-permission/{code}/ - 检查权限")
    print("  - GET /api/auth/user-permissions/ - 获取用户权限")
    print()

def main():
    """主测试函数"""
    print("Django PostgreSQL 项目功能测试")
    print("=" * 50)
    
    try:
        test_models()
        test_user_creation()
        test_permission_system()
        test_api_endpoints()
        
        print("✅ 项目功能测试完成！")
        print("\n下一步:")
        print("1. 启动服务器: python manage.py runserver")
        print("2. 访问 http://127.0.0.1:8000/api/auth/ 测试API")
        print("3. 使用Postman或curl测试认证接口")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        print("请确保已运行数据库迁移和权限初始化")

if __name__ == "__main__":
    main()
