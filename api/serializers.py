# api/serializers.py

from rest_framework import serializers
from .models import Order, PrintFile
from PyPDF2 import PdfReader

# ----------------------------------------------------
# 第1部分: PrintFileSerializer，保持不变
# ----------------------------------------------------
class PrintFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintFile
        fields = ['file', 'uploaded_at']

# ----------------------------------------------------
# 第2部分: PrintFileUploadSerializer，保持不变
# ----------------------------------------------------
class PrintFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintFile
        # 同时返回 id, file 和 purpose
        fields = ['id', 'file', 'purpose']
        # purpose 字段是可选的，默认为'PRINT'
        extra_kwargs = {'purpose': {'required': False}}

# ----------------------------------------------------
# 第3部分: OrderSerializer，这是我们需要确保正确的部分
# ----------------------------------------------------
class OrderSerializer(serializers.ModelSerializer):
    # 这是我们自己添加的字段1
    files = PrintFileSerializer(many=True, read_only=True)
    
    # 这是我们自己添加的字段2
    file_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    payment_screenshot_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Order
        
        # 核心修正区域：确保'fields'列表包含了所有字段
        fields = [
            'id', 
            'order_number', 
            'phone_number', 
            'status', 
            'specifications', 
            'total_price', 
            'created_at', 
            'updated_at',
            'files',      # 必须包含字段1
            'file_ids',    # 必须包含字段2
            'payment_screenshot_id'  # 新增字段，用于上传付款截图
        ]
        
        read_only_fields = ['order_number', 'total_price', 'status']

    # 重写create方法以添加计价逻辑
    # 这里我们将根据上传的文件和打印规格来计算订单总价 
    def create(self, validated_data):
        file_ids = validated_data.pop('file_ids', [])
        screenshot_id = validated_data.pop('payment_screenshot_id', None)

        # --- 在这里添加计价逻辑 ---
        calculated_price = 0.0
        # 假设我们有一个计价规则
        price_rules = {'A4_黑白': 0.15, 'A4_彩色': 0.5, 'A3_黑白': 0.2, 'A3_彩色': 1.0}

        specs = validated_data.get('specifications', {})
        copies = specs.get('copies', 1)

        # 找到与此订单关联的文件并计算总页数
        total_pages = 0
        if file_ids:
            files_to_process = PrintFile.objects.filter(id__in=file_ids)
            for f in files_to_process:
                try:
                    # PyPDF2 读取页数
                    reader = PdfReader(f.file)
                    total_pages += len(reader.pages)
                except Exception:
                    # 如果不是pdf或文件损坏，则跳过
                    pass

        # 根据规格计算价格
        key = f"{specs.get('paper_size', 'A4')}_{specs.get('color', '黑白')}"
        price_per_page = price_rules.get(key, 0.1) # 获取单价，如果规格未定义则用默认价
        calculated_price = float(price_per_page) * total_pages * copies

        # 将计算出的价格加入到validated_data中
        validated_data['total_price'] = calculated_price

        order = Order.objects.create(**validated_data)
        
        if file_ids:
            files_to_associate = PrintFile.objects.filter(id__in=file_ids, order__isnull=True, purpose='PRINT')
            files_to_associate.update(order=order)
        
        if screenshot_id:
            try:
                # 之前我们是在Order模型上直接加了ImageField，但后来改成了用PrintFile模型并加purpose字段
                # 所以这里的逻辑应该是去更新PrintFile记录
                screenshot_file = PrintFile.objects.get(id=screenshot_id, order__isnull=True, purpose='PAYMENT')
                screenshot_file.order = order
                screenshot_file.save()
            except PrintFile.DoesNotExist:
                print(f"警告：未找到ID为 {screenshot_id} 的待关联付款截图")

        return order