from django.db import models
from user_auth.models import User

# Create your models here.
class Forum(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    views = models.ManyToManyField(User, blank=True, related_name='post_views')
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    saved = models.ManyToManyField(User, related_name='post_saved', blank=True)
    repost = models.ManyToManyField(User, related_name='repost', blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='owner')
    comment_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.title}'
    
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





class SaveItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Forum, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user}' 
    
    class Meta:
        ordering = ['-added']



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sender')
    post = models.ForeignKey(Forum, on_delete=models.CASCADE, null=True, blank=True, related_name='post')
    status = models.CharField(max_length=50)
    isRead = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user }'
    

    class Meta:
        ordering = ['-created']











