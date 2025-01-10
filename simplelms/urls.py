"""
URL configuration for simplelms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from lms_core import views
from lms_core.api import apiv1

urlpatterns = [
    path('api/v1/', apiv1.urls),
    path('admin/', admin.site.urls),
    path('testing/', views.testing),
    path('tambah/', views.addData),
    path('ubah/', views.editData),
    path('hapus/', views.deleteData),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.user_activity_dashboard, name='user_activity_dashboard'),
    path('batch_enroll/<int:course_id>/', views.batch_enroll_students, name='batch_enroll'),
    path('course_analytics/<int:course_id>/', views.course_analytics, name='course_analytics'),
    path('category/add/', views.add_category, name='add_category'),
    path('category/show/', views.show_categories, name='show_categories'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),

    
    path('certificate/<int:course_id>/', views.certificate, name='certificate'),
    path('add_completion/<int:content_id>/', views.add_completion, name='add_completion'),
    path('show_completions/<int:course_id>/', views.show_completions, name='show_completions'),
    path('delete_completion/<int:content_id>/', views.delete_completion, name='delete_completion'),
    path('', views.index, name='index'),
]
