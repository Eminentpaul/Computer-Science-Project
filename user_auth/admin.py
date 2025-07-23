from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import User, Profile

# Register your models here.
class UserAdmin(ModelAdmin):
    list_display = ['first_name', 'last_name', 'regno', 'level', 'email']
    list_display_links = ['first_name', 'last_name', 'regno', 'level', 'email']
    list_filter = ['level']
    search_fields = ['first_name', 'last_name', 'regno']
    list_per_page = 50

    readonly_fields = ['password']
    

class ProfileAdmin(ModelAdmin):
    filter_horizontal = ['followers']
    list_per_page = 50
    list_display = ['user', 'facebook', 'instagram', 'tiktok', 'x', 'github']

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)

