# api/tasks.py (最终完善版)

import traceback
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from decouple import config
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import traceback  # <--- 1. 请确保导入了这个模块
import logging

logger = logging.getLogger(__name__)


from .models import Order # 【修改】只导入Order
from .pdf_generator import generate_order_pdf # 【修改】导入新的PDF生成器

@shared_task(bind=True)
def process_order_creation_tasks(self, order_id):
    """
    【已重构】异步处理订单创建后的所有耗时任务。
    """
    """处理订单创建后的异步任务，如生成PDF和发送邮件"""
    logger.info(f"开始处理订单ID {order_id} 的后续任务。")
    try:
        order = Order.objects.get(id=order_id)

        # 任务一：生成并保存PDF
        try:
            logger.info(f"正在为订单 {order.order_number} 生成PDF...")
            pdf_file = generate_order_pdf(order)
            logger.info(f"订单 {order.order_number} 的PDF已成功生成。")
            order.order_summary_pdf.save(pdf_file.name, pdf_file, save=True)
        except Order.DoesNotExist:
            logger.error(f"任务失败：找不到订单ID {order_id}。")
        except Exception as e:
            # --- ▼▼▼ 2. 将原来的 except 块替换为下面的代码 ▼▼▼ ---
            # 获取完整的、详细的错误堆栈信息
            detailed_error = traceback.format_exc()
        
            # 使用 logger.error 记录更严重级别的日志，并包含所有细节
            logger.error(f"""
            !!! 任务处理失败 !!!
            订单ID: {order_id}
            错误类型: {type(e).__name__}
            错误信息: {e}
            --- 详细追溯信息 ---
            {detailed_error}
            --------------------
            """)

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