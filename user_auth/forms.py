from django.contrib.auth.forms import UserCreationForm
from .models import User 


class UserForm(UserCreationForm):
    pass
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'regno', 'email', 'password1', 'password2']

        