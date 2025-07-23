from django.forms import ModelForm
from .models import Forum
from user_auth.models import Profile
from base.models import Blog


class ForumForm(ModelForm):
    class Meta:
        model = Forum
        fields = ['title', 'description']



class EventForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'category', 'description']


class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['facebook', 'instagram', 'x', 'tiktok', 'github', 'state', 'bio', 'image'] 