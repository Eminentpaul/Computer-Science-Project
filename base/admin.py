from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import HomeSlide, Blog, Images, Class_Timetable, Excos, Comment, Staff, Lab, Class
from import_export.admin import ImportExportModelAdmin


# Register your models here.
class BlogAdmin(ModelAdmin):
    list_display = ['title', 'category', 'created']


class LecturerAdmin(ImportExportModelAdmin):
    list_display = ['full_name', 'phone_no', 'email', 'status', 'qualifications', 'image_tag']
    list_display_links = ['full_name', 'phone_no', 'email', 'status', 'qualifications']
    search_fields = ['full_name', 'phone_no']
    list_filter = ['status']


class ExcosAdmin(ImportExportModelAdmin):
    list_display = ['name', 'position', 'year']
    list_display_links = ['name', 'position', 'year']
    search_fields = ['name']
    list_filter = ['position', 'year']



admin.site.register(HomeSlide)
admin.site.register(Blog, BlogAdmin)
# admin.site.register(Images)
admin.site.register(Class_Timetable)
admin.site.register(Excos, ExcosAdmin)
admin.site.register(Comment)
admin.site.register(Staff, LecturerAdmin) 
admin.site.register(Lab)
admin.site.register(Class)
