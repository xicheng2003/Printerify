#!/usr/bin/env python
"""
OAuth配置测试脚本
用于检查OAuth相关的配置是否正确
"""

import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.conf import settings
from django.urls import reverse, resolve
from api.models import User
from allauth.socialaccount.models import SocialAccount

def test_environment_variables():
    """测试环境变量配置"""
    print("🔧 环境变量配置检查:")
    print("-" * 50)
    
    # 检查GitHub配置
    github_client_id = getattr(settings, 'GITHUB_CLIENT_ID', None)
    github_client_secret = getattr(settings, 'GITHUB_CLIENT_SECRET', None)
    
    print(f"GitHub Client ID: {'✅ 已配置' if github_client_id else '❌ 未配置'}")
    if github_client_id:
        print(f"  - 值: {github_client_id[:8]}...")
    
    print(f"GitHub Client Secret: {'✅ 已配置' if github_client_secret else '❌ 未配置'}")
    if github_client_secret:
        print(f"  - 值: {github_client_secret[:8]}...")
    
    # 检查Google配置
    google_client_id = getattr(settings, 'GOOGLE_CLIENT_ID', None)
    google_client_secret = getattr(settings, 'GOOGLE_CLIENT_SECRET', None)
    
    print(f"Google Client ID: {'✅ 已配置' if google_client_id else '❌ 未配置'}")
    if google_client_id:
        print(f"  - 值: {google_client_id[:8]}...")
    
    print(f"Google Client Secret: {'✅ 已配置' if google_client_secret else '❌ 未配置'}")
    if google_client_secret:
        print(f"  - 值: {google_client_secret[:8]}...")
    
    print()

def test_django_settings():
    """测试Django设置"""
    print("⚙️ Django设置检查:")
    print("-" * 50)
    
    # 检查INSTALLED_APPS
    required_apps = [
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.github',
        'allauth.socialaccount.providers.google'
    ]
    
    for app in required_apps:
        if app in settings.INSTALLED_APPS:
            print(f"✅ {app} - 已安装")
        else:
            print(f"❌ {app} - 未安装")
    
    # 检查AUTHENTICATION_BACKENDS
    required_backends = [
        'allauth.account.auth_backends.AuthenticationBackend'
    ]
    
    print("\n认证后端:")
    for backend in required_backends:
        if backend in settings.AUTHENTICATION_BACKENDS:
            print(f"✅ {backend} - 已配置")
        else:
            print(f"❌ {backend} - 未配置")
    
    print()

def test_urls():
    """测试URL配置"""
    print("🔗 URL配置检查:")
    print("-" * 50)
    
    try:
        # 测试GitHub OAuth URL
        github_url = reverse('oauth_github')
        print(f"✅ GitHub OAuth URL: {github_url}")
    except Exception as e:
        print(f"❌ GitHub OAuth URL: {e}")
    
    try:
        # 测试Google OAuth URL
        google_url = reverse('oauth_google')
        print(f"✅ Google OAuth URL: {google_url}")
    except Exception as e:
        print(f"❌ Google OAuth URL: {e}")
    
    try:
        # 测试OAuth回调URL
        callback_url = reverse('oauth_github_callback')
        print(f"✅ GitHub回调URL: {callback_url}")
    except Exception as e:
        print(f"❌ GitHub回调URL: {e}")
    
    print()

def test_models():
    """测试模型配置"""
    print("🗄️ 模型配置检查:")
    print("-" * 50)
    
    try:
        # 检查User模型字段
        user_fields = [field.name for field in User._meta.fields]
        required_fields = ['github_id', 'google_id', 'avatar_url']
        
        for field in required_fields:
            if field in user_fields:
                print(f"✅ User.{field} - 已存在")
            else:
                print(f"❌ User.{field} - 不存在")
        
        # 检查SocialAccount模型
        social_account_count = SocialAccount.objects.count()
        print(f"✅ SocialAccount模型 - 可用 (当前记录数: {social_account_count})")
        
    except Exception as e:
        print(f"❌ 模型检查失败: {e}")
    
    print()

def test_oauth_service():
    """测试OAuth服务"""
    print("🔐 OAuth服务检查:")
    print("-" * 50)
    
    try:
        from api.services.oauth_service import OAuthService
        
        service = OAuthService()
        print("✅ OAuthService - 已导入")
        
        # 检查服务属性
        if hasattr(service, 'github_client_id'):
            print(f"✅ GitHub Client ID属性: {'已设置' if service.github_client_id else '未设置'}")
        
        if hasattr(service, 'google_client_id'):
            print(f"✅ Google Client ID属性: {'已设置' if service.google_client_id else '未设置'}")
            
    except Exception as e:
        print(f"❌ OAuth服务检查失败: {e}")
    
    print()

def main():
    """主函数"""
    print("🚀 OAuth配置诊断工具")
    print("=" * 60)
    print()
    
    try:
        test_environment_variables()
        test_django_settings()
        test_urls()
        test_models()
        test_oauth_service()
        
        print("📋 诊断完成!")
        print("\n💡 如果看到❌标记，请检查相应的配置")
        print("🔧 主要检查点:")
        print("   1. 环境变量 (.env文件)")
        print("   2. Django设置 (settings.py)")
        print("   3. URL配置 (urls.py)")
        print("   4. 数据库迁移")
        
    except Exception as e:
        print(f"❌ 诊断过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
