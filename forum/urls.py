from django.urls import path
from . import views

urlpatterns = [
    path('user/<str:pk>/dashboard/', views.dashboard, name='dashboard'),
    path('user/<str:pk>/edit/profile/', views.edit_profile, name='edit_profile'),
    path('', views.forum, name='forum'),
    path('post/', views.forum_post, name='forum_post'),
    path('<str:pk>/post/details/', views.forum_detail, name='forum_detail'),
    path('post/<str:pk>/likes', views.post_like, name='post_like'),
    path('post/<str:pk>/likes/details', views.post_detail_like, name='post_detail_like'),
    path('comment/<str:pk>/<str:pd>/likes',
         views.comment_like, name='comment_like'),
    path('user/<str:pk>/follow', views.follow, name='follow'),
    path('post/<str:pk>/edit', views.edit_forum, name='edit_forum'),
    path('post/<str:pk>/delete', views.delete_post, name='delete')
]