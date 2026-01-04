#!/usr/bin/env python
"""
快速演示脚本：暂停营业功能演示

这个脚本演示如何使用API快速启用/禁用营业状态。
"""

import os
import sys
import django

# 配置Django设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import SystemConfig

def print_header(text):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def show_current_status():
    """显示当前营业状态"""
    config = SystemConfig.get_config()
    status = "✓ 营业中" if config.is_open else "✗ 已关闭"
    print(f"\n当前状态: {status}")
    print(f"关闭原因: {config.closure_reason}")
    if config.reopening_date:
        print(f"重新开业: {config.reopening_date}")
    if config.notice_content:
        print(f"额外通知:\n{config.notice_content}")

def enable_closure():
    """启用关闭状态"""
    print_header("启用暂停营业")
    
    config = SystemConfig.get_config()
    config.is_open = False
    config.closure_reason = "放假暂停营业，感谢您的理解！"
    config.reopening_date = "2026-02-01"
    config.notice_content = """我们将在2月1日恢复营业。
如有紧急需求，请通过以下方式联系我们：
📧 邮箱：support@printerify.com
📱 电话：400-XXX-XXXX"""
    config.allow_viewing_history = True
    config.save()
    
    print("✓ 暂停营业已启用")
    show_current_status()

def disable_closure():
    """禁用关闭状态"""
    print_header("恢复营业")
    
    config = SystemConfig.get_config()
    config.is_open = True
    config.save()
    
    print("✓ 营业已恢复")
    show_current_status()

def main():
    """主函数"""
    print_header("暂停营业功能演示")
    
    print("""
可用命令：
  1. 显示当前状态
  2. 启用暂停营业
  3. 禁用暂停营业（恢复营业）
  0. 退出
    """)
    
    while True:
        choice = input("\n请选择 (0-3): ").strip()
        
        if choice == '0':
            print("\n再见！")
            break
        elif choice == '1':
            show_current_status()
        elif choice == '2':
            enable_closure()
        elif choice == '3':
            disable_closure()
        else:
            print("❌ 无效选择，请重试")
    
if __name__ == '__main__':
    main()
