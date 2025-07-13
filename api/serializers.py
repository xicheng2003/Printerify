# api/serializers.py

from rest_framework import serializers
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from decouple import config

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
            'printable_files', 'file_ids', 'payment_screenshot_id'
        ]
        read_only_fields = ['order_number', 'total_price', 'status', 'pickup_code']

    def get_printable_files(self, obj):
        print_files = obj.files.filter(purpose='PRINT')
        return PrintFileSerializer(print_files, many=True).data

    def create(self, validated_data):
        file_ids = validated_data.pop('file_ids', [])
        screenshot_id = validated_data.pop('payment_screenshot_id', None)
        
        pickup_code, pickup_code_num = generate_pickup_code()
        validated_data['pickup_code'] = pickup_code
        validated_data['pickup_code_num'] = pickup_code_num

        specs = validated_data.get('specifications', {})
        
        total_pages = 0
        files_to_process = []
        if file_ids:
            files_to_process = PrintFile.objects.filter(id__in=file_ids, purpose='PRINT')
            for f in files_to_process:
                total_pages += calculate_pages(f.file)
        
        total_price = get_price(specs, total_pages)
        validated_data['total_price'] = total_price
        
        order = Order.objects.create(**validated_data)
        
        if file_ids:
            files_to_process.update(order=order)
        
        if screenshot_id:
            try:
                screenshot_file = PrintFile.objects.get(id=screenshot_id, order__isnull=True, purpose='PAYMENT')
                screenshot_file.order = order
                screenshot_file.save()
            except PrintFile.DoesNotExist:
                print(f"警告：未找到ID为 {screenshot_id} 的待关联付款截图")

        # --- 新增：发送邮件提醒 ---
        try:
            admin_email = config('ADMIN_EMAIL', default=None)
            if admin_email:
                # 准备邮件内容
                context = {
                    'order': order,
                    'domain': settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'
                }
                html_message = render_to_string('api/new_order_alert.html', context)
                plain_message = strip_tags(html_message)
                
                # 发送邮件
                send_mail(
                    f'新订单提醒: {order.pickup_code}',
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [admin_email],
                    html_message=html_message,
                    fail_silently=False,
                )
        except Exception as e:
            # 即便邮件发送失败，也不应影响订单的创建
            print(f"邮件发送失败: {e}")

        return order