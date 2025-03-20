from django.db import models
from user_auth.models import User

# Create your models here.
class Forum(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    views = models.ManyToManyField(User, blank=True, related_name='post_views')
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    comment_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']

        verbose_name = 'Forum Post'
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Forum, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.first_name
    
    class Meta:
        ordering = ['-created']