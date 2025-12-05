# printerify/api/admin.py (修复了内联显示问题的最终版)

import zipfile
import io
from django.http import HttpResponse
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin, TabularInline
from .models import Order, BindingGroup, Document, User, Package, UserPackage, Transaction
from .tasks import send_order_completion_email

# 注册用户模型
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'phone_number')

@admin.register(Document)
class DocumentAdmin(ModelAdmin):
    """
    独立的“文件”管理页面，方便搜索和查看。
    """
    list_display = ('id', 'original_filename', 'group_info', 'file_link')
    search_fields = ('original_filename', 'group__order__order_code')
    list_per_page = 20

    def group_info(self, obj):
        # 提供一个链接，可以从文件直接跳到其所属的装订组
        group_url = reverse('admin:api_bindinggroup_change', args=[obj.group.id])
        return format_html('<a href="{}">组G{} (订单O{})</a>', group_url, obj.group.id, obj.group.order.id)
    group_info.short_description = '所属组/订单'

    def file_link(self, obj):
        if obj.file_path:
            return format_html('<a href="{}" target="_blank">查看文件</a>', obj.file_path.url)
        return "无文件"
    file_link.short_description = '文件链接'

class DocumentInline(TabularInline):
    """
    文件内联编辑器。
    【重要】它现在将被用在 BindingGroupAdmin 中，而不是嵌套在另一个内联里。
    """
    model = Document
    extra = 0
    # 【修改】在字段列表的最前面，加上顺序号
    fields = ('sequence_in_group', 'original_filename', 'get_file_link', 'color_mode', 'print_sided', 'copies', 'page_count', 'print_cost')
    # 【修改】将顺序号也设为只读
    readonly_fields = ('sequence_in_group', 'original_filename', 'get_file_link', 'page_count', 'print_cost')


    def get_file_link(self, obj):
        if obj.file_path:
            return format_html('<a href="{}" target="_blank">点击查看</a>', obj.file_path.url)
        return "N/A"
    get_file_link.short_description = '查看文件'

    def has_add_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False

@admin.register(BindingGroup)
class BindingGroupAdmin(ModelAdmin):
    """
    【新增】为“装订组”创建独立的管理页面。
    这个页面是解决问题的关键，它会包含文件的内联列表。
    """
    list_display = ('id', 'order_link', 'binding_type', 'binding_cost')
    inlines = [DocumentInline] # 在这里，我们可以安全地使用文件内联
    
    def order_link(self, obj):
        order_url = reverse('admin:api_order_change', args=[obj.order.id])
        return format_html('<a href="{}">{}</a>', order_url, obj.order.order_code)
    order_link.short_description = '所属订单'


class BindingGroupInlineForOrder(TabularInline):
    """
    【修改】这是专门用在“订单”页面里的简化版内联。
    它只显示基本信息和一个跳转链接。
    """
    model = BindingGroup
    extra = 0
    # 【修改】我们在这里已经有 sequence_in_order 了，确保它在第一个位置
    fields = ('sequence_in_order', 'binding_type', 'binding_cost', 'view_documents_link')
    readonly_fields = ('sequence_in_order', 'binding_type', 'binding_cost', 'view_documents_link')
    
    def view_documents_link(self, obj):
        # 生成指向这个装订组独立编辑页面的链接
        group_url = reverse('admin:api_bindinggroup_change', args=[obj.id])
        return format_html('<a href="{}">查看/管理此组的 {} 个文件</a>', group_url, obj.documents.count())
    view_documents_link.short_description = '文件详情'

    def has_add_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    """
    主订单模型的后台管理配置。
    """
    list_display = ('order_number', 'pickup_code', 'phone_number', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'phone_number', 'pickup_code')
    # 【修改】使用我们新的、专门为订单页设计的简化版内联
    inlines = [BindingGroupInlineForOrder]
    readonly_fields = ('order_number', 'pickup_code', 'pickup_code_num', 'phone_number', 'total_price', 'created_at', 'updated_at')
    actions = ['download_selected_files', 'mark_as_completed']

    def save_model(self, request, obj, form, change):
        """
        重写保存逻辑，以便在状态变为“已完成”时触发邮件。
        """
        # 保存前的原始状态
        if obj.pk:
            original_obj = Order.objects.get(pk=obj.pk)
            original_status = original_obj.status
        else:
            original_status = None

        # 调用父类的保存方法，确保数据先被写入数据库
        super().save_model(request, obj, form, change)

        # 检查状态是否从非“已完成”变为了“已完成”
        if obj.status == Order.StatusChoices.COMPLETED and original_status != Order.StatusChoices.COMPLETED:
            # 触发异步邮件任务
            send_order_completion_email.delay(obj.id)

    @admin.action(description='标记选中订单为“已完成”并发送邮件')
    def mark_as_completed(self, request, queryset):
        """
        新增一个后台动作，用于批量标记订单为完成状态。
        """
        updated_count = 0
        for order in queryset:
            if order.status != Order.StatusChoices.COMPLETED:
                order.status = Order.StatusChoices.COMPLETED
                order.save()
                # 直接在循环中为每个订单触发任务
                send_order_completion_email.delay(order.id)
                updated_count += 1
        
        self.message_user(request, f"{updated_count} 个订单已成功标记为“已完成”并触发了邮件通知。")

    # 下载功能的代码保持不变
    @admin.action(description='下载选中订单的打印文件和详情PDF')
    def download_selected_files(self, request, queryset):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            for order in queryset:
                folder_name = f"{order.pickup_code}_{order.phone_number[-4:] if order.phone_number else 'XXXX'}"
                for group in order.groups.all():
                    for document in group.documents.all():
                        if document.file_path:
                            file_name_in_zip = f"{folder_name}/打印_{document.original_filename}"
                            zip_file.writestr(file_name_in_zip, document.file_path.read())
                if order.order_summary_pdf:
                    pdf_name_in_zip = f"{folder_name}/订单详情_{order.order_number}.pdf"
                    zip_file.writestr(pdf_name_in_zip, order.order_summary_pdf.read())
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="printerify_orders.zip"'
        return response


# --- 套餐相关管理页面 ---

@admin.register(Package)
class PackageAdmin(ModelAdmin):
    """
    套餐管理页面
    """
    list_display = ('name', 'pages', 'price', 'discount_rate', 'is_active', 'is_featured', 'sort_order', 'created_at')
    list_filter = ('is_active', 'is_featured', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active', 'is_featured', 'sort_order')
    ordering = ['sort_order', 'price']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'pages', 'price', 'original_price', 'discount_rate')
        }),
        ('有效期设置', {
            'fields': ('validity_days',),
            'description': '留空表示永久有效'
        }),
        ('显示设置', {
            'fields': ('is_active', 'is_featured', 'sort_order')
        }),
    )


@admin.register(UserPackage)
class UserPackageAdmin(ModelAdmin):
    """
    用户套餐管理页面
    """
    list_display = ('id', 'user_link', 'package_name', 'purchase_price', 'pages_total', 'pages_remaining', 'status', 'purchased_at', 'expires_at', 'action_buttons')
    list_filter = ('status', 'purchased_at', 'package')
    search_fields = ('user__username', 'user__email', 'package__name')
    readonly_fields = ('user', 'package', 'purchase_price', 'pages_total', 'pages_remaining', 'purchased_at', 'activated_at', 'payment_screenshot_preview')
    actions = ['activate_packages', 'cancel_packages']
    
    fieldsets = (
        ('用户和套餐信息', {
            'fields': ('user', 'package', 'purchase_price', 'pages_total', 'pages_remaining')
        }),
        ('支付信息', {
            'fields': ('payment_method', 'payment_screenshot', 'payment_screenshot_preview')
        }),
        ('状态和时间', {
            'fields': ('status', 'purchased_at', 'activated_at', 'expires_at')
        }),
        ('备注', {
            'fields': ('remark',)
        }),
    )
    
    def user_link(self, obj):
        """用户链接"""
        user_url = reverse('admin:api_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', user_url, obj.user.username)
    user_link.short_description = '用户'
    
    def package_name(self, obj):
        """套餐名称"""
        return obj.package.name
    package_name.short_description = '套餐'
    
    def payment_screenshot_preview(self, obj):
        """支付凭证预览"""
        if obj.payment_screenshot:
            return format_html('<a href="{}" target="_blank"><img src="{}" style="max-width: 300px; max-height: 200px;" /></a>', 
                             obj.payment_screenshot.url, obj.payment_screenshot.url)
        return "无凭证"
    payment_screenshot_preview.short_description = '支付凭证预览'
    
    def action_buttons(self, obj):
        """操作按钮"""
        if obj.status == UserPackage.StatusChoices.PENDING:
            return format_html(
                '<a class="button" href="{}">审核激活</a>',
                reverse('admin:api_userpackage_change', args=[obj.id])
            )
        return '-'
    action_buttons.short_description = '操作'
    
    @admin.action(description='激活选中的待审核套餐')
    def activate_packages(self, request, queryset):
        """批量激活套餐"""
        activated_count = 0
        for user_package in queryset:
            if user_package.status == UserPackage.StatusChoices.PENDING:
                try:
                    user_package.activate()
                    activated_count += 1
                except Exception as e:
                    self.message_user(request, f"激活套餐 {user_package.id} 失败: {str(e)}", level='error')
        
        if activated_count > 0:
            self.message_user(request, f"成功激活 {activated_count} 个套餐")
    
    @admin.action(description='取消选中的套餐')
    def cancel_packages(self, request, queryset):
        """批量取消套餐"""
        updated = queryset.update(status=UserPackage.StatusChoices.CANCELLED)
        self.message_user(request, f"成功取消 {updated} 个套餐")


@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):
    """
    交易记录管理页面
    """
    list_display = ('id', 'user_link', 'transaction_type', 'pages', 'amount', 'balance_before', 'balance_after', 'order_link', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('user__username', 'user__email', 'order__order_number', 'description')
    readonly_fields = ('user', 'transaction_type', 'amount', 'pages', 'balance_before', 'balance_after', 'order', 'user_package', 'description', 'created_at')
    
    def user_link(self, obj):
        """用户链接"""
        user_url = reverse('admin:api_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', user_url, obj.user.username)
    user_link.short_description = '用户'
    
    def order_link(self, obj):
        """订单链接"""
        if obj.order:
            order_url = reverse('admin:api_order_change', args=[obj.order.id])
            return format_html('<a href="{}">{}</a>', order_url, obj.order.order_number)
        return '-'
    order_link.short_description = '关联订单'
    
    def has_add_permission(self, request):
        """禁止手动添加交易记录"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """禁止删除交易记录"""
        return False