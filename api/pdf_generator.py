# 文件路径: api/pdf_generator.py

from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from weasyprint import HTML
from django.conf import settings
import os

def generate_order_pdf(order):
    """
    根据订单信息生成一个PDF文件。
    """
    context = {'order': order}
    html_string = render_to_string('api/order_summary.html', context)

    # 定义静态文件目录，WeasyPrint会在这里寻找二维码图片
    static_dir = os.path.join(settings.BASE_DIR, 'api', 'static')
    base_url = static_dir

    # 使用WeasyPrint生成PDF，并提供base_url让它能解析相对路径的图片
    html = HTML(string=html_string, base_url=base_url)
    pdf_file = html.write_pdf()

    file_name = f'order_{order.order_number}_summary.pdf'
    django_file = ContentFile(pdf_file, name=file_name)

    return django_file