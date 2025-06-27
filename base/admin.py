from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import HomeSlide, Blog, Images, Hall, Excos, Comment, Lecturer

# Register your models here.
class BlogAdmin(ModelAdmin):
    list_display = ['title', 'category', 'created']


class LecturerAdmin(ModelAdmin):
    list_display = ['full_name', 'phone_no', 'email', 'status', 'qualifications']
    list_display_links = ['full_name', 'phone_no', 'email', 'status', 'qualifications']
    search_fields = ['full_name', 'phone_no']
    list_filter = ['status']



admin.site.register(HomeSlide)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Images)
admin.site.register(Hall)
admin.site.register(Excos)
admin.site.register(Comment)
admin.site.register(Lecturer, LecturerAdmin) 