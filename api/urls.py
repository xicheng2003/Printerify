# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, FileUploadView, PriceEstimationView, PaymentScreenshotUploadView, UserRegistrationView, UserLoginView, user_logout, user_profile, update_user_profile, user_orders, get_csrf_token

# 1. 创建一个路由器
router = DefaultRouter()
# 2. 将 OrderViewSet 注册到路由器，它会自动生成 /orders/, /orders/{pk}/ 等URL
router.register(r'orders', OrderViewSet, basename='order')

# 3. 定义我们所有手写的、独立的URL路径
urlpatterns = [
    # 将路由器的URL包含进来
    path('', include(router.urls)),
    
    # 用户认证相关URL
    path('csrf/', get_csrf_token, name='csrf-token'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', user_logout, name='user-logout'),
    path('profile/', user_profile, name='user-profile'),
    path('profile/update/', update_user_profile, name='update-user-profile'),
    path('user-orders/', user_orders, name='user-orders'),
    
    # 手动添加我们自定义的API路径
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('estimate-price/', PriceEstimationView.as_view(), name='estimate-price'),
    path('upload-payment/', PaymentScreenshotUploadView.as_view(), name='payment-upload'),
]