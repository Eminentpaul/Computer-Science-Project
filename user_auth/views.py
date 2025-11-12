from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages as mg
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from .forms import UserForm
from .models import User
import random

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

        if "CS/N" not in regno and "CS/H" not in regno:
            mg.error(request, "Regno is not acceptable")
        else:
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



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        user = User.objects.filter(email=email)

        token = random.randint(5, 10)

        if user.exists():
            
            with get_connection(
                host=settings.EMAIL_HOST, 
                port=settings.EMAIL_PORT,  
                username=settings.EMAIL_HOST_USER, 
                password=settings.EMAIL_HOST_PASSWORD, 
                use_ssl=settings.EMAIL_USE_SSL
            ) as connection:
                subject = "CS - RESET PASSWORD"
                message = f"""
                Click the Link below to change your Password

https://127.0.0.1:8000/User/reset_password/{token}/?p={email}
                """
                email_from = "info@normatrusted.agency"
                receiver = [f'{email}']
                EmailMessage(subject, message, email_from, receiver, connection=connection).send()  


                mg.success(request, 'Password reset link have been sent to your Email')
        else:
            mg.error(request, f'This Emial ({email}) is not registered with us')

    return render(request, 'user_auth/recover-pass.html')


def reset_password(request, pk):
    d = request.GET.get('p')
    user = User.objects.filter(email=d).first()

    if user:
        
        if request.method == 'POST':
            password = request.POST.get('password')
            cpassword = request.POST.get('cpassword')


            if cpassword == password:
                user.set_password(cpassword)
                user.save()

                mg.success(request, 'Reset Password Successful, you can now login')
                return redirect('login')
            else:
                mg.error(request, 'The Passwords are not the same!')
        return render(request, 'user_auth/reset.html')
    else:
        return redirect('/')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/')