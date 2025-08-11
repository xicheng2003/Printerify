#!/usr/bin/env python
"""
Django迁移状态检查脚本
使用方法: python check_migration_status.py
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

from django.core.management import execute_from_command_line
from django.db import connection
from django.conf import settings

def check_database_connection():
    """检查数据库连接"""
    print("🔍 检查数据库连接...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ 数据库连接正常")
            return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def check_migration_status():
    """检查迁移状态"""
    print("\n🔍 检查迁移状态...")
    try:
        # 模拟执行showmigrations命令
        from django.core.management import call_command
        from io import StringIO
        
        output = StringIO()
        call_command('showmigrations', 'api', stdout=output)
        migrations_output = output.getvalue()
        
        print("✅ 迁移状态检查完成")
        print("📋 迁移详情:")
        print(migrations_output)
        
        return True
    except Exception as e:
        print(f"❌ 迁移状态检查失败: {e}")
        return False

def check_model_consistency():
    """检查模型一致性"""
    print("\n🔍 检查模型一致性...")
    try:
        from django.core.management import call_command
        
        # 检查模型
        call_command('check', '--database', 'default')
        print("✅ 模型一致性检查通过")
        return True
    except Exception as e:
        print(f"❌ 模型一致性检查失败: {e}")
        return False

def check_oauth_config():
    """检查OAuth配置"""
    print("\n🔍 检查OAuth配置...")
    
    # 检查必要的环境变量
    required_vars = [
        'GITHUB_CLIENT_ID',
        'GITHUB_CLIENT_SECRET', 
        'GOOGLE_CLIENT_ID',
        'GOOGLE_CLIENT_SECRET'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not getattr(settings, var, None):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  缺少OAuth环境变量: {', '.join(missing_vars)}")
        print("   这些变量在生产环境中必须设置")
    else:
        print("✅ OAuth环境变量配置完整")
    
    # 检查OAuth应用是否在INSTALLED_APPS中
    oauth_apps = [
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.github',
        'allauth.socialaccount.providers.google'
    ]
    
    missing_apps = []
    for app in oauth_apps:
        if app not in settings.INSTALLED_APPS:
            missing_apps.append(app)
    
    if missing_apps:
        print(f"❌ 缺少OAuth应用: {', '.join(missing_apps)}")
    else:
        print("✅ OAuth应用配置完整")
    
    return len(missing_vars) == 0 and len(missing_apps) == 0

def check_critical_models():
    """检查关键模型"""
    print("\n🔍 检查关键模型...")
    try:
        from api.models import User, Order, BindingGroup, Document
        
        # 检查User模型
        user_count = User.objects.count()
        print(f"✅ User模型 - 可用 (当前记录数: {user_count})")
        
        # 检查Order模型
        order_count = Order.objects.count()
        print(f"✅ Order模型 - 可用 (当前记录数: {order_count})")
        
        # 检查BindingGroup模型
        group_count = BindingGroup.objects.count()
        print(f"✅ BindingGroup模型 - 可用 (当前记录数: {group_count})")
        
        # 检查Document模型
        doc_count = Document.objects.count()
        print(f"✅ Document模型 - 可用 (当前记录数: {doc_count})")
        
        return True
    except Exception as e:
        print(f"❌ 模型检查失败: {e}")
        return False

def check_migration_files():
    """检查迁移文件"""
    print("\n🔍 检查迁移文件...")
    
    migrations_dir = Path("api/migrations")
    if not migrations_dir.exists():
        print("❌ 迁移目录不存在")
        return False
    
    migration_files = list(migrations_dir.glob("0*.py"))
    print(f"📁 找到 {len(migration_files)} 个迁移文件:")
    
    for file in sorted(migration_files):
        print(f"   - {file.name}")
    
    return True

def generate_migration_plan():
    """生成迁移计划"""
    print("\n🔍 生成迁移计划...")
    try:
        from django.core.management import call_command
        from io import StringIO
        
        output = StringIO()
        call_command('makemigrations', '--dry-run', 'api', stdout=output)
        plan_output = output.getvalue()
        
        if "No changes detected" in plan_output:
            print("✅ 无需创建新迁移")
        else:
            print("📝 建议的迁移计划:")
            print(plan_output)
        
        return True
    except Exception as e:
        print(f"❌ 生成迁移计划失败: {e}")
        return False

def main():
    """主函数"""
    print("🧪 Django迁移状态检查工具")
    print("=" * 50)
    
    # 执行各项检查
    checks = [
        ("数据库连接", check_database_connection),
        ("迁移状态", check_migration_status),
        ("模型一致性", check_model_consistency),
        ("OAuth配置", check_oauth_config),
        ("关键模型", check_critical_models),
        ("迁移文件", check_migration_files),
        ("迁移计划", generate_migration_plan),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name}检查异常: {e}")
            results.append((name, False))
    
    # 总结检查结果
    print("\n" + "=" * 50)
    print("📊 检查结果总结:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总体结果: {passed}/{total} 项检查通过")
    
    if passed == total:
        print("🎉 所有检查都通过了！可以安全进行迁移。")
        print("\n建议的下一步操作:")
        print("1. 备份数据库")
        print("2. 运行迁移: python manage.py migrate")
        print("3. 测试应用功能")
    else:
        print("⚠️  存在一些问题需要解决。")
        print("\n建议的解决方案:")
        print("1. 查看上面的错误信息")
        print("2. 参考 DJANGO_MIGRATION_TROUBLESHOOTING.md")
        print("3. 解决问题后重新运行检查")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
