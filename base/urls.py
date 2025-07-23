from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us', views.about, name='about'),
    path('blogs/', views.blog, name='blog'),
    path('blogs/<str:pk>/details/', views.blog_details, name='blog_details'), 
    path('Examination/halls/', views.halls, name='halls'),
    path('Lecturers/Non-Teaching/', views.non_lecturers, name='non_lecturers'),
    path('Lecturers/', views.lecturer, name='lecturers'),
    path('Lecturers/<str:pk>', views.lecturer_details, name='lecturers_pop'),
    path('excos_year/<str:pk>', views.excos_year, name='excos_year'),
    path('excos/', views.excos, name='excos'),
    path('contact/', views.contact, name='contact'),
    path('labs/', views.labs, name='labs'),
    path('pop/<str:pk>/', views.excos_pop, name='pop'),
    path('lap_pop/<str:pk>/', views.lab_pop, name='lab_pop')
]



