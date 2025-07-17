from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.staticfiles import finders
from urllib.parse import urlparse
import mimetypes

def generate_order_pdf(order):
    """
    根据订单信息生成PDF文件。
    最终版本：通过提供虚拟 base_url 和增强的 url_fetcher，确保在任何环境下都能稳定运行。
    """

    # 1. 渲染 HTML 模板。
    # 您已经确认模板路径是 'api/order_ordersummary.html'
    context = {'order': order}
    html_string = render_to_string('api/order_summary.html', context)

    # 2. 定义一个增强版的 URL Fetcher
    # 这个函数现在可以处理由 base_url 生成的完整 URL
    def django_url_fetcher(url):
        """
        拦截 WeasyPrint 的所有外部资源请求 (CSS, 图片等)。
        它能将 'app://printerify/static/css/styles.css' 这样的内部 URL
        正确解析为服务器上的真实文件路径。
        """
        # 解析 URL，获取其中的路径部分
        # 例如: 'app://printerify/static/images/qrcode.png' -> '/static/images/qrcode.png'
        parsed_url = urlparse(url)
        path = parsed_url.path

        # 检查路径是否以我们设定的 STATIC_URL 开头
        if path.startswith(settings.STATIC_URL):
            # 计算出相对于静态文件根目录的路径
            # 例如: '/static/images/qrcode.png' -> 'images/qrcode.png'
            static_file_path = path[len(settings.STATIC_URL):]
        else:
            # 如果 URL 不符合预期格式，则抛出错误
            raise IOError(f"URL '{url}' does not match STATIC_URL '{settings.STATIC_URL}'")

        # 使用 Django 的 finders 在所有静态文件目录中查找该文件
        absolute_path = finders.find(static_file_path)

        if absolute_path:
            # 找到文件后，读取内容并猜测其 MIME 类型
            mime_type, _ = mimetypes.guess_type(absolute_path)
            return {
                'string': open(absolute_path, 'rb').read(),
                'mime_type': mime_type or 'application/octet-stream',
            }

        # 如果找不到文件，则抛出清晰的错误
        raise IOError(f"Failed to find static file: '{static_file_path}' (from URL: '{url}')")

    # 3. 创建 HTML 对象，这是关键一步
    # 我们提供一个虚拟的 base_url 来让 WeasyPrint 正确处理所有链接
    # 'app://printerify' 是一个完全虚构的地址，仅用于满足 WeasyPrint 的内部逻辑
    html = HTML(string=html_string, base_url='app://printerify', url_fetcher=django_url_fetcher)

    # 4. 生成 PDF
    # WeasyPrint 会自动通过我们提供的 fetcher 加载 CSS 和图片，无需手动指定
    pdf_bytes = html.write_pdf()

    # 5. 创建 Django ContentFile 以便保存或发送
    file_name = f"order_{order.order_number}_summary.pdf"
    pdf_file = ContentFile(pdf_bytes, name=file_name)

    return pdf_file