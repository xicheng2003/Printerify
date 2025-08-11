#!/usr/bin/env python3
"""
OAuth配置和网络连接测试脚本
用于诊断OAuth相关问题
"""

import os
import sys
import django
import requests
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.conf import settings
from api.services.oauth_service import OAuthService

def test_oauth_config():
    """测试OAuth配置"""
    print("🔍 检查OAuth配置...")
    print("=" * 50)
    
    # 检查GitHub配置
    github_client_id = getattr(settings, 'GITHUB_CLIENT_ID', None)
    github_client_secret = getattr(settings, 'GITHUB_CLIENT_SECRET', None)
    
    print(f"GitHub Client ID: {'✅ 已配置' if github_client_id else '❌ 未配置'}")
    if github_client_id:
        print(f"  - 值: {github_client_id[:8]}...")
    
    print(f"GitHub Client Secret: {'✅ 已配置' if github_client_secret else '❌ 未配置'}")
    if github_client_secret:
        print(f"  - 值: {github_client_secret[:8]}...")
    
    print()
    
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

def test_network_connectivity():
    """测试网络连接"""
    print("🌐 测试网络连接...")
    print("=" * 50)
    
    # 测试GitHub API连接
    print("测试GitHub API连接...")
    try:
        response = requests.get('https://api.github.com', timeout=10)
        if response.status_code == 200:
            print("✅ GitHub API连接正常")
        else:
            print(f"⚠️ GitHub API响应异常: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ GitHub API连接失败: {e}")
    
    # 测试Google OAuth连接
    print("测试Google OAuth连接...")
    try:
        response = requests.get('https://oauth2.googleapis.com', timeout=10)
        if response.status_code == 200:
            print("✅ Google OAuth连接正常")
        else:
            print(f"⚠️ Google OAuth响应异常: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Google OAuth连接失败: {e}")
    
    # 测试SSL连接
    print("测试SSL连接...")
    try:
        response = requests.get('https://github.com', timeout=10, verify=True)
        if response.status_code == 200:
            print("✅ SSL连接正常")
        else:
            print(f"⚠️ SSL响应异常: {response.status_code}")
    except requests.exceptions.SSLError as e:
        print(f"❌ SSL连接失败: {e}")
    except requests.exceptions.RequestException as e:
        print(f"❌ 连接失败: {e}")
    
    print()

def test_oauth_service():
    """测试OAuth服务"""
    print("🔧 测试OAuth服务...")
    print("=" * 50)
    
    try:
        service = OAuthService()
        print("✅ OAuth服务实例化成功")
        
        # 检查服务属性
        if hasattr(service, 'github_client_id'):
            print(f"✅ GitHub Client ID属性: {'已设置' if service.github_client_id else '未设置'}")
        
        if hasattr(service, 'google_client_id'):
            print(f"✅ Google Client ID属性: {'已设置' if service.google_client_id else '未设置'}")
        
        # 检查网络会话配置
        if hasattr(service, 'session'):
            print("✅ 网络会话已配置")
            print(f"  - User-Agent: {service.session.headers.get('User-Agent', '未设置')}")
            print(f"  - 重试次数: {getattr(service, 'max_retries', '未设置')}")
            print(f"  - 重试延迟: {getattr(service, 'retry_delay', '未设置')}秒")
        
    except Exception as e:
        print(f"❌ OAuth服务测试失败: {e}")
    
    print()

def test_environment_variables():
    """测试环境变量"""
    print("🔑 检查环境变量...")
    print("=" * 50)
    
    # 检查.env文件
    env_file = project_root / '.env'
    if env_file.exists():
        print(f"✅ 找到.env文件: {env_file}")
        
        # 读取并检查关键配置
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            required_vars = [
                'GITHUB_CLIENT_ID',
                'GITHUB_CLIENT_SECRET', 
                'GOOGLE_CLIENT_ID',
                'GOOGLE_CLIENT_SECRET'
            ]
            
            for var in required_vars:
                if var in content:
                    print(f"  ✅ {var}: 已配置")
                else:
                    print(f"  ❌ {var}: 未配置")
                    
        except Exception as e:
            print(f"  ❌ 读取.env文件失败: {e}")
    else:
        print(f"❌ 未找到.env文件: {env_file}")
        print("  请创建.env文件并配置OAuth凭据")
    
    print()

def main():
    """主函数"""
    print("🚀 OAuth配置和网络连接诊断工具")
    print("=" * 60)
    print()
    
    test_oauth_config()
    test_network_connectivity()
    test_oauth_service()
    test_environment_variables()
    
    print("📋 诊断完成！")
    print()
    print("💡 如果发现问题，请检查：")
    print("  1. 环境变量是否正确配置")
    print("  2. 网络连接是否稳定")
    print("  3. 防火墙设置是否阻止了连接")
    print("  4. OAuth应用配置是否正确")

if __name__ == '__main__':
    main()
