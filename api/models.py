# api/models.py

import time
import random
from django.db import models

# 定义一个函数，用于生成唯一的、基于时间的订单号
def generate_order_number():
    """生成格式为 YYYYMMDDHHMMSS + 4位随机数的订单号"""
    return time.strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999))

# 订单模型
class Order(models.Model):
    # 定义订单状态的选项
    # 这是Django推荐的做法，可以避免在代码中使用硬编码的字符串
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', '待处理'
        PRINTING = 'PRINTING', '打印中'
        COMPLETED = 'COMPLETED', '已完成'
        PICKED_UP = 'PICKED_UP', '已取件'
        CANCELLED = 'CANCELLED', '已取消'

    # 订单号：我们使用default参数，让Django在创建新订单时自动调用我们的函数生成订单号
    # unique=True 保证了每个订单号都是独一无二的
    order_number = models.CharField(max_length=20, default=generate_order_number, unique=True, editable=False, verbose_name="订单号")
    
    # 用户手机号：用于订单查询和联系用户
    phone_number = models.CharField(max_length=15, verbose_name="用户手机号")
    
    # 订单状态：使用我们上面定义的选项，并设置一个默认值
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING, verbose_name="订单状态")
    
    # 打印规格：使用JSONField来存储复杂的、不固定的打印设置，如纸张大小、色彩、单双面等
    # 这是一个非常灵活的字段类型
    specifications = models.JSONField(verbose_name="打印规格")
    
    # 订单总价：使用DecimalField来处理货币，避免浮点数精度问题
    # max_digits是总位数，decimal_places是小数位数
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="订单总价")
    
    # 付款截图：ImageField用于存储用户上传的付款截图
    # upload_to参数指定了图片上传后的存储路径，Django会自动创建这些目录
    # blank=True 允许在表单中不填写这个字段，null=True 允许数据库中该字段为NULL
    # verbose_name用于在Django后台显示更友好的字段名
    payment_screenshot = models.ImageField(
        upload_to='screenshots/%Y/%m/%d/', # 截图上传路径
        blank=True, # 允许该字段在表单中为空
        null=True,  # 允许数据库中该字段为NULL
        verbose_name="付款截图"
    )  
    # 创建时间：auto_now_add=True 会在订单创建时自动记录当前时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    # 更新时间：auto_now=True 会在订单每次被保存时自动更新为当前时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        # 这个方法让对象在后台显示时更具可读性
        return f"订单 {self.order_number} - {self.get_status_display()}"


# 打印文件模型
class PrintFile(models.Model):
    class PurposeChoices(models.TextChoices):
        PRINT = 'PRINT', '打印文件'
        PAYMENT = 'PAYMENT', '付款凭证'
    # 关联订单：使用ForeignKey将文件与一个订单关联起来
    # on_delete=models.CASCADE 的意思是，当对应的订单被删除时，这个文件记录也应一同被删除
    # related_name='files' 允许我们通过 order.files 的方式反向查询一个订单下的所有文件
    order = models.ForeignKey(
    Order,
    on_delete=models.SET_NULL, # 当订单被删除时，文件记录的order字段被设为NULL，而不是删除文件记录
    null=True,                 # 允许数据库中该字段为NULL
    blank=True,                # 允许在表单或后台中该字段为空
    related_name='files',
    verbose_name="所属订单"
)
    
    # 文件字段：FileField是专门用来处理文件上传的字段
    # upload_to='print_files/%Y/%m/%d/' 指定了文件上传后存放的路径
    # Django会自动在MEDIA_ROOT目录下创建这些子目录
    file = models.FileField(upload_to='print_files/%Y/%m/%d/', verbose_name="上传的文件")

    # 上传时间
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")

    # 文件用途：使用CharField来存储文件的用途
    # choices参数定义了可选的用途，Django会自动生成一个下拉
    purpose = models.CharField(
        max_length=10, 
        choices=PurposeChoices.choices, 
        default=PurposeChoices.PRINT, 
        verbose_name="文件用途"
    )

    def __str__(self):
        # os.path.basename可以从文件路径中提取文件名
        import os
        return f"文件 {os.path.basename(self.file.name)} (订单: {self.order.order_number})"