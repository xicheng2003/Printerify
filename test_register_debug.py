#!/usr/bin/env python
"""
调试用户注册API的脚本
"""
import requests
import json

def test_register_api():
    """测试用户注册API"""
    url = "http://127.0.0.1:8000/api/register/"
    
    # 测试数据
    test_data = {
        "username": "debuguser123",
        "email": "debuguser123@example.com",
        "phone_number": "13800138002",
        "password": "debugpass123",
        "password_confirm": "debugpass123"
    }
    
    print("🔍 开始调试用户注册API...")
    print(f"📡 请求URL: {url}")
    print(f"📋 请求数据: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
    print("-" * 50)
    
    try:
        # 发送POST请求
        response = requests.post(url, json=test_data)
        
        print(f"📊 响应状态码: {response.status_code}")
        print(f"📋 响应头: {dict(response.headers)}")
        print(f"📄 响应内容: {response.text}")
        
        if response.status_code == 201:
            print("✅ 注册成功!")
            data = response.json()
            print(f"👤 用户ID: {data.get('user', {}).get('id')}")
            print(f"🔑 Token: {data.get('token')}")
        elif response.status_code == 400:
            print("❌ 注册失败 - 400错误:")
            try:
                error_data = response.json()
                print("🔍 错误详情:")
                for field, errors in error_data.items():
                    print(f"  {field}: {errors}")
            except:
                print(f"  📝 无法解析错误详情: {response.text}")
        else:
            print(f"❌ 意外状态码: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保Django服务器正在运行")
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")

def test_csrf_endpoint():
    """测试CSRF端点"""
    print("\n" + "="*50)
    print("🔍 测试CSRF端点...")
    
    url = "http://127.0.0.1:8000/api/csrf/"
    
    try:
        response = requests.get(url)
        print(f"📊 CSRF端点状态码: {response.status_code}")
        print(f"📋 CSRF响应: {response.text[:100]}...")
        
        if response.status_code == 200:
            print("✅ CSRF端点工作正常")
        else:
            print("❌ CSRF端点有问题")
            
    except Exception as e:
        print(f"❌ CSRF测试失败: {e}")

if __name__ == "__main__":
    print("🚀 用户注册API调试工具")
    print("=" * 50)
    
    # 测试CSRF端点
    test_csrf_endpoint()
    
    # 测试注册API
    test_register_api()
