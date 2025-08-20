from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import HomeSlide, Blog, Images, Excos, Comment, Staff, Lab, Class, Course, HOD, Project_Team, Semester
from import_export.admin import ImportExportModelAdmin


# Register your models here.
class BlogAdmin(ModelAdmin):
    list_display = ['title', 'category', 'created']


class LecturerAdmin(ImportExportModelAdmin):
    list_display = ['full_name', 'phone_no', 'email', 'status', 'qualifications', 'image_tag']
    list_display_links = ['full_name', 'phone_no', 'email', 'status', 'qualifications']
    search_fields = ['full_name', 'phone_no']
    list_filter = ['status']
    list_per_page = 15


class CourseAdmin(ImportExportModelAdmin):
    list_display = ['course_code', 'course_title', 'level', 'semester', 'credit_load', 'lecturer']
    list_display_links = ['course_code', 'course_title', 'level', 'semester', 'credit_load']
    search_fields = ['course_code', 'course_title']
    list_filter = ['semester', 'level']
    list_editable = ['lecturer']
    



class SemesterAdmin(ImportExportModelAdmin):
    list_display = ['semester']
    list_display_link = ['semester']
    # list_editable = ['semester']


class HODAdmin(ImportExportModelAdmin):
    list_display = ['lecturer', 'started', 'ended']
    list_display_links = ['lecturer', 'started', 'ended']
    


class ExcosAdmin(ImportExportModelAdmin):
    list_display = ['name', 'position', 'year', 'image_tag']
    list_display_links = ['name', 'position', 'year']
    search_fields = ['name']
    list_filter = ['position', 'year']



admin.site.register(HomeSlide)
admin.site.register(Blog, BlogAdmin)
# admin.site.register(Images)
admin.site.register(Excos, ExcosAdmin)
admin.site.register(Comment)
admin.site.register(Staff, LecturerAdmin) 
admin.site.register(Lab)
admin.site.register(Class)
admin.site.register(HOD, HODAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Project_Team)
admin.site.register(Semester, SemesterAdmin)