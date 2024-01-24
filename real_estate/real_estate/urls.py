"""
URL configuration for real_estate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from app import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('properties', views.PropertyViewSet,basename="properties")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('create_user/', views.UserTableView.as_view(), name='create_user'),
    path('login/', views.Login.as_view(), name='login'),
    path('user/<str:user_id>/', views.Userinfo.as_view(), name='user-info'),
    path('user_profile/<str:user_id>/', views.UserDetailsAPIView.as_view(), name='userinfo'),
    path('tenanatdata', views.TenentRentAggrimentCreateView.as_view(), name='tenant-info'),
    path('tntuntdata/<str:tenant_id>', views.Tenantunits.as_view(), name='tntunt-info'),
    path('prodata/', views.PropertyUnitsCreateView.as_view(), name='prodata'),
    path('unitlistview/', views.PropertyUnitsListView.as_view(), name='prod'),
    path('pr/<str:unit_id>/', views.PropertyUnitsCreateView.as_view(), name='prodkata'),

]