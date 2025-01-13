from django.urls import path
from .views import signup_view, login_view, home_view
from . import views

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/courses/', views.manage_courses, name='manage_courses'),
    path('admin/resources/', views.manage_resources, name='manage_resources'),
    path('admin/users/', views.manage_users, name='manage_users'),
    path('admin/upload/', views.upload_resource, name='upload_resource'),

]
