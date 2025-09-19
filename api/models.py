# printerify/api/models.py (最终版，包含自定义文件路径)

import time
import random
import string
from django.db import models
from django.db.models import Max
from django.utils import timezone # 导入 timezone 模块
from django.contrib.auth.models import AbstractUser

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


# --- 用户模型 ---

class User(AbstractUser):
    """
    自定义用户模型，添加手机号字段和OAuth支持
    """
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # OAuth相关字段
    github_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    google_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    avatar_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.username
    
    def get_avatar_url(self):
        """获取用户头像URL"""
        if self.avatar_url:
            return self.avatar_url
        # 从OAuth提供商获取头像
        try:
            from allauth.socialaccount.models import SocialAccount
            social_account = SocialAccount.objects.filter(user=self).first()
            if social_account:
                if social_account.provider == 'github':
                    return social_account.extra_data.get('avatar_url', '')
                elif social_account.provider == 'google':
                    return social_account.extra_data.get('picture', '')
        except:
            pass
        return None
    
    def get_display_name(self):
        """获取显示名称"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        else:
            return self.username


# --- 模型定义 ---

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', '待处理'
        PROCESSING = 'processing', '处理中'
        COMPLETED = 'completed', '已完成'
        CANCELLED = 'cancelled', '已取消'

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, help_text="关联用户")
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
     # --- ▼▼▼ 修正后的代码 ▼▼▼ ---

    # 1. 定义选择项的嵌套类 (这是推荐的 Django 实践)
    class PaperSizeChoices(models.TextChoices):
        A4 = 'a4', 'A4'
        B5 = 'b5', 'B5'
        A4_70G = 'a4_70g', 'A4(70g)'
        A4_80G = 'a4_80g', 'A4(80g)'
        B5_70G = 'b5_70g', 'B5(70g)'

    class PrintSidedChoices(models.TextChoices):
        SINGLE = 'single', '单面打印'
        DOUBLE = 'double', '双面打印'
        SINGLE_DOUBLE = 'single_double', '封面单面'

    group = models.ForeignKey(BindingGroup, related_name='documents', on_delete=models.CASCADE, help_text="所属装订组")
    original_filename = models.CharField(max_length=255)
    file_path = models.FileField(upload_to=get_order_document_path, help_text="文件存储路径")
    
    color_mode = models.CharField(max_length=20, default='black_white', help_text="色彩模式")
    
    # 2. 【修正】确保字段正确引用嵌套类
    print_sided = models.CharField(
        max_length=20,
        choices=PrintSidedChoices.choices,  # <-- 引用 PrintSidedChoices 类的 .choices 属性
        default=PrintSidedChoices.SINGLE,
        help_text="单双面"
    )
    
    # 3. 【修正】确保字段正确引用嵌套类
    paper_size = models.CharField(
        max_length=10,
        choices=PaperSizeChoices.choices, # <-- 引用 PaperSizeChoices 类的 .choices 属性
        default=PaperSizeChoices.A4_70G,
        help_text="纸张尺寸"
    )
    
    copies = models.PositiveIntegerField(default=1, help_text="打印份数")
    page_count = models.PositiveIntegerField(help_text="文件页数")
    # 新增：记录页数来源（estimated/exact）
    class PageCountSource(models.TextChoices):
        ESTIMATED = 'estimated', '预估'
        EXACT = 'exact', '精确'

    page_count_source = models.CharField(
        max_length=16,
        choices=PageCountSource.choices,
        default=PageCountSource.ESTIMATED,
        help_text="页数来源（预估/精确）",
    )
    print_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="此文件的打印费用")
    sequence_in_group = models.PositiveIntegerField(default=0, help_text="文件在组内的顺序")
    
    # (可选但推荐) 新增 display 属性，方便模板和后台调用
    @property
    def print_sided_display(self):
        return self.get_print_sided_display()

    @property
    def paper_size_display(self):
        return self.get_paper_size_display()

    @property
    def page_count_source_display(self):
        return self.get_page_count_source_display()
        
    # --- ▲▲▲ 修正代码结束 ▲▲▲ ---
    
    class Meta:
        ordering = ['sequence_in_group']

    def __str__(self):
        return f"Document {self.original_filename} in Group {self.group.id}"