#!/usr/bin/env python
"""
环境变量设置脚本
这个脚本帮助您设置必要的环境变量
"""
import os
import secrets
import string

def generate_secret_key():
    """生成一个安全的SECRET_KEY"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(50))

def create_env_file():
    """创建.env文件"""
    env_content = f"""# Django 核心配置
SECRET_KEY={generate_secret_key()}
DEBUG=True

# 数据库配置
USE_POSTGRES=False

# 如果使用PostgreSQL，取消注释并设置以下变量
# USE_POSTGRES=True
# POSTGRES_DB=printerify
# POSTGRES_USER=your_db_user
# POSTGRES_PASSWORD=your_db_password
# POSTGRES_HOST=localhost
# POSTGRES_PORT=5432

# 邮件配置
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=localhost
EMAIL_PORT=25
EMAIL_USE_TLS=False
EMAIL_USE_SSL=False
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=

# Redis配置
REDIS_PASSWORD=

# OAuth配置（可选）
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ .env 文件创建成功!")
        print("⚠️  注意: 在生产环境中，请修改 SECRET_KEY 为更安全的值")
        return True
    except Exception as e:
        print(f"❌ 创建 .env 文件失败: {e}")
        return False

def check_env_vars():
    """检查环境变量是否已设置"""
    required_vars = ['SECRET_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ 缺少必要的环境变量: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ 所有必要的环境变量都已设置")
        return True

def main():
    print("🔧 环境变量设置工具")
    print("=" * 50)
    
    # 检查是否已存在.env文件
    if os.path.exists('.env'):
        print("📁 .env 文件已存在")
        choice = input("是否要重新创建? (y/N): ").lower().strip()
        if choice != 'y':
            print("保持现有 .env 文件不变")
            return
    
    # 创建.env文件
    if create_env_file():
        print("\n📋 下一步操作:")
        print("1. 检查 .env 文件中的配置")
        print("2. 根据您的环境修改相应的值")
        print("3. 重启Django服务器")
        print("\n💡 提示: 在生产环境中，请确保:")
        print("   - DEBUG=False")
        print("   - 使用强密码的SECRET_KEY")
        print("   - 正确配置数据库连接")
    else:
        print("\n❌ 设置失败，请手动创建 .env 文件")

if __name__ == "__main__":
    main()
