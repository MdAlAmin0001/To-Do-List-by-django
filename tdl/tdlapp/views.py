from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.db.models import Q
from datetime import date, datetime

from django.contrib.auth import get_user_model
from tdlapp.tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from django.core.mail import EmailMessage
from tdl.settings import EMAIL_HOST_USER
import random
from django.core.mail import send_mail


def activate(request,uid64,token):
    User=get_user_model()
    try:
        uid= force_str(urlsafe_base64_decode(uid64))
        user=User.objects.get(pk=uid)

    except:
        user =None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        return redirect('mySigninPage')

    print("account activation: ", account_activation_token.check_token(user, token))

    return redirect('loginpage')


def activateEmail(request,user,to_mail):
    mail_sub='Active your user Account'
    message=render_to_string("template_activate.html",{
        'user': user.username,
        'domain':get_current_site(request).domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
        'protocol':'https' if request.is_secure() else 'http'
    })
    email= EmailMessage(mail_sub, message, to=[to_mail])
    if email.send():
        messages.success(request,f'Dear')
    else:
        message.error(request,f'not')


def signupPage(request):
    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('loginpage')
    else:
        form = Signup()
    return render(request, 'signup.html', {'form': form})



def loginpage(request):
    if request.method == 'POST':
        form = login_form(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            user=authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form=login_form()
    return render(request, 'loginpage.html',{'form':form})

@login_required
def logoutpage(request):
    logout(request)
    return redirect('loginpage')


def home(request):
    if request.user.is_authenticated:
        # Filter tasks for today
        today = date.today()
        today_tasks = Task.objects.filter((Q(user=request.user) & Q(due_date=today)) | (Q(user=request.user) & Q(is_scheduled=True, scheduled_date=today))).order_by('priority', 'is_completed', 'due_date')


    else:
        today_tasks = []

    context = {
        'today_tasks': today_tasks,
    }

    return render(request, 'home.html', context)


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('priority', 'is_completed', 'due_date')
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_create.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_update.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return redirect('task_list')


def taskcomplete(request,id):
    task=get_object_or_404(Task, id=id)
    task.is_completed=True
    task.save()
    return redirect('task_list')

def task_filter_by_priority(request, priority):

    allowed_priorities = ['HIGH', 'MEDIUM', 'LOW']

    if priority.upper() in allowed_priorities:
        tasks = Task.objects.filter(user=request.user, priority=priority.upper()).order_by('is_completed', 'due_date')
    else:
        tasks = Task.objects.filter(user=request.user).order_by('priority', 'is_completed', 'due_date')
    
    return render(request, 'task_list.html', {'tasks': tasks})


def task_filter_by_date(request):
    if request.method == 'GET' and 'due_date' in request.GET:
        due_date_str = request.GET.get('due_date')
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            tasks = Task.objects.filter(user=request.user, due_date=due_date).order_by('priority', 'is_completed')
        except ValueError:
            tasks = Task.objects.filter(user=request.user).order_by('priority', 'is_completed')
    else:
        tasks = Task.objects.filter(user=request.user).order_by('priority', 'is_completed')
    return render(request, 'task_list.html', {'tasks': tasks})

def forgetpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Custom_user.objects.get(email=email)
            otp = random.randint(111111, 999999)
            user.otp_token = otp
            user.save()

            
            subject = f"Important: Your One-Time Password {otp}"

            msg = f"""
            Dear {user.display_name} ,

            We received a request to verify your identity.
            Your one-time password is: {otp}

            Please enter this code to complete your request.

            For your security:

            * Never share your OTP with anyone.
            * This code is valid only for [2 minutes].
            * Delete this email once you've used the OTP.

            If you didn't request this OTP, please contact us immediately

            Sincerely,

            The Developer Team
            """
            from_mail = EMAIL_HOST_USER
            recipient = [email]
            send_mail(
                subject=subject,
                recipient_list=recipient,
                from_email=from_mail,
                message=msg,
            )
            return render(request, 'changepassword.html', {'email': email})
        except Custom_user.DoesNotExist:
            # Email not found in the database
            message = "Email address not found. Please check and try again."
            return render(request, 'forgetpassword.html', {'error_message': message})
    else:
        return render(request, 'forgetpassword.html')


def changepassword(request):
    if request.method == "POST":
        mail = request.POST.get('email')
        otp = request.POST.get('otp')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        user = Custom_user.objects.get(email = mail)
        if user.otp_token != otp:
            return redirect('forgetpassword')
        if password != c_password:
            return redirect('forgetpassword')
        user.set_password(password)
        
        user.save()
        return redirect('loginpage')
    return render(request, 'changepassword.html')
