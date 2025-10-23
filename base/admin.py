from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import HomeSlide, Blog, Images, Excos, Comment, Staff, Lab, Class, Course, HOD, Project_Team, Semester, Timetable, Level
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin


# Register your models here.
class BlogAdmin(ModelAdmin):
    list_display = ['title', 'category', 'created']


class TimetableAdmin(ModelAdmin):
    list_display = ['level', 'course', 'start_time', 'end_time', 'day_of_week']
    list_display_links = ['level', 'course', 'start_time', 'end_time', 'day_of_week']


class LecturerAdmin(ImportExportModelAdmin):
    list_display = ['full_name', 'phone_no', 'email', 'status', 'qualifications', 'image_tag']
    list_display_links = ['full_name', 'phone_no', 'email', 'status', 'qualifications']
    search_fields = ['full_name', 'phone_no']
    list_filter = ['status']
    list_per_page = 15




class CourseAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    list_display = ['course_code', 'course_title', 'level', 'semester', 'credit_load', 'lecturer']
    list_display_links = ['course_code', 'course_title', 'semester', 'credit_load']
    search_fields = ['course_code', 'course_title']
    list_filter = ['semester', 'level']
    list_editable = ['lecturer', 'level']
    



class SemesterAdmin(ImportExportModelAdmin):
    list_display = ['id', 'semester']
    list_display_link = ['semester']
    list_editable = ['semester']


class HODAdmin(ImportExportModelAdmin):
    list_display = ['lecturer', 'started', 'ended']
    list_display_links = ['lecturer', 'started', 'ended']
    


class ExcosAdmin(ImportExportModelAdmin):
    list_display = ['name', 'position', 'year', 'image_tag']
    list_display_links = ['name', 'position', 'year']
    search_fields = ['name']
    list_filter = ['position', 'year']



admin.site.register(HomeSlide, ImportExportModelAdmin)
admin.site.register(Blog, BlogAdmin)
# admin.site.register(Images)
admin.site.register(Excos, ExcosAdmin)
admin.site.register(Comment)
admin.site.register(Staff, LecturerAdmin) 
admin.site.register(Lab, ImportExportModelAdmin)
admin.site.register(Class, ImportExportModelAdmin)
admin.site.register(HOD, HODAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Project_Team, ImportExportModelAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Timetable, TimetableAdmin)
admin.site.register(Level)
admin.site.register(Images) 