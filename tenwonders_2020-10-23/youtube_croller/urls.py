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
from main.views import main,work_create,work_delete,work_detail,notice_create,notice_detail,notice_delete
from main.views import meeting,meeting_create,meeting_detail,meeting_delete,internal_search,assign_worker,exclude_worker
from login.views import login,logout,signup
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',main,name='home'),
    path('',login, name='login'),
    path('logout/',logout, name='logout'),
    path('sign_up/',signup, name='signup'),
    path('work_create/',work_create,name='work_create'),
    path('work_detail/<int:work_id>',work_detail,name='work_detail'),
    path('work_delete/<int:work_id>',work_delete,name='work_delete'),
    path('notice_create/',notice_create,name="notice_create"),
    path('notice_detail/<int:notice_id>', notice_detail, name="notice_detail"),
    path('notice_delete/<int:notice_id>', notice_delete, name='notice_delete'),
    path('meeting/',meeting,name="meeting"),
    path('meeting_create/',meeting_create,name='meeting_create'),
    path('meeting_detail/<int:meeting_id>',meeting_detail,name="meeting_detail"),
    path('meeting_delete/<int:meeting_id>',meeting_delete,name="meeting_delete"),
    path('internal_search/',internal_search,name="internal_search"),
    path('assign_worker/<int:work_id><int:worker_id>',assign_worker,name="assign_worker"),
    path('exclude_worker/<int:work_id><int:worker_id>',exclude_worker,name='exclude_worker'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
