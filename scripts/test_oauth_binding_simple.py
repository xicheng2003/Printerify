#!/usr/bin/env python3
"""
简单的OAuth绑定功能测试
用于验证OAuth账户绑定的基本逻辑
"""

import os
import sys
import django
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from api.services.oauth_service import OAuthService

User = get_user_model()

def test_oauth_binding_logic():
    """测试OAuth绑定逻辑"""
    print("🧪 测试OAuth绑定逻辑...")
    print("=" * 50)
    
    # 创建OAuth服务实例
    oauth_service = OAuthService()
    print("✅ OAuth服务创建成功")
    
    # 模拟用户信息
    github_user_info = {
        'provider': 'github',
        'id': '12345',
        'username': 'testuser',
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'avatar_url': 'https://example.com/avatar.jpg',
        'github_id': '12345',
        'extra_data': {}
    }
    
    google_user_info = {
        'provider': 'google',
        'id': '67890',
        'username': 'testuser',
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'avatar_url': 'https://example.com/avatar.jpg',
        'google_id': '67890',
        'extra_data': {}
    }
    
    print("✅ 模拟用户信息创建成功")
    
    # 测试用户查找逻辑
    print("\n🔍 测试用户查找逻辑...")
    
    # 清理测试用户（如果存在）
    User.objects.filter(username='testuser').delete()
    print("✅ 清理了旧的测试用户")
    
    # 测试创建新用户
    try:
        user = oauth_service.find_or_create_user(github_user_info)
        if user:
            print(f"✅ 成功创建用户: {user.username}")
            print(f"  - GitHub ID: {user.github_id}")
            print(f"  - Google ID: {user.google_id}")
        else:
            print("❌ 用户创建失败")
            return
    except Exception as e:
        print(f"❌ 用户创建异常: {e}")
        return
    
    # 测试绑定Google账户到现有用户
    print("\n🔗 测试绑定Google账户...")
    
    # 模拟已认证的请求
    class MockRequest:
        def __init__(self, user):
            self.user = user
        
        @property
        def user(self):
            return self._user
        
        @user.setter
        def user(self, value):
            self._user = value
        
        @property
        def is_authenticated(self):
            return self.user is not None
    
    mock_request = MockRequest(user)
    
    try:
        # 尝试绑定Google账户
        bound_user = oauth_service.find_or_create_user(google_user_info, mock_request)
        if bound_user and bound_user.id == user.id:
            print("✅ 成功绑定Google账户到现有用户")
            print(f"  - 用户ID: {bound_user.id}")
            print(f"  - GitHub ID: {bound_user.github_id}")
            print(f"  - Google ID: {bound_user.google_id}")
        else:
            print("❌ Google账户绑定失败")
    except Exception as e:
        print(f"❌ Google账户绑定异常: {e}")
    
    # 测试通过Google ID查找用户
    print("\n🔍 测试通过Google ID查找用户...")
    try:
        google_user = User.objects.filter(google_id='67890').first()
        if google_user and google_user.id == user.id:
            print("✅ 通过Google ID成功找到用户")
            print(f"  - 用户ID: {google_user.id}")
            print(f"  - 用户名: {google_user.username}")
        else:
            print("❌ 通过Google ID查找用户失败")
    except Exception as e:
        print(f"❌ 查找用户异常: {e}")
    
    # 测试通过GitHub ID查找用户
    print("\n🔍 测试通过GitHub ID查找用户...")
    try:
        github_user = User.objects.filter(github_id='12345').first()
        if github_user and github_user.id == user.id:
            print("✅ 通过GitHub ID成功找到用户")
            print(f"  - 用户ID: {github_user.id}")
            print(f"  - 用户名: {github_user.username}")
        else:
            print("❌ 通过GitHub ID查找用户失败")
    except Exception as e:
        print(f"❌ 查找用户异常: {e}")
    
    # 清理测试数据
    print("\n🧹 清理测试数据...")
    try:
        User.objects.filter(username='testuser').delete()
        print("✅ 测试数据清理完成")
    except Exception as e:
        print(f"❌ 数据清理失败: {e}")

def main():
    """主函数"""
    print("🚀 OAuth绑定功能测试")
    print("=" * 60)
    print()
    
    test_oauth_binding_logic()
    
    print("\n📋 测试完成！")
    print("\n💡 如果所有测试都通过，说明OAuth绑定逻辑正常工作")

if __name__ == '__main__':
    main()
