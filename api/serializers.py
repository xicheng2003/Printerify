# printerify/api/serializers.py

from rest_framework import serializers
from django.db import transaction  # 导入数据库事务处理
from django.contrib.auth import authenticate
from .models import Order, BindingGroup, Document, generate_pickup_code, User, Package, UserPackage, Transaction
from .services import pricing  # 假设您的计费逻辑在 services/pricing.py 中
from django.core.files import File # <-- 【新增】导入Django的File对象
from pathlib import Path          # <-- 【新增】导入Path对象
from django.conf import settings  # <-- 【新增】导入settings
# 【新增】导入我们的Celery任务
from .tasks import process_order_creation_tasks 


# --- 用户认证序列化器 ---

class UserSerializer(serializers.ModelSerializer):
    """
    用户信息序列化器
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'first_name', 'last_name', 'page_balance', 'total_pages_purchased', 'total_pages_used', 'created_at', 'updated_at')
        read_only_fields = ('id', 'page_balance', 'total_pages_purchased', 'total_pages_used', 'created_at', 'updated_at')


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("两次输入的密码不一致")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    用户登录序列化器
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, required=False)
    oauth_provider = serializers.CharField(required=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        oauth_provider = attrs.get('oauth_provider')

        if oauth_provider:
            # OAuth用户登录，不需要密码验证
            try:
                user = User.objects.get(username=username)
                # 验证用户确实有对应的OAuth ID
                if oauth_provider == 'github' and user.github_id:
                    pass  # 验证通过
                elif oauth_provider == 'google' and user.google_id:
                    pass  # 验证通过
                else:
                    raise serializers.ValidationError("OAuth用户验证失败")
            except User.DoesNotExist:
                raise serializers.ValidationError("OAuth用户不存在")
        else:
            # 传统用户名密码登录
            if not password:
                raise serializers.ValidationError("密码是必填项")
            
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("用户名或密码错误")

        attrs['user'] = user
        return attrs


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
    # 接受完整枚举值以及兼容的简写（a4/b5）
    paper_size = serializers.ChoiceField(choices=list(Document.PaperSizeChoices.values))
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
    remark = serializers.CharField(write_only=True, required=False, allow_blank=True)
    use_balance = serializers.BooleanField(write_only=True, required=False, default=False)  # 新增：是否使用余额
    
    class Meta:
        model = Order
        fields = ('id', 'order_number', 'pickup_code', 'status', 'total_price', 'phone_number', 'groups', 'created_at', 'payment_method', 'payment_screenshot_id', 'remark', 'use_balance')
        read_only_fields = ('id', 'order_number', 'pickup_code', 'status', 'total_price', 'created_at')

    def create(self, validated_data):
        groups_data = validated_data.pop('groups')
        phone_number = validated_data.pop('phone_number', None)
        screenshot_id = validated_data.pop('payment_screenshot_id', None)
        payment_method = validated_data.pop('payment_method', None)
        remark = validated_data.pop('remark', '')
        use_balance = validated_data.pop('use_balance', False)  # 新增：是否使用余额
        
        # 获取当前用户（如果已认证）
        user = self.context['request'].user if self.context['request'].user.is_authenticated else None

        with transaction.atomic():
            # 取件码生成逻辑已移至 Order.save() 方法中，以支持并发重试
            order = Order.objects.create(
                user=user,  # 关联用户（如果已登录）
                total_price=0,
                phone_number=phone_number,
                payment_method=payment_method,
                remark=remark
            )

            #【修改后】总价从我们定义的基础服务费开始计算
            total_order_price = pricing.PRICE_CONFIG.get('base_service_fee', 0)
            total_pages_consumed = 0  # 新增：计算总页数消耗

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
                        page_count_source=Document.PageCountSource.ESTIMATED,
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
                    total_pages_consumed += page_count * doc_data['copies']  # 新增：累计总页数

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
            
            # 【新增】余额扣费逻辑
            if use_balance and user and user.is_authenticated:
                # 检查用户余额是否足够
                if user.page_balance >= total_pages_consumed:
                    # 记录扣费前余额
                    balance_before = user.page_balance
                    
                    # 扣除余额
                    user.page_balance -= total_pages_consumed
                    user.total_pages_used += total_pages_consumed
                    user.save()
                    
                    # 创建交易记录
                    Transaction.objects.create(
                        user=user,
                        transaction_type=Transaction.TransactionType.CONSUME,
                        amount=total_order_price,
                        pages=-total_pages_consumed,  # 负数表示消费
                        balance_before=balance_before,
                        balance_after=user.page_balance,
                        order=order,
                        description=f"订单 {order.order_number} 消费 {total_pages_consumed} 页"
                    )
                    
                    # 标记订单已使用余额支付（可选，如果需要区分支付方式）
                    order.payment_method = f"{payment_method} + 余额抵扣" if payment_method else "余额抵扣"
                    order.save()
                else:
                    # 余额不足，抛出异常
                    raise serializers.ValidationError({
                        'use_balance': f'余额不足：需要 {total_pages_consumed} 页，当前余额 {user.page_balance} 页'
                    })

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
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__' # 显示所有字段

    def to_representation(self, instance):
        """
        扩展返回：
        - is_estimated: 订单价格是否仍为预估（任一文档为 estimated 即视为预估）
        - page_count_source: overall 标识（'estimated' | 'exact'）
        - note: 前端友好文案
        """
        data = super().to_representation(instance)
        try:
            any_estimated = False
            # 遍历组内文档，若存在预估则整体为预估
            for group in instance.groups.all():
                for doc in group.documents.all():
                    if getattr(doc, 'page_count_source', 'estimated') != 'exact':
                        any_estimated = True
                        break
                if any_estimated:
                    break

            data['is_estimated'] = any_estimated
            data['page_count_source'] = 'estimated' if any_estimated else 'exact'
            data['note'] = '价格为预估，后台将自动校正' if any_estimated else '价格已精确计算'
        except Exception:
            # 防御式：若出现异常，不影响主体数据
            pass
        return data


# --- 套餐相关序列化器 ---

class PackageSerializer(serializers.ModelSerializer):
    """
    套餐序列化器 - 用于展示套餐信息
    """
    price_per_page = serializers.SerializerMethodField()
    savings = serializers.SerializerMethodField()
    
    class Meta:
        model = Package
        fields = (
            'id', 'name', 'description', 'pages', 'price', 'original_price',
            'discount_rate', 'validity_days', 'is_active', 'is_featured',
            'sort_order', 'price_per_page', 'savings', 'created_at'
        )
        read_only_fields = ('id', 'created_at')
    
    def get_price_per_page(self, obj):
        """计算每页成本"""
        return obj.price_per_page
    
    def get_savings(self, obj):
        """计算节省金额"""
        return obj.savings


class UserPackageSerializer(serializers.ModelSerializer):
    """
    用户套餐序列化器 - 用于展示用户已购套餐
    """
    package_name = serializers.CharField(source='package.name', read_only=True)
    package_info = PackageSerializer(source='package', read_only=True)
    is_valid = serializers.SerializerMethodField()
    
    class Meta:
        model = UserPackage
        fields = (
            'id', 'package', 'package_name', 'package_info', 'purchase_price',
            'pages_total', 'pages_remaining', 'payment_method', 'payment_screenshot',
            'purchased_at', 'activated_at', 'expires_at', 'status', 'remark',
            'is_valid', 'created_at'
        )
        read_only_fields = ('id', 'purchased_at', 'activated_at', 'created_at')
    
    def get_is_valid(self, obj):
        """检查套餐是否有效"""
        return obj.is_valid


class UserPackageCreateSerializer(serializers.ModelSerializer):
    """
    用户套餐创建序列化器 - 用于购买套餐
    """
    payment_screenshot_id = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    class Meta:
        model = UserPackage
        fields = ('package', 'payment_method', 'payment_screenshot_id', 'remark')
    
    def validate_package(self, value):
        """验证套餐是否有效"""
        if not value.is_active:
            raise serializers.ValidationError("该套餐已下架，无法购买")
        return value
    
    def create(self, validated_data):
        """创建套餐购买记录"""
        user = self.context['request'].user
        package = validated_data['package']
        payment_method = validated_data.get('payment_method', '')
        payment_screenshot_id = validated_data.pop('payment_screenshot_id', None)
        remark = validated_data.get('remark', '')
        
        # 创建用户套餐记录
        user_package = UserPackage.objects.create(
            user=user,
            package=package,
            purchase_price=package.price,
            pages_total=package.pages,
            pages_remaining=package.pages,
            payment_method=payment_method,
            remark=remark,
            status=UserPackage.StatusChoices.PENDING
        )
        
        # 处理支付凭证
        if payment_screenshot_id:
            temp_path = Path(settings.MEDIA_ROOT) / 'temp_uploads' / payment_screenshot_id
            if temp_path.exists():
                # 移动文件到正式目录
                with open(temp_path, 'rb') as f:
                    user_package.payment_screenshot.save(temp_path.name, File(f), save=True)
                # 删除临时文件
                temp_path.unlink()
        
        return user_package


class TransactionSerializer(serializers.ModelSerializer):
    """
    交易记录序列化器
    """
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    order_number = serializers.CharField(source='order.order_number', read_only=True, allow_null=True)
    package_name = serializers.CharField(source='user_package.package.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Transaction
        fields = (
            'id', 'user', 'user_username', 'transaction_type', 'transaction_type_display',
            'amount', 'pages', 'balance_before', 'balance_after',
            'order', 'order_number', 'user_package', 'package_name',
            'description', 'created_at'
        )
        read_only_fields = ('id', 'created_at')


class UserBalanceSerializer(serializers.ModelSerializer):
    """
    用户余额信息序列化器
    """
    active_packages = serializers.SerializerMethodField()
    recent_transactions = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'page_balance', 'total_pages_purchased', 
            'total_pages_used', 'active_packages', 'recent_transactions'
        )
        read_only_fields = fields
    
    def get_active_packages(self, obj):
        """获取用户的活跃套餐"""
        active_packages = obj.packages.filter(
            status=UserPackage.StatusChoices.ACTIVE,
            pages_remaining__gt=0
        )
        return UserPackageSerializer(active_packages, many=True).data
    
    def get_recent_transactions(self, obj):
        """获取最近10条交易记录"""
        recent = obj.transactions.all()[:10]
        return TransactionSerializer(recent, many=True).data
