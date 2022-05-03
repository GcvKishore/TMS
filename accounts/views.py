from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from .forms import SignUpForm


# Create your views here.
def signUpAs(request):
    return render(request, 'accounts/sign-up-as.html')


def tuteeSignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('website:index')
        else:
            content = {
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'username': request.POST['username'],
                'email': request.POST['email'],
                'username_error': '',
                'password1_error': '',
                'password2_error': '',
                'email_error': '',
            }

            for error in form.errors:
                label = error + '_error'
                content[label] = form.errors[error]

            return render(request, 'accounts/tutee-sign-up.html', content)
    else:
        form = SignUpForm()
        return render(request, 'accounts/tutee-sign-up.html')


def instructorSignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            current_user = User.objects.get(username=username)
            # current_user.is_staff = True
            current_user.save()

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('website:index')
        else:

            content = {
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'username': request.POST['username'],
                'email': request.POST['email'],
                'username_error': '',
                'password1_error': '',
                'password2_error': '',
                'email_error': '',
            }

            for error in form.errors:
                label = error + '_error'
                content[label] = form.errors[error]

            return render(request, 'accounts/instructor-sign-up.html', content)
    else:
        form = SignUpForm()
        return render(request, 'accounts/instructor-sign-up.html')


def forgotPassword(request):
    return render(request, 'accounts/forgot-password.html')
