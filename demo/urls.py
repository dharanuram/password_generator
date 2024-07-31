from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('generate_password/', views.generate_password, name='generate_password'),
    path('logout/', views.user_logout, name='logout'),
]
