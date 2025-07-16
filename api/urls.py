# api/urls.py (最终修复版)

from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 【关键修复】在这里，把 PaymentScreenshotUploadView 添加到导入列表中
from .views import OrderViewSet, FileUploadView, PriceEstimationView, PaymentScreenshotUploadView

# 1. 创建一个路由器
router = DefaultRouter()
# 2. 将 OrderViewSet 注册到路由器，它会自动生成 /orders/, /orders/{pk}/ 等URL
router.register(r'orders', OrderViewSet, basename='order')

# 3. 定义我们所有手写的、独立的URL路径
urlpatterns = [
    # 将路由器的URL包含进来
    path('', include(router.urls)),
    
    # 手动添加我们自定义的API路径
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('estimate-price/', PriceEstimationView.as_view(), name='estimate-price'),
    # --- 【新增】为付款凭证上传添加URL ---
    path('upload-payment/', PaymentScreenshotUploadView.as_view(), name='payment-upload'),
]