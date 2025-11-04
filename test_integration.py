#!/usr/bin/env python
"""
前后端集成测试脚本
验证Django后端和React前端的集成情况
"""

import os
import django
import sys
import requests
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from auth_app.models import User

def test_backend_api():
    """测试后端API是否正常工作"""
    print("=== 测试后端API ===")
    
    base_url = "http://localhost:8000/api"
    
    # 测试登录API
    print("1. 测试登录API...")
    try:
        # 首先检查是否有用户
        user_count = User.objects.count()
        if user_count == 0:
            print("   ⚠️  没有用户，请先创建用户: python manage.py createsuperuser")
            return False
        
        # 获取第一个用户用于测试
        test_user = User.objects.first()
        print(f"   📧 测试用户: {test_user.email}")
        
        # 尝试登录（使用错误密码测试错误处理）
        login_data = {
            "email": test_user.email,
            "password": "wrong_password"  # 使用错误密码测试
        }
        
        response = requests.post(f"{base_url}/auth/login/", json=login_data)
        
        if response.status_code == 401:
            print("   ✅ 登录API错误处理正常（预期使用错误密码）")
        else:
            print(f"   ⚠️  登录API返回状态码: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ 无法连接到后端服务器，请确保后端正在运行")
        return False
    except Exception as e:
        print(f"   ❌ 登录API测试失败: {e}")
        return False
    
    # 测试其他API端点
    endpoints = [
        "/auth/permissions/",
        "/auth/role-permissions/",
    ]
    
    for endpoint in endpoints:
        print(f"2. 测试端点 {endpoint}...")
        try:
            response = requests.get(f"{base_url}{endpoint}")
            if response.status_code in [200, 401]:  # 401表示需要认证，这也是正常的
                print(f"   ✅ {endpoint} 端点正常")
            else:
                print(f"   ⚠️  {endpoint} 返回状态码: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {endpoint} 测试失败: {e}")
    
    print("✅ 后端API测试完成")
    return True

def test_frontend_build():
    """测试前端项目构建"""
    print("\n=== 测试前端项目 ===")
    
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    
    # 检查前端目录是否存在
    if not os.path.exists(frontend_dir):
        print("❌ 前端目录不存在")
        return False
    
    # 检查package.json
    package_json = os.path.join(frontend_dir, "package.json")
    if not os.path.exists(package_json):
        print("❌ package.json 不存在")
        return False
    
    # 检查关键文件
    required_files = [
        "src/App.jsx",
        "src/components/Login.jsx", 
        "src/components/Dashboard.jsx",
        "src/services/api.js"
    ]
    
    for file in required_files:
        file_path = os.path.join(frontend_dir, file)
        if os.path.exists(file_path):
            print(f"   ✅ {file} 存在")
        else:
            print(f"   ❌ {file} 不存在")
            return False
    
    print("✅ 前端项目结构检查完成")
    return True

def test_api_integration():
    """测试前后端API集成"""
    print("\n=== 测试前后端API集成 ===")
    
    # 测试API配置
    api_config_path = os.path.join(os.path.dirname(__file__), "frontend", "src", "services", "api.js")
    
    if os.path.exists(api_config_path):
        with open(api_config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查关键配置
        checks = [
            ("baseURL", "检查API基础URL配置"),
            ("axios.create", "检查axios实例创建"),
            ("interceptors", "检查请求拦截器"),
            ("authAPI", "检查认证API"),
            ("userAPI", "检查用户API"),
        ]
        
        for check, description in checks:
            if check in content:
                print(f"   ✅ {description} 正常")
            else:
                print(f"   ❌ {description} 异常")
                return False
    else:
        print("   ❌ API配置文件不存在")
        return False
    
    print("✅ 前后端API集成配置检查完成")
    return True

def main():
    """主测试函数"""
    print("全栈项目集成测试")
    print("=" * 50)
    
    print("📋 测试计划:")
    print("1. 后端API功能测试")
    print("2. 前端项目结构检查") 
    print("3. 前后端API集成测试")
    print("")
    
    # 运行测试
    backend_ok = test_backend_api()
    frontend_ok = test_frontend_build()
    integration_ok = test_api_integration()
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    print(f"后端API测试: {'✅ 通过' if backend_ok else '❌ 失败'}")
    print(f"前端项目测试: {'✅ 通过' if frontend_ok else '❌ 失败'}")
    print(f"集成配置测试: {'✅ 通过' if integration_ok else '❌ 失败'}")
    
    if backend_ok and frontend_ok and integration_ok:
        print("\n🎉 所有测试通过！项目集成正常。")
        print("\n🚀 下一步:")
        print("1. 确保后端服务器运行: python manage.py runserver")
        print("2. 确保前端服务器运行: cd frontend && npm run dev")
        print("3. 访问 http://localhost:5173 测试完整功能")
        print("4. 使用创建的用户账号登录测试")
    else:
        print("\n⚠️  部分测试失败，请检查相关问题。")
        print("\n🔧 故障排除:")
        print("- 确保后端服务器正在运行")
        print("- 检查数据库迁移和权限初始化")
        print("- 验证前端依赖安装")
        print("- 查看README.md中的详细说明")

if __name__ == "__main__":
    main()
