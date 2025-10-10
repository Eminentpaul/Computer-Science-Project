from django.urls import path
from . import views

urlpatterns = [
    path('', views.timetable_dash, name='timetable_dash'),
    path('add/lecture/', views.create_timetable, name='add_lecture'),
    path('edit/<str:pk>/course/', views.edit_course, name='edit_course'),
    path('delete/<str:pk>/course/', views.delete_course, name='delete_course'),
]