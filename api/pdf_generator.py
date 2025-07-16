# api/pdf_generator.py (最终版)

from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from weasyprint import HTML
from django.conf import settings
import os

def generate_order_pdf(order):
    """
    【已重构】根据新的订单结构和您原来的HTML模板，生成PDF文件。
    """
    # 渲染我们新的 order_summary.html 模板
    context = {'order': order}
    html_string = render_to_string('api/order_summary.html', context)

    # 【复用】您原来的静态文件路径逻辑，非常棒
    static_dir = os.path.join(settings.BASE_DIR, 'api', 'static')
    base_url = static_dir

    # 使用WeasyPrint将HTML字符串转换为PDF
    html = HTML(string=html_string, base_url=base_url)
    pdf_file_content = html.write_pdf()

    # 创建一个Django可以识别的文件对象
    file_name = f'order_{order.order_number}_summary.pdf'
    django_file = ContentFile(pdf_file_content, name=file_name)

    return django_file