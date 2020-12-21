"""youtube_croller URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from main.views import main, go_back_and_clean,create_contract,show_record,confirm,delete,wait,delete_contract,celly_btn_info,btn_push,btn_create,btn_delete,notice_create,notice_detail,notice_delete
from login.views import login,logout,signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',main,name='home'),
    path('delete/', go_back_and_clean, name="delete"),
    path('',login, name='login'),
    path('logout/',logout, name='logout'),
    path('sign_up/',signup, name='signup'),
    path('create_contract/',create_contract,name='create_contract'),
    path('contract_board/<int:contract_id>',show_record,name='contract_board'),
    path('confirm/<int:record_id><int:contract_id>',confirm,name='confirm'),
    path('delete/<int:record_id><int:contract_id>',delete,name='delete'),
    path('wait/<int:record_id><int:contract_id>',wait,name='wait'),
    path('delete_contract/<int:contract_id>',delete_contract,name='delete_contract'),
    path('btn_info/<int:btn_id>',celly_btn_info,name='btn_info'),
    path('btn_push/<int:btn_id>',btn_push, name="btn_push"),
    path('btn_create/',btn_create,name='btn_create'),
    path('btn_delete/<int:btn_id>', btn_delete, name='btn_delete'),
    path('notice_create/',notice_create,name="notice_create"),
    path('notice_detail/<int:notice_id>', notice_detail, name="notice_detail"),
    path('notice_delete/<int:notice_id>', notice_delete, name='notice_delete'),
]
