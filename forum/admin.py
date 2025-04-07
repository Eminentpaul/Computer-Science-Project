from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Forum, Comment


class ForumAdmin(ModelAdmin):
    list_display = ['author', 'title', 'created']


admin.site.register(Forum, ForumAdmin)
admin.site.register(Comment)