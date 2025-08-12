#!/usr/bin/env python3
"""
OAuth修复验证脚本
快速验证所有硬编码的127.0.0.1地址是否已被修复
"""

import os
import re
from pathlib import Path

def check_hardcoded_urls():
    """检查是否还有硬编码的127.0.0.1地址"""
    print("🔍 检查硬编码的127.0.0.1地址...")
    
    # 需要检查的文件（排除settings.py，因为它包含正常的配置）
    files_to_check = [
        'api/views.py',
        'frontend/src/views/OAuthCallbackView.vue',
        'frontend/src/router/index.js'
    ]
    
    found_hardcoded = []
    
    for file_path in files_to_check:
        if Path(file_path).exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 查找硬编码的127.0.0.1:5173
            matches = re.findall(r'127\.0\.0\.1:5173', content)
            if matches:
                found_hardcoded.append({
                    'file': file_path,
                    'count': len(matches),
                    'matches': matches
                })
    
    if found_hardcoded:
        print("❌ 发现硬编码的127.0.0.1地址:")
        for item in found_hardcoded:
            print(f"   {item['file']}: {item['count']} 处")
        return False
    else:
        print("✅ 未发现硬编码的127.0.0.1地址")
        return True

def check_dynamic_url_config():
    """检查是否使用了动态URL配置"""
    print("\n🔍 检查动态URL配置...")
    
    # 检查settings.py中的FRONTEND_URL配置
    if Path('backend/settings.py').exists():
        with open('backend/settings.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'FRONTEND_URL' in content:
            print("✅ 在settings.py中找到了FRONTEND_URL配置")
        else:
            print("❌ 在settings.py中未找到FRONTEND_URL配置")
            return False
    
    # 检查views.py中是否使用了settings.FRONTEND_URL
    if Path('api/views.py').exists():
        with open('api/views.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'settings.FRONTEND_URL' in content:
            print("✅ 在views.py中使用了settings.FRONTEND_URL")
        else:
            print("❌ 在views.py中未使用settings.FRONTEND_URL")
            return False
    
    return True

def check_oauth_callback_urls():
    """检查OAuth回调URL的构建方式"""
    print("\n🔍 检查OAuth回调URL构建...")
    
    if Path('api/views.py').exists():
        with open('api/views.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查是否还有硬编码的frontend_callback_url
        hardcoded_patterns = [
            r"frontend_callback_url = 'http://127\.0\.0\.1:5173/oauth/callback'",
            r"frontend_callback_url = 'http://127\.0\.0\.1:5173/oauth/callback'"
        ]
        
        found_hardcoded = False
        for pattern in hardcoded_patterns:
            if re.search(pattern, content):
                found_hardcoded = True
                break
        
        if found_hardcoded:
            print("❌ 发现硬编码的frontend_callback_url")
            return False
        else:
            print("✅ 未发现硬编码的frontend_callback_url")
            
        # 检查是否使用了动态构建
        if "f'{settings.FRONTEND_URL}/oauth/callback'" in content:
            print("✅ 使用了动态构建的回调URL")
            return True
        else:
            print("❌ 未使用动态构建的回调URL")
            return False
    
    return False

def check_environment_config():
    """检查环境配置"""
    print("\n🔍 检查环境配置...")
    
    # 检查是否有.env文件
    env_files = ['.env', '.env.local', '.env.production']
    env_found = False
    
    for env_file in env_files:
        if Path(env_file).exists():
            print(f"✅ 找到环境配置文件: {env_file}")
            env_found = True
            break
    
    if not env_found:
        print("⚠️  未找到环境配置文件，建议创建.env文件")
    
    # 检查env_example.txt是否包含FRONTEND_URL
    if Path('env_example.txt').exists():
        with open('env_example.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'FRONTEND_URL' in content:
            print("✅ env_example.txt包含FRONTEND_URL配置说明")
        else:
            print("❌ env_example.txt未包含FRONTEND_URL配置说明")
    
    return True

def main():
    """主函数"""
    print("🚀 OAuth修复验证工具")
    print("=" * 50)
    
    # 检查当前工作目录
    if not Path('manage.py').exists():
        print("❌ 请在项目根目录运行此脚本")
        return
    
    all_passed = True
    
    # 执行各项检查
    if not check_hardcoded_urls():
        all_passed = False
    
    if not check_dynamic_url_config():
        all_passed = False
    
    if not check_oauth_callback_urls():
        all_passed = False
    
    check_environment_config()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有检查都通过了！OAuth修复完成。")
        print("\n💡 下一步：")
        print("   1. 在生产环境设置 FRONTEND_URL=https://print.morlight.top")
        print("   2. 更新GitHub和Google OAuth应用的回调URL")
        print("   3. 重启Django服务")
        print("   4. 测试OAuth登录流程")
    else:
        print("❌ 部分检查未通过，请根据上述提示进行修复。")
        print("\n💡 修复完成后，重新运行此脚本验证。")

if __name__ == '__main__':
    main()
