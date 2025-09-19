# api/tasks.py (最终完善版)

import traceback
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from decouple import config
from django.template.loader import render_to_string
from django.utils.html import strip_tags


import os
from decimal import Decimal
from pathlib import Path

from .models import Order, BindingGroup, Document  # 导入相关模型
from .services import pricing  # 复用页数与计价逻辑
from .pdf_generator import generate_order_pdf # 【修改】导入新的PDF生成器

@shared_task(bind=True)
def process_order_creation_tasks(self, order_id):
    """
    【已重构】异步处理订单创建后的所有耗时任务。
    """

    try:
        order = Order.objects.get(id=order_id)

        # 任务零：异步精确页数与价格重算（可选，建议生产开启 soffice）
        try:
            if _is_async_recount_enabled():
                _recount_order_pages_and_prices(order)
        except Exception as e:
            print(f"!!! 异步页数/价格重算失败，订单ID: {order.order_number}, 错误: {e}")

        # 任务一：生成并保存PDF
        try:
            pdf_file = generate_order_pdf(order)
            order.order_summary_pdf.save(pdf_file.name, pdf_file, save=True)
        except Exception as e:
            print(f"!!! PDF生成失败，订单ID: {order.order_number}, 错误: {e}")

        # 任务二：发送邮件提醒
        # 2.1 发送管理员邮件提醒 (逻辑不变)
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
            print(f"!!! 管理员邮件发送失败: {e}")

        # 2.2 发送用户订单确认邮件
        try:
            if order.user and order.user.email:
                context = { 'order': order }
                html_message = render_to_string('api/user_order_confirmation.html', context)
                plain_message = strip_tags(html_message)
                send_mail(
                    f'订单确认 - 取件码: {order.pickup_code} | Printerify',
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [order.user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                print(f"✓ 用户订单确认邮件已发送至: {order.user.email}")
            else:
                print(f"! 订单 {order.order_number} 未关联用户或无邮箱地址，跳过用户邮件发送")
        except Exception as e:
            print(f"!!! 用户订单确认邮件发送失败: {e}")
            # 用户邮件发送失败不影响其他任务，只记录错误

        return f"Order {order_id} post-processing finished."

    except Order.DoesNotExist:
        return f"Order {order_id} not found."
    except Exception:
        traceback.print_exc()
        raise

def _is_async_recount_enabled() -> bool:
    """是否开启异步精确页数重算。默认开启（True），可通过 env/settings 关闭。"""
    val = os.getenv('DOCX_ASYNC_RECOUNT_ENABLED', '').strip().lower()
    if val in {'0', 'false', 'no', 'off'}:
        return False
    if val in {'1', 'true', 'yes', 'on'}:
        return True
    try:
        from django.conf import settings  # type: ignore
        return bool(getattr(settings, 'DOCX_ASYNC_RECOUNT_ENABLED', True))
    except Exception:
        return True


def _get_async_recount_timeout() -> int:
    """异步重算时 LibreOffice 转换超时，默认 20s。"""
    v = os.getenv('DOCX_ASYNC_RECOUNT_TIMEOUT', '').strip()
    if v.isdigit():
        return max(1, int(v))
    try:
        from django.conf import settings  # type: ignore
        return int(getattr(settings, 'DOCX_ASYNC_RECOUNT_TIMEOUT', 20))
    except Exception:
        return 20


def _recount_order_pages_and_prices(order: Order) -> None:
    """
    使用 LibreOffice（若可用）对 DOCX 进行更精确的页数计算，并据此重算价格、装订费与订单总价。
    - 仅在文件存在时进行；
    - 对非 DOCX（如 PDF）不必重算（已有准确页数），但允许统一再算一遍以保证一致性；
    - 无 LibreOffice 或转换失败则跳过该文件。
    """
    timeout_sec = _get_async_recount_timeout()

    base_service_fee = pricing.PRICE_CONFIG.get('base_service_fee', Decimal('0.00'))
    new_total_order_price: Decimal = Decimal(str(base_service_fee))

    for group in order.groups.all():
        group_print_cost: Decimal = Decimal('0.00')
        group_total_pages: int = 0

        for doc in group.documents.all():
            # 获取文件物理路径
            try:
                file_path = Path(doc.file_path.path)
            except Exception:
                # 文件不存在或路径无效，跳过
                continue

            # 计算更精确的页数（优先 soffice）
            new_pages = None
            file_lower = str(file_path).lower()
            if file_lower.endswith('.docx'):
                # 优先尝试 LibreOffice
                pages = pricing._docx_pages_via_soffice(str(file_path), timeout_sec=timeout_sec)  # type: ignore[attr-defined]
                if isinstance(pages, int) and pages > 0:
                    new_pages = pages
                else:
                    # 回退到同步路径同样的逻辑（元数据/启发式），确保至少有值
                    try:
                        new_pages = pricing._docx_page_count(str(file_path))  # type: ignore[attr-defined]
                    except Exception:
                        new_pages = doc.page_count or 1
            elif file_lower.endswith('.pdf'):
                try:
                    import fitz
                    with fitz.open(str(file_path)) as pdf:
                        new_pages = int(pdf.page_count)
                except Exception:
                    new_pages = doc.page_count or 1
            else:
                # 其他格式沿用同步计算
                try:
                    new_pages = pricing._calculate_pages(str(file_path))  # type: ignore[attr-defined]
                except Exception:
                    new_pages = doc.page_count or 1

            # 更新文档页数并重算打印费用
            try:
                page_count_to_use = int(new_pages) if new_pages and new_pages > 0 else 1
            except Exception:
                page_count_to_use = doc.page_count or 1

            # 重新计算打印费用（注意：calculate_document_price 已包含 copies 乘法）
            try:
                _, new_print_cost = pricing.calculate_document_price(
                    file_path=str(file_path),
                    paper_size=doc.paper_size,
                    color_mode=doc.color_mode,
                    print_sided=doc.print_sided,
                    copies=doc.copies,
                )
            except Exception:
                # 回退：按单价估算
                try:
                    price_map = pricing.PRICE_CONFIG['print'][doc.paper_size][doc.color_mode]
                    per = price_map.get(doc.print_sided, Decimal('0.00'))
                    new_print_cost = per * Decimal(str(page_count_to_use)) * Decimal(str(doc.copies))
                except Exception:
                    new_print_cost = doc.print_cost

            if doc.page_count != page_count_to_use or doc.print_cost != new_print_cost or doc.page_count_source != Document.PageCountSource.EXACT:
                doc.page_count = page_count_to_use
                doc.print_cost = new_print_cost
                doc.page_count_source = Document.PageCountSource.EXACT
                doc.save(update_fields=['page_count', 'print_cost', 'page_count_source'])

            group_total_pages += page_count_to_use * doc.copies
            group_print_cost += new_print_cost

        # 重算装订费
        try:
            new_binding_cost = pricing.calculate_binding_cost(group.binding_type, group_total_pages)
        except Exception:
            new_binding_cost = group.binding_cost

        if group.binding_cost != new_binding_cost:
            group.binding_cost = new_binding_cost
            group.save(update_fields=['binding_cost'])

        new_total_order_price += group_print_cost + new_binding_cost

    # 更新订单总价
    if order.total_price != new_total_order_price:
        order.total_price = new_total_order_price
        order.save(update_fields=['total_price'])


# 旧的异步任务已不再需要，可以删除