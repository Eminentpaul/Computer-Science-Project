from django.forms import ModelForm
from .models import Forum
from user_auth.models import Profile


class ForumForm(ModelForm):
    class Meta:
        model = Forum
        fields = ['title', 'description']


class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['facebook', 'instagram', 'x', 'tiktok', 'github', 'bio', 'image'] 