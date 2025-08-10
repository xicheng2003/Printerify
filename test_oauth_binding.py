#!/usr/bin/env python3
"""
OAuth账户绑定功能测试脚本
测试OAuth账户绑定的各种场景
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

User = get_user_model()

def test_oauth_binding_scenarios():
    """测试OAuth账户绑定的各种场景"""
    print("🧪 开始测试OAuth账户绑定功能...")
    
    # 创建测试客户端
    client = Client()
    
    # 场景1: 创建用户并绑定GitHub
    print("\n📋 场景1: 创建用户并绑定GitHub")
    try:
        # 创建测试用户
        user = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        print(f"✅ 创建用户成功: {user.username}")
        
        # 模拟用户登录
        client.force_login(user)
        print("✅ 用户登录成功")
        
        # 检查绑定状态
        response = client.get('/api/oauth/bindings/')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取绑定状态成功: {data}")
        else:
            print(f"❌ 获取绑定状态失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 场景1测试失败: {e}")
    
    # 场景2: 测试账户绑定逻辑
    print("\n📋 场景2: 测试账户绑定逻辑")
    try:
        # 创建另一个测试用户
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        print(f"✅ 创建用户2成功: {user2.username}")
        
        # 模拟用户2登录
        client.force_login(user2)
        print("✅ 用户2登录成功")
        
        # 测试绑定GitHub
        response = client.post('/api/oauth/bindings/github/')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 绑定GitHub请求成功: {data}")
        else:
            print(f"❌ 绑定GitHub请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 场景2测试失败: {e}")
    
    # 场景3: 测试OAuth服务逻辑
    print("\n📋 场景3: 测试OAuth服务逻辑")
    try:
        from api.services.oauth_service import OAuthService
        
        oauth_service = OAuthService()
        print("✅ OAuth服务初始化成功")
        
        # 测试用户查找逻辑
        user_info = {
            'provider': 'github',
            'id': '12345',
            'username': 'githubuser',
            'email': 'github@example.com',
            'github_id': '12345'
        }
        
        # 测试查找现有用户
        found_user = oauth_service.find_or_create_user(user_info)
        if found_user:
            print(f"✅ 用户查找/创建成功: {found_user.username}")
        else:
            print("❌ 用户查找/创建失败")
            
    except Exception as e:
        print(f"❌ 场景3测试失败: {e}")
    
    # 清理测试数据
    print("\n🧹 清理测试数据...")
    try:
        User.objects.filter(username__startswith='testuser').delete()
        print("✅ 测试数据清理完成")
    except Exception as e:
        print(f"❌ 数据清理失败: {e}")
    
    print("\n🎉 OAuth账户绑定功能测试完成！")

if __name__ == '__main__':
    test_oauth_binding_scenarios()
