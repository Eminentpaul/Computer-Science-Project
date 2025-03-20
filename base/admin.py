from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import HomeSlide, Blog, Images, Hall, Excos, Comment

# Register your models here.
class BlogAdmin(ModelAdmin):
    list_display = ['title', 'category', 'created']



admin.site.register(HomeSlide)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Images)
admin.site.register(Hall)
admin.site.register(Excos)
admin.site.register(Comment)