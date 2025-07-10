# 文件路径: api/models.py

import random
from django.db import models
from django.db.models import Max
import time # 移到文件顶部

def generate_order_number():
    """生成格式为YYYYMMDDHHMMSS + 4位随机数的订单号"""
    return time.strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999))

def generate_pickup_code():
    """
    生成一个在有效订单中唯一的、循环的取件码 (P-066 to P-666)。
    """
    # 延迟导入以避免循环依赖
    from .models import Order

    ACTIVE_STATUSES = [
        Order.StatusChoices.PENDING,
        Order.StatusChoices.PRINTING,
        Order.StatusChoices.COMPLETED,
    ]

    last_code_obj = Order.objects.filter(status__in=ACTIVE_STATUSES).aggregate(max_code=Max('pickup_code_num'))
    last_code_num = last_code_obj.get('max_code') or 65 # 起始码的前一个

    next_code_num = last_code_num + 1

    while True:
        if next_code_num > 666:
            next_code_num = 66

        code_to_check = f"P-{next_code_num:03d}"
        is_taken = Order.objects.filter(status__in=ACTIVE_STATUSES, pickup_code=code_to_check).exists()

        if not is_taken:
            return code_to_check, next_code_num

        next_code_num += 1

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', '待处理'
        PRINTING = 'PRINTING', '打印中'
        COMPLETED = 'COMPLETED', '已完成'
        PICKED_UP = 'PICKED_UP', '已取件'
        CANCELLED = 'CANCELLED', '已取消'

    order_number = models.CharField(max_length=20, default=generate_order_number, unique=True, editable=False, verbose_name="订单号")
    phone_number = models.CharField(max_length=15, verbose_name="用户手机号")
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING, verbose_name="订单状态")
    specifications = models.JSONField(verbose_name="打印规格")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="订单总价")
    payment_screenshot = models.ImageField(upload_to='screenshots/%Y/%m/%d/', blank=True, null=True, verbose_name="付款截图")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    pickup_code = models.CharField(max_length=10, blank=True, verbose_name="取件码")
    pickup_code_num = models.IntegerField(default=0, verbose_name="取件码数字部分")

    # --- 新增字段 ---
    order_summary_pdf = models.FileField(upload_to='order_summaries/%Y/%m/%d/', blank=True, null=True, verbose_name="订单详情PDF")


    def __str__(self):
        return f"订单 {self.order_number} ({self.pickup_code})"

class PrintFile(models.Model):
    class PurposeChoices(models.TextChoices):
        PRINT = 'PRINT', '打印文件'
        PAYMENT = 'PAYMENT', '付款凭证'

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='files', verbose_name="所属订单")
    file = models.FileField(upload_to='print_files/%Y/%m/%d/', verbose_name="上传的文件")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")
    purpose = models.CharField(max_length=10, choices=PurposeChoices.choices, default=PurposeChoices.PRINT, verbose_name="文件用途")

    def __str__(self):
        import os
        if self.order:
            return f"文件 {os.path.basename(self.file.name)} (订单: {self.order.order_number})"
        return f"待关联文件 {os.path.basename(self.file.name)}"