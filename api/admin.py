# api/admin.py

import zipfile
import io
from django.http import HttpResponse
from django.contrib import admin
from .models import Order, PrintFile

# 创建一个内联类，以便在订单页面直接看到关联的文件
class PrintFileInline(admin.TabularInline):
    model = PrintFile
    extra = 1 # 默认显示一个额外的空文件上传栏

# 为Order模型自定义后台管理界面
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'phone_number', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'phone_number')
    inlines = [PrintFileInline] # 将文件内联显示
    
    # 添加自定义动作
    actions = ['download_selected_files']

    @admin.action(description='下载选中订单的打印文件')
    def download_selected_files(self, request, queryset):
        # 创建一个内存中的字节流缓冲区
        zip_buffer = io.BytesIO()
        
        # 使用 with 语句，并确保变量名正确 (zip_file)
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            # 确保下面的循环有正确的缩进
            for order in queryset:
                for print_file in order.files.all():
                    # 准备要写入zip包内的文件名
                    file_name_in_zip = f"{order.order_number}/{print_file.file.name.split('/')[-1]}"
                    
                    # 使用正确的变量名 'zip_file' 来写入文件
                    zip_file.writestr(file_name_in_zip, print_file.file.read())

        # 准备HTTP响应
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="selected_files.zip"'
        return response

# 也单独注册PrintFile模型，以便单独管理
@admin.register(PrintFile)
class PrintFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'file', 'uploaded_at')
    search_fields = ('order__order_number',)