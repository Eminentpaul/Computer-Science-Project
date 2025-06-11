from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser
from base.utils import imageResize
import uuid


# Create your models here.
LEVEL = (
    ('ND 1', 'ND 1'),
    ('ND 2', 'ND 2'),
    ('HND 1', 'HND 1'),
    ('HND 2', 'HND 2')
)


class User(AbstractUser):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    regno = models.CharField(max_length=20, null=True)
    level = models.CharField(max_length=20, choices=LEVEL, null=True, blank=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(unique=True)
    

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email' 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def clean(self):
        self.regno = self.regno.upper()
        return self.regno
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"





class Profile(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='Users', default='../media/Users/user-avater.png', null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField(
        User, blank=True, related_name='user_follower')
    facebook = models.URLField(blank=True, null=True)
    instagram = models.CharField(max_length=200, null=True, blank=True)
    x = models.CharField(max_length=200, null=True, blank=True, verbose_name='X/Twitter')
    tiktok = models.CharField(max_length=200, blank=True, null=True)
    github = models.CharField(max_length=200, blank=True, null=True)
    permission = models.BooleanField(default=False)

    
    def __str__(self):
        return self.user.first_name

    @property
    def avatar(self):
        if self.image:
            return self.image.url
        else:
            return f'../static/img/user-avater.png'

    def save(self, *args, **kwargs):
        if self.image:
            self.image = imageResize(self.image)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_profile, sender=User)
post_save.connect(save_profile, sender=User)
