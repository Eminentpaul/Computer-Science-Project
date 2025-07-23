from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve as mediaserve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('Forum/', include('forum.urls')),
    path('User/', include('user_auth.urls')),
    # path('accounts/', include('allauth.urls')), 
]


# 404 handler
handler404 = 'base.views._404'


urlpatterns.append(re_path(f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$', mediaserve, {'document_root': settings.MEDIA_ROOT}))

urlpatterns += [
    # your other paths here
    re_path(r'^media/(?P<path>.*)$', mediaserve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', mediaserve,{'document_root': settings.STATIC_ROOT}),
]
