#!/usr/bin/env python3
"""
OAuth配置检查脚本
用于验证生产环境的OAuth回调链接配置是否正确
"""

import os
import sys
from pathlib import Path

def check_environment():
    """检查环境变量配置"""
    print("🔍 检查环境变量配置...")
    
    # 检查Django设置
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    
    try:
        import django
        django.setup()
        from django.conf import settings
        
        print(f"✅ Django设置加载成功")
        print(f"   DEBUG模式: {settings.DEBUG}")
        print(f"   允许的主机: {settings.ALLOWED_HOSTS}")
        
        # 检查前端URL配置
        if hasattr(settings, 'FRONTEND_URL'):
            print(f"   前端URL: {settings.FRONTEND_URL}")
            
            # 验证前端URL格式
            if settings.DEBUG:
                if '127.0.0.1' in settings.FRONTEND_URL:
                    print("   ✅ 开发环境配置正确")
                else:
                    print("   ⚠️  开发环境建议使用127.0.0.1")
            else:
                if '127.0.0.1' in settings.FRONTEND_URL:
                    print("   ❌ 生产环境错误：使用了本地地址")
                    print("   💡 生产环境应该使用: https://print.morlight.top")
                elif 'print.morlight.top' in settings.FRONTEND_URL:
                    print("   ✅ 生产环境配置正确")
                else:
                    print("   ⚠️  生产环境URL不是预期的域名")
        else:
            print("   ❌ 缺少FRONTEND_URL配置")
            
        # 检查CORS配置
        print(f"   CORS允许的源: {getattr(settings, 'CORS_ALLOWED_ORIGINS', '未配置')}")
        print(f"   CSRF信任的源: {getattr(settings, 'CSRF_TRUSTED_ORIGINS', '未配置')}")
        
    except Exception as e:
        print(f"❌ Django设置加载失败: {e}")
        return False
    
    return True

def check_oauth_providers():
    """检查OAuth提供商配置"""
    print("\n🔍 检查OAuth提供商配置...")
    
    try:
        from django.conf import settings
        
        # 检查GitHub配置
        github_client_id = getattr(settings, 'GITHUB_CLIENT_ID', None)
        github_client_secret = getattr(settings, 'GITHUB_CLIENT_SECRET', None)
        
        if github_client_id and github_client_secret:
            print("   ✅ GitHub OAuth已配置")
            print(f"      Client ID: {github_client_id[:8]}...")
        else:
            print("   ⚠️  GitHub OAuth未配置")
            
        # 检查Google配置
        google_client_id = getattr(settings, 'GOOGLE_CLIENT_ID', None)
        google_client_secret = getattr(settings, 'GOOGLE_CLIENT_SECRET', None)
        
        if google_client_id and google_client_secret:
            print("   ✅ Google OAuth已配置")
            print(f"      Client ID: {google_client_id[:8]}...")
        else:
            print("   ⚠️  Google OAuth未配置")
            
    except Exception as e:
        print(f"❌ OAuth提供商检查失败: {e}")

def check_url_configuration():
    """检查URL配置"""
    print("\n🔍 检查URL配置...")
    
    try:
        from django.conf import settings
        from django.urls import reverse
        
        # 检查OAuth回调URL
        if hasattr(settings, 'FRONTEND_URL'):
            frontend_url = settings.FRONTEND_URL
            oauth_callback_url = f"{frontend_url}/oauth/callback"
            
            print(f"   OAuth回调URL: {oauth_callback_url}")
            
            # 验证URL格式
            if settings.DEBUG:
                if '127.0.0.1' in oauth_callback_url:
                    print("   ✅ 开发环境回调URL正确")
                else:
                    print("   ⚠️  开发环境回调URL可能不正确")
            else:
                if '127.0.0.1' in oauth_callback_url:
                    print("   ❌ 生产环境错误：回调URL指向本地地址")
                    print("   💡 应该指向: https://print.morlight.top/oauth/callback")
                elif 'print.morlight.top' in oauth_callback_url:
                    print("   ✅ 生产环境回调URL正确")
                else:
                    print("   ⚠️  生产环境回调URL不是预期的域名")
        else:
            print("   ❌ 无法确定OAuth回调URL（缺少FRONTEND_URL配置）")
            
    except Exception as e:
        print(f"❌ URL配置检查失败: {e}")

def check_oauth_views():
    """检查OAuth视图配置"""
    print("\n🔍 检查OAuth视图配置...")
    
    try:
        # 检查views.py中的硬编码URL
        views_file = Path('api/views.py')
        if views_file.exists():
            content = views_file.read_text(encoding='utf-8')
            
            # 检查是否还有硬编码的127.0.0.1
            if '127.0.0.1:5173' in content:
                print("   ❌ 发现硬编码的本地地址")
                print("   💡 请检查api/views.py中是否还有未修复的硬编码URL")
            else:
                print("   ✅ 未发现硬编码的本地地址")
                
            # 检查是否使用了settings.FRONTEND_URL
            if 'settings.FRONTEND_URL' in content:
                print("   ✅ 使用了动态前端URL配置")
            else:
                print("   ⚠️  可能没有使用动态前端URL配置")
        else:
            print("   ❌ 无法找到api/views.py文件")
            
    except Exception as e:
        print(f"❌ OAuth视图检查失败: {e}")

def generate_production_config():
    """生成生产环境配置建议"""
    print("\n📋 生产环境配置建议:")
    print("=" * 50)
    
    print("1. 环境变量配置 (.env 文件):")
    print("   DEBUG=False")
    print("   FRONTEND_URL=https://print.morlight.top")
    print("   GITHUB_CLIENT_ID=你的GitHub客户端ID")
    print("   GITHUB_CLIENT_SECRET=你的GitHub客户端密钥")
    print("   GOOGLE_CLIENT_ID=你的Google客户端ID")
    print("   GOOGLE_CLIENT_SECRET=你的Google客户端密钥")
    
    print("\n2. GitHub OAuth应用配置:")
    print("   - 登录GitHub开发者设置")
    print("   - 创建新的OAuth应用")
    print("   - Authorization callback URL设置为:")
    print("     https://print.morlight.top/api/oauth/github/callback/")
    
    print("\n3. Google OAuth应用配置:")
    print("   - 登录Google Cloud Console")
    print("   - 创建OAuth 2.0客户端ID")
    print("   - 授权重定向URI设置为:")
    print("     https://print.morlight.top/api/oauth/google/callback/")
    
    print("\n4. 前端路由配置:")
    print("   - 确保 /oauth/callback 路由正确配置")
    print("   - 检查前端域名是否为 print.morlight.top")
    
    print("\n5. 部署后验证:")
    print("   - 访问 https://print.morlight.top")
    print("   - 测试OAuth登录流程")
    print("   - 检查浏览器开发者工具中的网络请求")

def main():
    """主函数"""
    print("🚀 OAuth配置检查工具")
    print("=" * 50)
    
    # 检查当前工作目录
    if not Path('manage.py').exists():
        print("❌ 请在项目根目录运行此脚本")
        sys.exit(1)
    
    # 执行各项检查
    if not check_environment():
        print("\n❌ 环境检查失败，无法继续")
        sys.exit(1)
    
    check_oauth_providers()
    check_url_configuration()
    check_oauth_views()
    
    # 生成配置建议
    generate_production_config()
    
    print("\n✅ 检查完成！")
    print("\n💡 如果发现问题，请根据上述建议进行修复")

if __name__ == '__main__':
    main()
