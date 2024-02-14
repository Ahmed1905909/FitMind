from django.urls import path
from user import views

urlpatterns = [
path('/register', views.register, name='register'),
path('/login', views.login, name='login'),
path('/admin-dashboard', views.admin_dashboard, name='admin-dashboard'),
path('/logout', views.logout_view, name='logout'),
path('/profile', views.profile , name='profile'),


]
