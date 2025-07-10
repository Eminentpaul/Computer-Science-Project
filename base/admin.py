from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import HomeSlide, Blog, Images, Hall, Excos, Comment, Lecturer, Lab, Class
from import_export.admin import ImportExportModelAdmin


# Register your models here.
class BlogAdmin(ModelAdmin):
    list_display = ['title', 'category', 'created']


class LecturerAdmin(ImportExportModelAdmin):
    list_display = ['full_name', 'phone_no', 'email', 'status', 'qualifications', 'image_tag']
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
admin.site.register(Lab)
admin.site.register(Class)