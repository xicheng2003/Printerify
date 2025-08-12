#!/usr/bin/env python
"""
OAuth集成测试脚本
测试完整的OAuth流程：GitHub登录 → 后端回调 → 前端重定向
"""

import requests
import time
import json

def test_github_oauth_flow():
    """测试GitHub OAuth完整流程"""
    print("🔍 测试GitHub OAuth完整流程")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000"
    frontend_url = "http://127.0.0.1:5173"
    
    # 1. 访问GitHub登录URL
    print("\n1. 访问GitHub登录URL...")
    github_login_url = f"{base_url}/api/oauth/github/"
    
    try:
        response = requests.get(github_login_url, allow_redirects=False)
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 302:
            redirect_url = response.headers.get('Location')
            print(f"   重定向到GitHub: {redirect_url}")
            
            # 检查重定向URL是否包含正确的参数
            if 'client_id=' in redirect_url and 'redirect_uri=' in redirect_url:
                print("   ✅ GitHub授权URL格式正确")
                
                # 提取回调URL
                if 'redirect_uri=' in redirect_url:
                    callback_start = redirect_url.find('redirect_uri=') + len('redirect_uri=')
                    callback_end = redirect_url.find('&', callback_start)
                    if callback_end == -1:
                        callback_end = len(redirect_url)
                    
                    callback_url = redirect_url[callback_start:callback_end]
                    print(f"   回调URL: {callback_url}")
                    
                    # 检查回调URL是否正确
                    expected_callback = f"{base_url}/api/oauth/github/callback/"
                    if callback_url == expected_callback:
                        print("   ✅ 回调URL配置正确")
                    else:
                        print(f"   ❌ 回调URL不匹配")
                        print(f"      期望: {expected_callback}")
                        print(f"      实际: {callback_url}")
                        print(f"   ⚠️  这可能是问题的根源！")
            else:
                print("   ❌ GitHub授权URL格式不正确")
        else:
            print(f"   ❌ 期望重定向(302)，但得到状态码: {response.status_code}")
            print(f"   响应内容: {response.text[:200]}...")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 请求失败: {str(e)}")
    
    # 2. 测试前端回调页面
    print("\n2. 测试前端回调页面...")
    frontend_callback_url = f"{frontend_url}/oauth/callback"
    
    try:
        # 测试成功情况
        success_url = f"{frontend_callback_url}?provider=github&success=true&username=testuser"
        print(f"   测试成功回调URL: {success_url}")
        
        response = requests.get(success_url)
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ 前端回调页面可访问")
        else:
            print(f"   ❌ 前端回调页面不可访问: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 前端测试失败: {str(e)}")
    
    # 3. 测试后端用户信息接口
    print("\n3. 测试后端用户信息接口...")
    userinfo_url = f"{base_url}/api/oauth/userinfo/"
    
    try:
        response = requests.get(userinfo_url)
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 401:
            print("   ✅ 用户信息接口正常工作（需要认证）")
        elif response.status_code == 200:
            print("   ✅ 用户信息接口返回数据")
            data = response.json()
            print(f"   用户信息: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"   ⚠️  用户信息接口状态码: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 用户信息接口测试失败: {str(e)}")
    
    print("\n" + "=" * 60)

def test_google_oauth_flow():
    """测试Google OAuth完整流程"""
    print("🔍 测试Google OAuth完整流程")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000"
    frontend_url = "http://127.0.0.1:5173"
    
    # 1. 访问Google登录URL
    print("\n1. 访问Google登录URL...")
    google_login_url = f"{base_url}/api/oauth/google/"
    
    try:
        response = requests.get(google_login_url, allow_redirects=False)
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 302:
            redirect_url = response.headers.get('Location')
            print(f"   重定向到Google: {redirect_url}")
            
            # 检查重定向URL是否包含正确的参数
            if 'client_id=' in redirect_url and 'redirect_uri=' in redirect_url:
                print("   ✅ Google授权URL格式正确")
                
                # 提取回调URL
                if 'redirect_uri=' in redirect_url:
                    callback_start = redirect_url.find('redirect_uri=') + len('redirect_uri=')
                    callback_end = redirect_url.find('&', callback_start)
                    if callback_end == -1:
                        callback_end = len(redirect_url)
                    
                    callback_url = redirect_url[callback_start:callback_end]
                    print(f"   回调URL: {callback_url}")
                    
                    # 检查回调URL是否正确
                    expected_callback = f"{base_url}/api/oauth/google/callback/"
                    if callback_url == expected_callback:
                        print("   ✅ 回调URL配置正确")
                    else:
                        print(f"   ❌ 回调URL不匹配")
                        print(f"      期望: {expected_callback}")
                        print(f"      实际: {callback_url}")
                        print(f"   ⚠️  这可能是问题的根源！")
            else:
                print("   ❌ Google授权URL格式不正确")
        else:
            print(f"   ❌ 期望重定向(302)，但得到状态码: {response.status_code}")
            print(f"   响应内容: {response.text[:200]}...")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 请求失败: {str(e)}")
    
    print("\n" + "=" * 60)

def main():
    """主函数"""
    print("🚀 开始OAuth集成测试...")
    print("请确保:")
    print("1. Django后端服务器运行在 http://127.0.0.1:8000")
    print("2. Vue前端服务器运行在 http://127.0.0.1:5173")
    print("3. 已正确配置GitHub和Google OAuth应用的回调URL")
    print()
    
    # 等待一下，确保服务器启动
    time.sleep(2)
    
    test_github_oauth_flow()
    test_google_oauth_flow()
    
    print("✅ 集成测试完成！")
    print("\n📝 重要检查项:")
    print("1. 确保GitHub OAuth应用的回调URL为: http://127.0.0.1:8000/api/oauth/github/callback/")
    print("2. 确保Google OAuth应用的回调URL为: http://127.0.0.1:8000/api/oauth/google/callback/")
    print("3. 如果回调URL不匹配，OAuth提供商将无法正确重定向")
    print("4. 检查Django控制台日志，查看OAuth回调的详细信息")

if __name__ == '__main__':
    main()
