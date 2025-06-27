from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us', views.about, name='about'),
    path('blogs/', views.blog, name='blog'),
    path('blogs/<str:pk>/details/', views.blog_details, name='blog_details'), 
    path('Examination/halls/', views.halls, name='halls'),
    path('Lecturers/', views.lecturer, name='lecturers'),
    path('Lecturers/<str:pk>', views.lecturer_details, name='lecturers_pop'),
    path('excos/', views.excos, name='excos'),
    path('contact/', views.contact, name='contact'),
    path('pop/<str:pk>/', views.excos_pop, name='pop')
]



