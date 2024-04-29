from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.contrib import messages
from django.http import HttpResponse
from .utils import send_otp
from datetime import datetime, timedelta
import pyotp

from django.core.mail import send_mail
from django.conf import settings
from polls.models import *

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            email = request.user.email

            #send one time password
            #send_otp(request)
            totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
            otp = totp.now()
            request.session['otp_secret_key'] = totp.secret
            valid_date = datetime.now() + timedelta(minutes=1)
            request.session['otp_valid_date'] = str(valid_date)

            print(f"Your confirmation password is {otp}")
            print(f"OTP {otp}")

            #FOR SENDING EMAIL TO THE USER
            recipient_list_email = email
            print(f"EMAIL {recipient_list_email}")
            subject = "Students Polling System"
            message = f"Hello {username}, Your confirmation codes is {otp}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [recipient_list_email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            # mwisho wa kusend one time password


            request.session['username'] = username

            redirect_url = request.GET.get('next', 'register_device')
            messages.success(request, "You have registered successfully")
            return redirect(redirect_url)
        else:
            messages.error(request, "Username Or Password is incorrect!!",
                           extra_tags='alert alert-warning alert-dismissible fade show')
            return redirect(register_device)

    # return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('run_uvicorn')

# def create_user(request):

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         password2 = request.POST.get('password2')
#         Course = request.POST.get('Course')
#         Year = request.POST.get('Year')
#         #role = request.POST['role']

#         if password == password2:
#             if MyUser.objects.filter(email=email).exists():
#                 messages.info(request, f"Email {email} Already Taken")
#                 return redirect('register')
#             elif MyUser.objects.filter(username=username).exists():
#                 messages.info(request, f"Username {username} Already Taken")
#                 return redirect('register')
#             else:
#                 user = MyUser.objects.create_user(
#                     username=username, 
#                     email=email, 
#                     password=password, 
#                     Course=Course, 
#                     Year=Year
#                     )
#                 user.save()


#                 #HIZI NI KWA AJILI KUTUMA EMAIL ENDAPO MTU AKIJISAJILI
#                 username = request.POST.get('email')
#                 #last_name = request.POST['last_name']
#                 email = request.POST.get('email')
#                 subject = "Welcome To Students Polling System"
#                 message = f"Ahsante  {username} kwa kujisajili kwenye mfumo wetu kama {username} email yako {email} "
#                 from_email = settings.EMAIL_HOST_USER
#                 recipient_list = [email]
#                 send_mail(subject, message, from_email, recipient_list, fail_silently=True)



                

                
#                 return redirect('login')
#         else:
#             messages.info(request, 'The Two Passwords Not Matching')
#             return redirect('register')

#     else:
#         return render(request, 'accounts/register.html')



def UserRegistrationView(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            
            email = request.POST.get('email')
            username = request.POST.get('username')

            
            #HIZI NI KWA AJILI KUTUMA EMAIL ENDAPO MTU AKIJISAJILI
            
            subject = "Welcome To Students Polling System"
            message = f"Ahsante  {username} kwa kujisajili kwenye mfumo wetu kama {username} email yako {email} "
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)


            messages.success(request, f'{username} is registered successfully')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {
        "form": form
    }
    return render(request, 'accounts/register.html', context)

# def create_user(request):
#     if request.method == 'POST':
#         check1 = False
#         check2 = False
#         check3 = False
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password1 = form.cleaned_data['password1']
#             password2 = form.cleaned_data['password2']
#             email = form.cleaned_data['email']

#             if password1 != password2:
#                 check1 = True
#                 messages.error(request, 'Password doesn\'t matched')
#             if User.objects.filter(username=username).exists():
#                 check2 = True
#                 messages.error(request, 'Username already exists')
#             if User.objects.filter(email=email).exists():
#                 check3 = True
#                 messages.error(request, 'Email already registered')

#             if check1 or check2 or check3:
#                 messages.error(
#                     request, "Registration Failed")
#                 return redirect('register')
#             else:
#                 user = User.objects.create_user(
#                     username=username, password=password1, email=email)
#                 messages.success(
#                     request, f'Thanks for registering {user.username}!')
#                 return redirect('login')
#     else:
#         messages.info(
#                     request, f'Registration failed!')
#         form = UserRegistrationForm()
#     return render(request, 'accounts/register.html', {'form': form})
