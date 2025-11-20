import os
import sys
import random
import django
from django.db.models import Count, Q

# 设置 Django 环境
# 假设脚本位于 scripts/ 目录下，需要将项目根目录添加到 path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Order

def generate_unique_code():
    """临时生成唯一码函数"""
    active_statuses = ['pending', 'processing', 'completed']
    while True:
        num = random.randint(10, 999)
        code = f"P-{num:03d}"
        if not Order.objects.filter(status__in=active_statuses, pickup_code=code).exists():
            return code, num

def fix_data():
    print("正在检查数据库中的冲突数据...")
    
    active_statuses = ['pending', 'processing', 'completed']
    
    # 1. 处理空取件码的活跃订单
    empty_code_orders = Order.objects.filter(
        status__in=active_statuses,
        pickup_code=''
    )
    if empty_code_orders.exists():
        print(f"发现 {empty_code_orders.count()} 个没有取件码的活跃订单，正在修复...")
        for order in empty_code_orders:
            new_code, new_num = generate_unique_code()
            order.pickup_code = new_code
            order.pickup_code_num = new_num
            order.save()
            print(f"  - 订单 {order.order_number}: 补全取件码 -> {new_code}")

    # 2. 处理重复取件码
    duplicates = Order.objects.filter(
        status__in=active_statuses
    ).values('pickup_code').annotate(
        count=Count('id')
    ).filter(count__gt=1)
    
    if not duplicates:
        print("没有发现重复的取件码。")
    else:
        print(f"发现 {len(duplicates)} 组重复取件码，正在修复...")
        for item in duplicates:
            code = item['pickup_code']
            # 获取所有使用该代码的订单
            orders = list(Order.objects.filter(
                status__in=active_statuses, 
                pickup_code=code
            ))
            
            # 保留第一个，修改其他的
            print(f"  处理重复组 {code}: 保留 {orders[0].order_number}, 修改其余 {len(orders)-1} 个")
            for order in orders[1:]:
                new_code, new_num = generate_unique_code()
                print(f"    - 订单 {order.order_number}: {code} -> {new_code}")
                order.pickup_code = new_code
                order.pickup_code_num = new_num
                order.save()

    print("\n数据修复完成！现在您可以重新运行 'python manage.py migrate' 了。")

if __name__ == '__main__':
    fix_data()
