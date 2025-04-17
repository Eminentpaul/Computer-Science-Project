from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Forum, Comment, SaveItem, Notification


class ForumAdmin(ModelAdmin):
    list_display = ['author', 'title', 'created']


class SavedAdmin(ModelAdmin):
    list_display = ['user', 'item', 'added']
    list_display_links = ['user', 'item']


admin.site.register(Forum, ForumAdmin)
admin.site.register(Comment)
admin.site.register(SaveItem, SavedAdmin)
admin.site.register(Notification)