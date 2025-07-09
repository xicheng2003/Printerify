from rest_framework import serializers
from .models import Order, PrintFile, generate_pickup_code
from .pricing import get_price, calculate_pages

class PrintFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintFile
        fields = ['file', 'uploaded_at']

class PrintFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintFile
        fields = ['id', 'file', 'purpose']
        extra_kwargs = {'purpose': {'required': False}}

class OrderSerializer(serializers.ModelSerializer):
    # --- 关键修改：新增一个只读字段，用于展示过滤后的打印文件 ---
    printable_files = serializers.SerializerMethodField()
    
    file_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    payment_screenshot_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'pickup_code', 'phone_number', 'status', 
            'specifications', 'total_price', 'created_at', 'updated_at',
            'printable_files', # <-- 使用新的字段
            'file_ids', 'payment_screenshot_id'
        ]
        read_only_fields = ['order_number', 'total_price', 'status', 'pickup_code']

    # --- 新增方法：定义如何获取 printable_files 的数据 ---
    def get_printable_files(self, obj):
        # 从一个订单的所有关联文件中，只筛选出用途为'PRINT'的文件
        print_files = obj.files.filter(purpose='PRINT')
        # 使用PrintFileSerializer来序列化这些过滤后的文件
        return PrintFileSerializer(print_files, many=True).data

    def create(self, validated_data):
        file_ids = validated_data.pop('file_ids', [])
        screenshot_id = validated_data.pop('payment_screenshot_id', None)
        
        # --- 关键修正：在创建订单前，先生成取件码 ---
        pickup_code, pickup_code_num = generate_pickup_code()
        validated_data['pickup_code'] = pickup_code
        validated_data['pickup_code_num'] = pickup_code_num

        # --- 关键修改：同样调用唯一的计价中心 ---
        specs = validated_data.get('specifications', {})
        
        total_pages = 0
        if file_ids:
            files_to_process = PrintFile.objects.filter(id__in=file_ids, purpose='PRINT')
            for f in files_to_process:
                total_pages += calculate_pages(f.file)
        
        # 调用计价中心获取价格
        total_price = get_price(specs, total_pages)
        validated_data['total_price'] = total_price
        
        # 创建订单实例
        order = Order.objects.create(**validated_data)
        
        # 关联文件
        if file_ids:
            # 复用查询结果，避免二次查询
            files_to_process.update(order=order)
        
        if screenshot_id:
            try:
                screenshot_file = PrintFile.objects.get(id=screenshot_id, order__isnull=True, purpose='PAYMENT')
                screenshot_file.order = order
                screenshot_file.save()
            except PrintFile.DoesNotExist:
                print(f"警告：未找到ID为 {screenshot_id} 的待关联付款截图")
        
        return order