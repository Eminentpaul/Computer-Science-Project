from django.db import models
from .utils import imageResize
from user_auth.models import User
from django.utils.safestring import mark_safe
import datetime

categories = (
    ('Campus', 'Campus'),
    ('Education', 'Education'),
    ('Social', 'Social'),
    ('Fellowship', 'Fellowship'),
    ('Research', 'Research')
)


Letcurer_status = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time')
)




    

def get_year_choices():
    current_year = datetime.datetime.now().year
    return [(year, year) for year in range(2024, current_year + 20)]




# Create your models here.
class HomeSlide(models.Model):
    title = models.CharField(max_length=100)
    tag = models.CharField(max_length=300)
    image = models.ImageField(upload_to='home/')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image = imageResize(self.image)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
    
    @property
    def home_image(self):
        return self.image.url
    



class Blog(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=categories) 
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']




class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    comment = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.author
    
    class Meta:
        ordering = ['-created']




class Images(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blogs')

    def save(self, *args, **kwargs):
        if self.image:
            self.image = imageResize(self.image)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def blog_image(self):
        return self.image.url

    class Meta:
        verbose_name = "Images"




class Class_Timetable(models.Model):
    name = models.CharField(max_length=200)
    link = models.URLField()
    image = models.ImageField(upload_to='Halls')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image = imageResize(self.image)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Class Timetable"


class Excos(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    year = models.IntegerField(choices=get_year_choices, default=datetime.datetime.now().year,)
    image = models.ImageField(upload_to='Excos')

    def __str__(self):
        return self.name 
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image = imageResize(self.image)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Excos"
        ordering = ['-year']




class Staff(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='Full Name')
    qualifications = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=500, choices=Letcurer_status, blank=True, null=True)
    citation = models.TextField(blank=True, null=True)
    phone_no = models.CharField(max_length=20, blank=True, null=True, verbose_name='Phone Number')
    email = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='Lecturers')
    is_teaching = models.BooleanField(default=True)



    def __str__(self):
        return self.full_name
    

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 45px; height:auto;" />' % self.image.url)
        else:
            return 'No Image Found' 
    image_tag.short_description = 'Image'
    

    def save(self, *args, **kwargs):
        if self.image:
            self.image = imageResize(self.image)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    
    class Meta:
        ordering = ['status']
        verbose_name_plural = 'Staff List'



class Lab(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='Labs')


    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        if self.image:
            self.image = imageResize(self.image)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


    # class Meta:
    #     verbose_name = 'Lab'


class Class(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='Classes')


    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        if self.image:
            self.image = imageResize(self.image)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


    class Meta:
        verbose_name_plural = 'Classes'



