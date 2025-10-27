from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us', views.about, name='about'),
    path('blogs/', views.blog, name='blog'),
    path('blogs/<str:pk>/details/', views.blog_details, name='blog_details'), 
    path('Lecturers/Non-Teaching/', views.non_lecturers, name='non_lecturers'),
    path('Lecturers/', views.lecturer, name='lecturers'),
    path('Lecturers/<str:pk>', views.lecturer_details, name='lecturers_pop'),
    path('excos_year/<str:pk>', views.excos_year, name='excos_year'),
    path('excos/', views.excos, name='excos'),
    path('contact/', views.contact, name='contact'),
    path('courses/all/', views.courses, name='courses'),
    path('courses/all/history/', views.courses_history, name='courses_history'),
    path('course/<str:pk>/all/history/', views.each_course_history, name='each_course_history'),
    path('labs/', views.labs, name='labs'),
    path('Class/Rooms/', views.class_room, name='class_room'),
    path('Class/Rooms/<str:pk>/pop/', views.class_pop, name='class_pop'),
    path('Project/Team/', views.developer, name='developer'),
    path('Project/Team/<str:pk>/pop/', views.developer_pop, name='developer_pop'),
    path('Class/timetable/', views.class_timetable, name='class_timetable'),
    path('Class/timetable/<str:pk>/pop/', views.class_timetable_pop, name='class_timetable_pop'),
    path('pop/<str:pk>/', views.excos_pop, name='pop'),
    path('lap_pop/<str:pk>/', views.lab_pop, name='lab_pop')
]



