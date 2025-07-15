# api/tasks.py

import traceback
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from decouple import config
# +++ 添加下面这两行导入语句 +++
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# +++ ---------------------- +++

from .models import Order, PrintFile
from .pdf_generator import generate_order_pdf
from .pricing import calculate_pages

@shared_task(bind=True)
def process_order_creation_tasks(self, order_id):
    """
    异步处理订单创建后的所有耗时任务：生成PDF和发送邮件提醒。
    """
    try:
        order = Order.objects.get(id=order_id)

        # 任务一：生成并保存PDF
        try:
            pdf_file = generate_order_pdf(order)
            order.order_summary_pdf.save(pdf_file.name, pdf_file, save=True)
        except Exception as e:
            print(f"!!! PDF生成失败，订单ID: {order.order_number}, 错误: {e}")
            # 即使失败，也继续发送邮件

        # 任务二：发送邮件提醒
        try:
            admin_email = config('ADMIN_EMAIL', default=None)
            if admin_email:
                context = {
                    'order': order,
                    'domain': settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'
                }
                html_message = render_to_string('api/new_order_alert.html', context)
                plain_message = strip_tags(html_message)
                send_mail(
                    f'新订单提醒: {order.pickup_code}',
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [admin_email],
                    html_message=html_message,
                    fail_silently=False,
                )
        except Exception as e:
            print(f"!!! 邮件发送失败: {e}")

        return f"Order {order_id} post-processing finished."

    except Order.DoesNotExist:
        return f"Order {order_id} not found."
    except Exception:
        traceback.print_exc()
        raise

@shared_task(bind=True)
def calculate_file_pages_task(self, file_id):
    """
    异步计算文件页数并更新到数据库。
    """
    try:
        print_file = PrintFile.objects.get(id=file_id)
        print_file.page_calculation_status = 'PROCESSING'
        print_file.save(update_fields=['page_calculation_status'])

        pages = calculate_pages(print_file.file)

        print_file.pages = pages
        print_file.page_calculation_status = 'COMPLETED'
        print_file.save(update_fields=['pages', 'page_calculation_status'])

        return f"File {file_id} pages calculated: {pages}."
    except PrintFile.DoesNotExist:
        return f"PrintFile {file_id} not found."
    except Exception:
        traceback.print_exc()
        try:
            print_file = PrintFile.objects.get(id=file_id)
            print_file.page_calculation_status = 'FAILED'
            print_file.save(update_fields=['page_calculation_status'])
        except PrintFile.DoesNotExist:
            pass
        raise