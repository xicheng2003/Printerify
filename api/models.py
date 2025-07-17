# printerify/api/models.py (最终版，包含自定义文件路径)

import time
import random
import string
from django.db import models
from django.db.models import Max
from django.utils import timezone # 导入 timezone 模块

# --- 核心业务逻辑函数 ---

def generate_order_number():
    """生成格式为 YYYYMMDDHHMMSS + 4位随机数的订单号"""
    return time.strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999))

def generate_pickup_code():
    """
    生成一个在有效订单中唯一的、循环的取件码 (P-066 to P-666)。
    """
    from .models import Order

    ACTIVE_STATUSES = [
        Order.StatusChoices.PENDING,
        Order.StatusChoices.PROCESSING,
        Order.StatusChoices.COMPLETED,
    ]
    
    last_code_obj = Order.objects.filter(status__in=ACTIVE_STATUSES).aggregate(max_code=Max('pickup_code_num'))
    last_code_num = last_code_obj.get('max_code') or 65

    next_code_num = last_code_num + 1

    while True:
        if next_code_num > 666:
            next_code_num = 66

        code_to_check = f"P-{next_code_num:03d}"
        is_taken = Order.objects.filter(status__in=ACTIVE_STATUSES, pickup_code=code_to_check).exists()

        if not is_taken:
            return code_to_check, next_code_num

        next_code_num += 1

def get_order_document_path(instance, filename):
    """
    【已按您的要求修改】
    动态生成文件存储路径，现在包含了装订组和文件顺序。
    格式为: order_documents/YYYY-MM-DD/取件码/装订组_G(ID)/顺序号_原始文件名.pdf
    """
    # 获取当前日期，格式化为 YYYY-MM-DD
    current_date = timezone.now().strftime('%Y-%m-%d')
    
    # 从文件实例向上追溯，获取订单和组的信息
    order = instance.group.order
    group = instance.group
    
    # 获取文件在组内的顺序号 (例如：1, 2, 3...)
    sequence = instance.sequence_in_group
    
    # 创建新的、包含顺序号的文件名，例如 "01_文件A.pdf", "02_文件B.pdf"
    # 使用 :02d 可以确保数字总是两位数，如 1 会变成 01，方便按文件名排序
    new_filename = f"{sequence:02d}_{filename}"
    
    # 拼接并返回最终路径
    return f'order_documents/{current_date}/{order.pickup_code}/Group_{group.id}/{new_filename}'

def get_payment_screenshot_path(instance, filename):
    """
    【新增】付款凭证的存储路径
    格式为: payments/YYYY-MM-DD/取件码/原始文件名
    """
    current_date = timezone.now().strftime('%Y-%m-%d')
    pickup_code = instance.pickup_code
    return f'payments/{current_date}/{pickup_code}/{filename}'


# --- 模型定义 ---

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', '待处理'
        PROCESSING = 'processing', '处理中'
        COMPLETED = 'completed', '已完成'
        CANCELLED = 'cancelled', '已取消'

    order_number = models.CharField(max_length=20, unique=True, default=generate_order_number, help_text="时间戳订单号")
    pickup_code = models.CharField(max_length=10, blank=True, help_text="循环取件码 (P-XXX)")
    pickup_code_num = models.IntegerField(default=0, help_text="用于排序的取件码数字部分")
    phone_number = models.CharField(max_length=20, blank=True, help_text="顾客联系电话")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="订单总价")
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING, help_text="订单状态")
    # 【修改】payment_method 字段现在会正确保存
    payment_method = models.CharField(max_length=50, blank=True, null=True, help_text="支付方式")
    # 【修改】payment_screenshot 指向了我们新的动态路径函数
    payment_screenshot = models.FileField(upload_to=get_payment_screenshot_path, blank=True, null=True, help_text="支付凭证截图")
    order_summary_pdf = models.FileField(upload_to='summaries/', blank=True, null=True, help_text="订单摘要PDF")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_number} ({self.pickup_code})"

class BindingGroup(models.Model):
    order = models.ForeignKey(Order, related_name='groups', on_delete=models.CASCADE, help_text="所属订单")
    binding_type = models.CharField(max_length=50, default='none', help_text="装订方式")
    binding_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="此组的装订费用")
    sequence_in_order = models.PositiveIntegerField(default=0, help_text="组在订单中的顺序")

    # --- ▼▼▼ 在这里添加下面的代码 ▼▼▼ ---
    @property
    def binding_type_display(self):
        """返回装订方式的中文显示名称"""
        # 这个映射表可以根据您的需求随时扩展
        mapping = {
            'none': '不装订',
            'staple_top_left': '订书钉 (左上角)',
            'staple_left_side': '订书钉 (左侧)',
            'staple': '骑马钉',
            'ring_bound': '胶圈装',
        }
        # 如果在映射表中找不到，则安全地返回原始英文值
        return mapping.get(self.binding_type, self.binding_type)
    # --- ▲▲▲ 添加代码结束 ▲▲▲ ---

    class Meta:
        ordering = ['sequence_in_order']

    def __str__(self):
        return f"Group {self.id} for Order {self.order.order_number}"

class Document(models.Model):
    group = models.ForeignKey(BindingGroup, related_name='documents', on_delete=models.CASCADE, help_text="所属装订组")
    original_filename = models.CharField(max_length=255)
    # 【已修改】这里的 upload_to 指向了我们新的函数
    file_path = models.FileField(upload_to=get_order_document_path, help_text="文件存储路径")
    
    color_mode = models.CharField(max_length=20, default='black_white', help_text="色彩模式")
    print_sided = models.CharField(max_length=20, default='single', help_text="单双面")
    copies = models.PositiveIntegerField(default=1, help_text="打印份数")
    
    page_count = models.PositiveIntegerField(help_text="文件页数")
    print_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="此文件的打印费用")
    sequence_in_group = models.PositiveIntegerField(default=0, help_text="文件在组内的顺序")
    
    class Meta:
        ordering = ['sequence_in_group']

    def __str__(self):
        return f"Document {self.original_filename} in Group {self.group.id}"