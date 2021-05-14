"""configure URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Login/', TemplateView.as_view(template_name="index.html")),
    path('', TemplateView.as_view(template_name="index.html")),
    path('IntelligentLighting/DeviceControl/', TemplateView.as_view(template_name="index.html")),
    path('IntelligentLighting/DataAnalysis/', TemplateView.as_view(template_name="index.html")),

    path('api/LoginApi', views.login_api),
    path('api/LogoutApi', views.logout_api),
    path('api/IntelligentLighting/DeviceControlApi/', views.intelligent_light_device_control_api),
    path('api/IntelligentLighting/DataAnalysisApi/', views.intelligent_light_data_analysis_api),
    path('api/IntelligentLighting/TimerTaskManageApi/', views.intelligent_light_timer_task_manage_api),
]
