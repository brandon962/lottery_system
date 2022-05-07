"""lottery_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from lottery import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.luck_home, name='luck_home'),
    path('scan', views.myscan, name='scan'),
    path('luck_home', views.luck_home, name='luck_home'),
    path('luck_start', views.luck_start, name='luck_start'),
    path('luck_reset', views.luck_reset, name='luck_reset'),
    path('look_home', views.look_home, name='luck_home'),
    path('look_prize', views.look_prize, name='look_prize'),
    path('look_prize_single', views.look_prize_single, name='look_prize_single'),
    path('look_select_prize', views.look_select_prize, name='look_select_prize'),
    path('all_member', views.users, name='all_member'),
    path('add', views.add, name='add'),
    path('welcome/', views.welcome, name='welcome'),
    path('upload_file', views.uploadFile, name = "uploadFile"),
    path('select_group', views.select_group,name='select_group')
]
