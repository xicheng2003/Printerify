# 文件路径: api/admin.py

import zipfile
import io
from django.http import HttpResponse
from django.contrib import admin
from django.utils.html import format_html
from .models import Order, PrintFile

class PrintFileInline(admin.TabularInline):
    model = PrintFile
    extra = 1
    # 设置为只读，避免在订单详情页直接修改
    readonly_fields = ('uploaded_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # 在列表页增加 'order_summary_pdf_link'
    list_display = ('order_number', 'pickup_code', 'phone_number', 'status', 'total_price', 'created_at', 'order_summary_pdf_link')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'phone_number', 'pickup_code')
    inlines = [PrintFileInline]
    # 将订单的核心信息设置为只读，防止误改
    readonly_fields = ('order_number', 'pickup_code', 'pickup_code_num', 'total_price', 'created_at', 'updated_at')
    actions = ['download_selected_files']

    # 在后台列表显示订单详情PDF的链接
    def order_summary_pdf_link(self, obj):
        if obj.order_summary_pdf:
            return format_html('<a href="{}" target="_blank">查看详情PDF</a>', obj.order_summary_pdf.url)
        return "生成中或失败"
    order_summary_pdf_link.short_description = '订单详情PDF'
    order_summary_pdf_link.allow_tags = True


    @admin.action(description='下载选中订单的打印文件和详情PDF')
    def download_selected_files(self, request, queryset):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            for order in queryset:
                # 文件夹以取件码命名，更方便查找
                folder_name = f"{order.pickup_code}_{order.phone_number[-4:]}"

                # 1. 添加打印文件
                for print_file in order.files.filter(purpose='PRINT'):
                    if print_file.file:
                        file_name_in_zip = f"{folder_name}/打印_{print_file.file.name.split('/')[-1]}"
                        zip_file.writestr(file_name_in_zip, print_file.file.read())

                # 2. 添加订单详情PDF
                if order.order_summary_pdf:
                    pdf_name_in_zip = f"{folder_name}/订单详情_{order.order_number}.pdf"
                    zip_file.writestr(pdf_name_in_zip, order.order_summary_pdf.read())

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="printerify_orders.zip"'
        return response

@admin.register(PrintFile)
class PrintFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'file', 'purpose', 'uploaded_at')
    search_fields = ('order__order_number',)
    list_filter = ('purpose',)