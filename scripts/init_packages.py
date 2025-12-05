#!/usr/bin/env python
"""
打印套餐系统 - 初始化套餐数据脚本

使用方法：
Windows: python scripts/init_packages.py
Linux/Mac: python scripts/init_packages.py
"""

import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Package
from decimal import Decimal

def create_initial_packages():
    """创建初始套餐数据"""
    
    # 检查是否已有套餐
    if Package.objects.exists():
        print("⚠️  检测到已有套餐数据，是否要删除并重新创建？")
        response = input("输入 'yes' 确认删除并重建，其他键取消: ")
        if response.lower() == 'yes':
            Package.objects.all().delete()
            print("✅ 已删除旧套餐数据")
        else:
            print("❌ 操作已取消")
            return
    
    packages_data = [
        {
            'name': '基础版',
            'description': '适合轻量用户，偶尔打印',
            'pages': 100,
            'price': Decimal('14.20'),
            'original_price': Decimal('15.00'),
            'discount_rate': Decimal('95'),
            'is_active': True,
            'is_featured': False,
            'sort_order': 1
        },
        {
            'name': '标准版',
            'description': '适合日常使用，性价比高',
            'pages': 300,
            'price': Decimal('40.50'),
            'original_price': Decimal('45.00'),
            'discount_rate': Decimal('90'),
            'is_active': True,
            'is_featured': True,  # 推荐套餐
            'sort_order': 2
        },
        {
            'name': '超值版',
            'description': '适合重度用户，大量打印',
            'pages': 500,
            'price': Decimal('63.75'),
            'original_price': Decimal('75.00'),
            'discount_rate': Decimal('85'),
            'is_active': True,
            'is_featured': False,
            'sort_order': 3
        },
        {
            'name': '旗舰版',
            'description': '适合超级用户，海量打印',
            'pages': 1000,
            'price': Decimal('120.00'),
            'original_price': Decimal('150.00'),
            'discount_rate': Decimal('80'),
            'is_active': True,
            'is_featured': False,
            'sort_order': 4
        }
    ]
    
    created_count = 0
    for pkg_data in packages_data:
        package = Package.objects.create(**pkg_data)
        created_count += 1
        
        # 计算节省金额
        savings = float(pkg_data['original_price']) - float(pkg_data['price'])
        price_per_page = float(pkg_data['price']) / pkg_data['pages']
        
        print(f"✅ 创建套餐: {package.name}")
        print(f"   - 页数: {package.pages}页")
        print(f"   - 价格: ¥{package.price} (原价 ¥{package.original_price})")
        print(f"   - 折扣: {package.discount_rate}折")
        print(f"   - 单页: ¥{price_per_page:.3f}/页")
        print(f"   - 节省: ¥{savings:.2f}")
        if package.is_featured:
            print(f"   - 🌟 推荐套餐")
        print()
    
    print(f"🎉 成功创建 {created_count} 个套餐！")
    print()
    print("📋 下一步:")
    print("1. 访问前端查看套餐: http://localhost:5173/packages")
    print("2. 在 Django Admin 管理套餐: http://localhost:8000/admin/api/package/")
    print()

if __name__ == '__main__':
    create_initial_packages()
