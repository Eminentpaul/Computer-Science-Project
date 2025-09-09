from django.urls import path 
from . import views 

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:pk>/', views.reset_password, name='reset_password'),
    path('logout', views.logout, name='logout')
]