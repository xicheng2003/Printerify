from django.utils import timezone
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay
import logging

logger = logging.getLogger(__name__)

def dashboard_callback(request, context):
    """
    为 Unfold 后台提供仪表盘数据
    """
    try:
        # 延迟导入，避免 AppRegistryNotReady
        from api.models import Order, User
        
        logger.info("Dashboard callback triggered")

        today = timezone.now().date()
        last_7_days = timezone.now() - timezone.timedelta(days=6)

        # --- 1. 关键指标 (KPIs) ---
        pending_count = Order.objects.filter(status='pending').count()
        today_orders = Order.objects.filter(created_at__date=today).count()
        total_revenue = Order.objects.aggregate(sum=Sum('total_price'))['sum'] or 0
        total_users = User.objects.count()

        # --- 2. 图表数据 (Charts) ---
        orders_trend = Order.objects.filter(created_at__gte=last_7_days)\
            .annotate(day=TruncDay('created_at'))\
            .values('day')\
            .annotate(count=Count('id'))\
            .order_by('day')
        
        trend_data_map = {entry['day'].strftime('%Y-%m-%d'): entry['count'] for entry in orders_trend}
        
        labels = []
        data = []
        for i in range(7):
            date = (last_7_days + timezone.timedelta(days=i)).date()
            date_str = date.strftime('%Y-%m-%d')
            labels.append(date.strftime('%m-%d'))
            data.append(trend_data_map.get(date_str, 0))

        # --- 3. 组装 Context ---
        context.update({
            "kpi": [
                {
                    "title": "待处理订单",
                    "metric": pending_count,
                    "footer": "需要尽快处理",
                    "metric_class": "text-red-600 font-bold",
                    "icon": "pending_actions",
                },
                {
                    "title": "今日订单",
                    "metric": today_orders,
                    "footer": f"{today.strftime('%Y-%m-%d')}",
                    "metric_class": "text-blue-600",
                    "icon": "today",
                },
                {
                    "title": "总收入",
                    "metric": f"¥{total_revenue:,.2f}",
                    "footer": "累计流水",
                    "metric_class": "text-purple-600",
                    "icon": "payments",
                },
                {
                    "title": "注册用户",
                    "metric": total_users,
                    "footer": "总用户数",
                    "metric_class": "text-green-600",
                    "icon": "group",
                },
            ],
            "charts": [
                {
                    "title": "近7天订单趋势",
                    "type": "line",
                    "data": {
                        "labels": labels,
                        "datasets": [
                            {
                                "label": "订单数量",
                                "data": data,
                                "borderColor": "#9333ea",
                                "backgroundColor": "rgba(147, 51, 234, 0.1)",
                                "fill": True,
                                "tension": 0.4,
                            }
                        ]
                    },
                    "options": {
                        "responsive": True,
                        "maintainAspectRatio": False,
                        "scales": {
                            "y": {
                                "beginAtZero": True,
                                "ticks": {
                                    "stepSize": 1
                                }
                            }
                        }
                    }
                },
                 {
                    "title": "订单状态分布",
                    "type": "doughnut",
                    "data": {
                        "labels": ["待处理", "处理中", "已完成", "已取消"],
                        "datasets": [
                            {
                                "data": [
                                    Order.objects.filter(status='pending').count(),
                                    Order.objects.filter(status='processing').count(),
                                    Order.objects.filter(status='completed').count(),
                                    Order.objects.filter(status='cancelled').count(),
                                ],
                                "backgroundColor": [
                                    "#ef4444",
                                    "#3b82f6",
                                    "#22c55e",
                                    "#9ca3af",
                                ],
                            }
                        ]
                    }
                }
            ]
        })
        
    except Exception as e:
        logger.error(f"Error in dashboard callback: {e}")
        print(f"Error in dashboard callback: {e}")
    
    return context
