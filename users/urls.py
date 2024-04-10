from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.urls import include


urlpatterns = [
    # path('', views.register, name='register'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LoginView.as_view(next_page='login'), name='logout'),
    # path('users/', include('users.urls')),
    # path('login/', views.login_view, name='login'),  # Ensure you have a corresponding `login_view` in your views.py
    path('', views.home, name='home'),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
    path('submit_course_rankings/', views.submit_course_rankings, name='submit_course_rankings'),
    path('some_error_view/', views.some_error_view, name='some_error_view'),
    path('success/', views.success, name='success'),
    # path('users/success', views.success, name='success'),
    # path('success/<str:username>/', views.success, name='success'),
    # path('register/success/<str:username>/', views.success, name='success'),
    path('logout/', views.custom_logout, name='custom_logout'),
    # path('system/<str:username>/', views.system_view, name='system'),
    path('system/', views.system_view, name='system'),
    path('profile/', views.profile, name='profile'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('rankings/', views.rankings, name='rankings'),

    #
    # path('submit_course_rankings/', views.submit_course_rankings, name='submit_course_rankings'),
    # path('courses_rank/<int:index>/<str:name>/', views.submit_course_rankings, name='courses_rank'),  # Example URL pattern
    # path('success/<str:name>/<int:index>/', views.success, name='success'),
]