from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Forum, Comment, Notification


class ForumAdmin(ModelAdmin):
    list_display = ['author', 'title', 'created']
    list_display_links = ['author', 'title', 'created']


class SavedAdmin(ModelAdmin):
    list_display = ['user', 'item', 'added']
    list_display_links = ['user', 'item']


admin.site.register(Forum, ForumAdmin)
admin.site.register(Comment)
admin.site.register(Notification)