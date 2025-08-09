# printerify/api/serializers.py

from rest_framework import serializers
from django.db import transaction  # 导入数据库事务处理
from .models import Order, BindingGroup, Document, generate_pickup_code
from .services import pricing  # 假设您的计费逻辑在 services/pricing.py 中
from django.core.files import File # <-- 【新增】导入Django的File对象
from pathlib import Path          # <-- 【新增】导入Path对象
from django.conf import settings  # <-- 【新增】导入settings
# 【新增】导入我们的Celery任务
from .tasks import process_order_creation_tasks 

# --- 嵌套序列化器：用于处理层级关系 ---

# --- ▼▼▼ DocumentCreateSerializer 已修改 ▼▼▼ ---
class DocumentCreateSerializer(serializers.Serializer):
    """
    用于在创建订单时，接收单个文件信息的"子序列化器"。
    【已更新】增加了 paper_size 并更新了 print_sided 的选项。
    """
    file_id = serializers.CharField()
    original_filename = serializers.CharField()
    color_mode = serializers.ChoiceField(choices=['black_white', 'color'])
    # 使用 Document 模型中定义的常量，确保前后端一致
    print_sided = serializers.ChoiceField(choices=Document.PrintSidedChoices.values)
    paper_size = serializers.ChoiceField(choices=Document.PaperSizeChoices.values)
    copies = serializers.IntegerField(min_value=1)
    sequence_in_group = serializers.IntegerField()
# --- ▲▲▲ 修改结束 ▲▲▲ ---

class BindingGroupCreateSerializer(serializers.Serializer):
    """
    用于在创建订单时，接收单个装订组信息的"子序列化器"。
    """
    binding_type = serializers.CharField()
    sequence_in_order = serializers.IntegerField()
    documents = DocumentCreateSerializer(many=True) # 关键：嵌套了文件序列化器

# --- 主序列化器：用于创建订单 ---

# --- 主序列化器 (create 方法已修改) ---
class OrderCreateSerializer(serializers.ModelSerializer):
    groups = BindingGroupCreateSerializer(many=True, write_only=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    payment_screenshot_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    payment_method = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    class Meta:
        model = Order
        fields = ('id', 'order_number', 'pickup_code', 'status', 'total_price', 'phone_number', 'groups', 'created_at', 'payment_method', 'payment_screenshot_id')
        read_only_fields = ('id', 'order_number', 'pickup_code', 'status', 'total_price', 'created_at')

    def create(self, validated_data):
        groups_data = validated_data.pop('groups')
        phone_number = validated_data.pop('phone_number', None)
        screenshot_id = validated_data.pop('payment_screenshot_id', None)
        payment_method = validated_data.pop('payment_method', None)

        with transaction.atomic():
            pickup_code_str, pickup_code_num_val = generate_pickup_code()
            order = Order.objects.create(
                total_price=0,
                phone_number=phone_number,
                pickup_code=pickup_code_str,
                pickup_code_num=pickup_code_num_val,
                payment_method=payment_method
            )

            #【修改后】总价从我们定义的基础服务费开始计算
            total_order_price = pricing.PRICE_CONFIG.get('base_service_fee', 0)

            if screenshot_id:
                temp_screenshot_path = Path(settings.MEDIA_ROOT) / 'payments' / screenshot_id
                if temp_screenshot_path.exists():
                    with open(temp_screenshot_path, 'rb') as f:
                        django_file = File(f)
                        # Django会自动使用模型中定义的upload_to函数来决定最终存储位置
                        order.payment_screenshot.save(screenshot_id, django_file, save=False) # save=False避免重复保存
                    temp_screenshot_path.unlink() # 删除临时文件

            for group_data in groups_data:
                documents_data = group_data.pop('documents')
                group = BindingGroup.objects.create(order=order, **group_data)
                
                total_group_print_cost = 0
                group_total_pages = 0

                for doc_data in documents_data:
                    # 【关键修复】从这里开始，我们重构文件处理逻辑
                    
                    # 1. 定位临时文件
                    temp_file_path_str = doc_data['file_id']
                    temp_file_full_path = Path(settings.MEDIA_ROOT) / temp_file_path_str
                    
                    if not temp_file_full_path.exists():
                        # 如果临时文件找不到，可以跳过或抛出异常
                        continue

                    # 2. 计算价格 (使用临时文件的路径)
                    # --- ▼▼▼ 计价函数调用已修改 ▼▼▼ ---
                    page_count, print_cost = pricing.calculate_document_price(
                        file_path=str(temp_file_full_path),
                        paper_size=doc_data['paper_size'], # 传递 paper_size
                        color_mode=doc_data['color_mode'],
                        print_sided=doc_data['print_sided'],
                        copies=doc_data['copies']
                    )
                    # --- ▲▲▲ 修改结束 ▲▲▲ ---
                    
                    # 3. 创建Document实例，但暂时不关联文件
                    # --- ▼▼▼ Document 实例创建已修改 ▼▼▼ ---
                    document = Document.objects.create(
                        group=group,
                        original_filename=doc_data['original_filename'],
                        page_count=page_count,
                        print_cost=print_cost,
                        color_mode=doc_data['color_mode'],
                        print_sided=doc_data['print_sided'],
                        paper_size=doc_data['paper_size'], # 保存 paper_size 到数据库
                        copies=doc_data['copies'],
                        sequence_in_group=doc_data['sequence_in_group']
                    )
                    # --- ▲▲▲ 修改结束 ▲▲▲ ---
                    
                    # 4. 打开临时文件，并用Django的File对象包装它
                    with open(temp_file_full_path, 'rb') as f:
                        django_file = File(f)
                        # 5. 将File对象保存到模型的FileField中
                        #    Django会自动将其移动到`upload_to`指定的新位置
                        document.file_path.save(doc_data['original_filename'], django_file, save=True)

                    # 6. （可选但推荐）删除临时的文件
                    temp_file_full_path.unlink()

                    total_group_print_cost += print_cost
                    group_total_pages += page_count * doc_data['copies']

                # 计算并保存装订费
                binding_cost = pricing.calculate_binding_cost(
                    binding_type=group.binding_type,
                    page_count=group_total_pages
                )
                group.binding_cost = binding_cost
                group.save()
                
                total_order_price += total_group_print_cost + binding_cost

            order.total_price = total_order_price
            order.save()

            # 【新增】在这里触发异步任务
            # 我们将订单的ID传递给任务
            process_order_creation_tasks.delay(order.id)

            return order

# --- 用于读取/展示订单详情的序列化器 ---

class DocumentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class BindingGroupDetailSerializer(serializers.ModelSerializer):
    documents = DocumentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = BindingGroup
        fields = '__all__'

class OrderDetailSerializer(serializers.ModelSerializer):
    groups = BindingGroupDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__' # 显示所有字段