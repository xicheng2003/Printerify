"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# backend/urls.py

from django.contrib import admin
from django.urls import path, include # 确保导入了 include
from django.conf import settings # 导入settings
from django.conf.urls.static import static # 导入static

urlpatterns = [
    path('admin/', admin.site.urls),
    # 将所有对 'api/' 路径的请求，都转发到 api.urls 文件中去处理
    # 我们之前的测试API可以删掉了
    path('api/', include('api.urls')), 
]
# 只在DEBUG模式下，才让Django处理media文件的URL
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)