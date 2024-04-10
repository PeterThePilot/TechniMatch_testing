"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.urls import path, include
from django.contrib import admin
from users.views import home
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('register/', include('users.urls')),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    # path('success/<str:username>/', views.success, name='success'),
    path('success/', views.success, name='success'),
    path('submit_course_rankings/', views.submit_course_rankings, name='courses_rank'),
    path('export-courses/', views.export_courses_to_csv, name='export_courses'),
    path('', home, name='home')# Ensure you create a `urls.py` in your users app
]