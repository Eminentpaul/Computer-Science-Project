from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages as mg

from .forms import UserForm
from .models import User

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('forum')
        else: mg.error(request, 'Invalid Email or Password')
    return render(request, 'user_auth/login.html')


def register(request):
    form = UserForm()
    error_msg = []

    if request.method == 'POST':
        regno = request.POST.get('regno').upper()
        if User.objects.filter(regno=regno).first():
            mg.error(request, f"This Regno: {regno} is already taken")
        else:
            form = UserForm(request.POST)

            if form.is_valid():
                user = form.save()
                auth.login(request, user)
                return redirect('forum')
            else:
                errors = form.errors.get_json_data(escape_html=True)
                for error in errors:
                    error_msg = errors[error][0]['message']

                mg.error(request, error_msg)

    return render(request, 'user_auth/signup.html')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/')