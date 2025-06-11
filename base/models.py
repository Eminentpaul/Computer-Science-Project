from django.db import models
from .utils import imageResize
from user_auth.models import User

categories = (
    ('Campus', 'Campus'),
    ('Education', 'Education'),
    ('Social', 'Social'),
    ('Fellowship', 'Fellowship'),
    ('Research', 'Research')
)

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

    
class Hall(models.Model):
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


class Excos(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
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
        verbose_name = "Excos"
