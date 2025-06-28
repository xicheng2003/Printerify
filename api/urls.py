# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, PrintFileViewSet # 导入PrintFileViewSet
from .views import PriceQuoteView

# 创建一个DefaultRouter实例
# 它会自动为我们注册的ViewSet生成标准的URL路由
router = DefaultRouter()

# 将我们的OrderViewSet注册到router上，并为其指定一个URL前缀'orders'
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'files', PrintFileViewSet, basename='file') # 新增这行，注册文件上传接口

# urlpatterns会自动包含由router生成的所有URL
urlpatterns = [
    path('', include(router.urls)),
    path('price-quote/', PriceQuoteView.as_view(), name='price-quote'), # 新增报价路由
]