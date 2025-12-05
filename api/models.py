# printerify/api/models.py (最终版，包含自定义文件路径)

import time
import random
import string
from django.db import models, transaction, IntegrityError
from django.db.models import Max, Q, UniqueConstraint
from django.utils import timezone # 导入 timezone 模块
from django.contrib.auth.models import AbstractUser

# --- 核心业务逻辑函数 ---

def generate_order_number():
    """生成格式为 YYYYMMDDHHMMSS + 4位随机数的订单号"""
    return time.strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999))

def generate_pickup_code():
    """
    生成一个在有效订单中唯一的取件码 (P-010 to P-999)。
    采用随机生成策略，避免因历史订单删除导致号码回退或重复的误导。
    """
    from .models import Order

    ACTIVE_STATUSES = [
        Order.StatusChoices.PENDING,
        Order.StatusChoices.PROCESSING,
        Order.StatusChoices.COMPLETED,
    ]
    
    # 尝试生成次数上限，防止极端情况下死循环
    MAX_RETRIES = 50
    
    for _ in range(MAX_RETRIES):
        # 随机生成 10 - 999 之间的数字
        # 范围扩大可以显著降低碰撞概率
        next_code_num = random.randint(10, 999)
        code_to_check = f"P-{next_code_num:03d}"
        
        # 检查是否被活跃订单占用
        is_taken = Order.objects.filter(status__in=ACTIVE_STATUSES, pickup_code=code_to_check).exists()

        if not is_taken:
            return code_to_check, next_code_num

    # 如果运气极差（或爆单）导致随机碰撞严重，则降级为顺序查找空缺
    # 从 10 开始找一个没被占用的
    for i in range(10, 1000):
        code_to_check = f"P-{i:03d}"
        if not Order.objects.filter(status__in=ACTIVE_STATUSES, pickup_code=code_to_check).exists():
            return code_to_check, i
            
    # 极度极端情况：所有号码都被占满了（几乎不可能，除非有近1000个未完成订单）
    # 返回一个溢出码或抛出异常，这里选择返回时间戳后三位作为兜底
    fallback_num = int(time.time()) % 1000
    return f"P-{fallback_num:03d}", fallback_num

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
    【新增】订单付款凭证的存储路径
    格式为: payments/YYYY-MM-DD/取件码/原始文件名
    """
    current_date = timezone.now().strftime('%Y-%m-%d')
    pickup_code = instance.pickup_code
    return f'payments/{current_date}/{pickup_code}/{filename}'


def get_package_payment_path(instance, filename):
    """
    套餐购买付款凭证的存储路径
    格式为: package_payments/YYYY-MM-DD/用户ID/文件名
    """
    current_date = timezone.now().strftime('%Y-%m-%d')
    user_id = instance.user_id
    return f'package_payments/{current_date}/{user_id}/{filename}'


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
    
    # 套餐余额字段
    page_balance = models.IntegerField(default=0, help_text="账户页数余额（标准页数）")
    total_pages_purchased = models.IntegerField(default=0, help_text="累计购买页数")
    total_pages_used = models.IntegerField(default=0, help_text="累计使用页数")
    
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
    remark = models.TextField(blank=True, null=True, help_text="用户备注")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['pickup_code'],
                condition=models.Q(status__in=['pending', 'processing', 'completed']),
                name='unique_active_pickup_code'
            )
        ]

    def save(self, *args, **kwargs):
        # 如果没有取件码，尝试生成并保存
        if not self.pickup_code:
            # 使用重试机制处理并发冲突
            max_retries = 5
            for attempt in range(max_retries):
                code_str, code_num = generate_pickup_code()
                self.pickup_code = code_str
                self.pickup_code_num = code_num
                try:
                    # 使用 savepoint 确保如果失败可以回滚而不影响外层事务
                    with transaction.atomic():
                        super().save(*args, **kwargs)
                    return # 保存成功，退出
                except IntegrityError:
                    # 只有在最后一次尝试失败时才抛出异常
                    if attempt == max_retries - 1:
                        raise
                    # 否则重置取件码并继续下一次尝试
                    self.pickup_code = ''
                    self.pickup_code_num = 0
                    continue
        else:
            super().save(*args, **kwargs)

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


# --- 套餐相关模型 ---

class Package(models.Model):
    """
    套餐模板 - 定义可供购买的打印套餐
    """
    name = models.CharField(max_length=100, help_text="套餐名称，如'基础版'")
    description = models.TextField(blank=True, help_text="套餐描述")
    pages = models.IntegerField(help_text="包含的标准打印页数")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="套餐价格")
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="原价（用于显示优惠）")
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=100, help_text="折扣率（如95表示95折）")
    
    # 套餐有效期配置
    validity_days = models.IntegerField(null=True, blank=True, help_text="有效期（天数），空表示永久有效")
    
    # 套餐状态
    is_active = models.BooleanField(default=True, help_text="是否启用该套餐")
    is_featured = models.BooleanField(default=False, help_text="是否推荐套餐（在列表中突出显示）")
    
    # 排序和分类
    sort_order = models.IntegerField(default=0, help_text="排序权重（越小越靠前）")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', 'price']
        verbose_name = "打印套餐"
        verbose_name_plural = "打印套餐"
    
    def __str__(self):
        return f"{self.name} - {self.pages}页 ¥{self.price}"
    
    @property
    def price_per_page(self):
        """计算每页成本"""
        if self.pages > 0:
            return float(self.price) / self.pages
        return 0
    
    @property
    def savings(self):
        """计算节省金额"""
        if self.original_price:
            return float(self.original_price) - float(self.price)
        return 0


class UserPackage(models.Model):
    """
    用户已购套餐记录 - 记录用户购买的套餐及使用情况
    """
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', '待支付'
        ACTIVE = 'active', '使用中'
        EXPIRED = 'expired', '已过期'
        EXHAUSTED = 'exhausted', '已用完'
        CANCELLED = 'cancelled', '已取消'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='packages', help_text="购买用户")
    package = models.ForeignKey(Package, on_delete=models.PROTECT, help_text="套餐类型")
    
    # 购买信息
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="实际支付价格")
    pages_total = models.IntegerField(help_text="套餐总页数")
    pages_remaining = models.IntegerField(help_text="剩余页数")
    
    # 支付信息
    payment_method = models.CharField(max_length=50, blank=True, null=True, help_text="支付方式")
    payment_screenshot = models.FileField(upload_to=get_package_payment_path, blank=True, null=True, help_text="支付凭证")
    
    # 时间信息
    purchased_at = models.DateTimeField(auto_now_add=True, help_text="购买时间")
    activated_at = models.DateTimeField(null=True, blank=True, help_text="激活时间（审核通过后）")
    expires_at = models.DateTimeField(null=True, blank=True, help_text="过期时间")
    
    # 状态
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING, help_text="套餐状态")
    
    # 备注
    remark = models.TextField(blank=True, null=True, help_text="备注信息")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-purchased_at']
        verbose_name = "用户套餐"
        verbose_name_plural = "用户套餐"
    
    def __str__(self):
        return f"{self.user.username} - {self.package.name} ({self.status})"
    
    @property
    def is_valid(self):
        """检查套餐是否有效（未过期且有剩余页数）"""
        if self.status != self.StatusChoices.ACTIVE:
            return False
        if self.pages_remaining <= 0:
            return False
        if self.expires_at and timezone.now() > self.expires_at:
            return False
        return True
    
    def activate(self):
        """激活套餐（审核通过后调用）"""
        if self.status == self.StatusChoices.PENDING:
            self.status = self.StatusChoices.ACTIVE
            self.activated_at = timezone.now()
            
            # 如果套餐有有效期，计算过期时间
            if self.package.validity_days:
                from datetime import timedelta
                self.expires_at = timezone.now() + timedelta(days=self.package.validity_days)
            
            # 记录激活前的余额
            balance_before = self.user.page_balance
            
            # 更新用户余额
            self.user.page_balance += self.pages_total
            self.user.total_pages_purchased += self.pages_total
            self.user.save()
            
            # 创建交易记录
            Transaction.objects.create(
                user=self.user,
                transaction_type=Transaction.TransactionType.RECHARGE,
                amount=self.purchase_price,
                pages=self.pages_total,
                balance_before=balance_before,
                balance_after=self.user.page_balance,
                user_package=self,
                description=f"套餐充值：{self.package.name}（{self.pages_total}页）"
            )
            
            self.save()
    
    def deduct_pages(self, pages):
        """扣除页数"""
        if pages > self.pages_remaining:
            raise ValueError(f"剩余页数不足：需要{pages}页，剩余{self.pages_remaining}页")
        
        self.pages_remaining -= pages
        
        # 如果用完了，更新状态
        if self.pages_remaining == 0:
            self.status = self.StatusChoices.EXHAUSTED
        
        self.save()


class Transaction(models.Model):
    """
    交易记录 - 记录所有余额变动（充值、消费）
    """
    class TransactionType(models.TextChoices):
        RECHARGE = 'recharge', '充值'
        CONSUME = 'consume', '消费'
        REFUND = 'refund', '退款'
        ADMIN_ADJUST = 'admin_adjust', '管理员调整'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions', help_text="关联用户")
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices, help_text="交易类型")
    
    # 金额和页数
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="交易金额")
    pages = models.IntegerField(help_text="页数变动（正数表示增加，负数表示减少）")
    
    # 余额快照
    balance_before = models.IntegerField(help_text="交易前余额")
    balance_after = models.IntegerField(help_text="交易后余额")
    
    # 关联对象
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions', help_text="关联订单（如果是消费）")
    user_package = models.ForeignKey(UserPackage, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions', help_text="关联套餐（如果是充值）")
    
    # 描述
    description = models.TextField(blank=True, help_text="交易描述")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "交易记录"
        verbose_name_plural = "交易记录"
    
    def __str__(self):
        return f"{self.user.username} - {self.get_transaction_type_display()} {self.pages}页"
