# printerify/api/admin.py (修复了内联显示问题的最终版)

import zipfile
import io
from django.http import HttpResponse
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Order, BindingGroup, Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
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

class DocumentInline(admin.TabularInline):
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
class BindingGroupAdmin(admin.ModelAdmin):
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


class BindingGroupInlineForOrder(admin.TabularInline):
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
class OrderAdmin(admin.ModelAdmin):
    """
    主订单模型的后台管理配置。
    """
    list_display = ('order_number', 'pickup_code', 'phone_number', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'phone_number', 'pickup_code')
    # 【修改】使用我们新的、专门为订单页设计的简化版内联
    inlines = [BindingGroupInlineForOrder]
    readonly_fields = ('order_number', 'pickup_code', 'pickup_code_num', 'phone_number', 'total_price', 'created_at', 'updated_at')
    actions = ['download_selected_files'] # 下载功能不受影响，依然可用

    # 下载功能的代码保持不变，因为它本来就是正确的
    @admin.action(description='下载选中订单的打印文件和详情PDF')
    def download_selected_files(self, request, queryset):
        # ... (此部分代码无需修改) ...
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