# api/tasks.py (最终完善版)

import traceback
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from decouple import config
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from .models import Order # 【修改】只导入Order
from .pdf_generator import generate_order_pdf # 【修改】导入新的PDF生成器

@shared_task(bind=True)
def process_order_creation_tasks(self, order_id):
    """
    【已重构】异步处理订单创建后的所有耗时任务。
    """
    # ▼▼▼ 在这里新增一行临时的诊断代码 ▼▼▼
    print(f"--- CELERY DIAGNOSIS: The value of DEFAULT_FROM_EMAIL is: '{settings.DEFAULT_FROM_EMAIL}' ---")
    # ▲▲▲ 诊断代码结束 ▲▲▲

    try:
        order = Order.objects.get(id=order_id)

        # 任务一：生成并保存PDF
        try:
            pdf_file = generate_order_pdf(order)
            order.order_summary_pdf.save(pdf_file.name, pdf_file, save=True)
        except Exception as e:
            print(f"!!! PDF生成失败，订单ID: {order.order_number}, 错误: {e}")

        # 任务二：发送邮件提醒 (逻辑不变)
        try:
            admin_email = config('ADMIN_EMAIL', default=None)
            if admin_email:
                context = { 'order': order }
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

# 旧的异步任务已不再需要，可以删除