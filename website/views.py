from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .functions import *


# Create your views here.
def index(request):
    if request.user.is_staff:
        return redirect('instructor:dashboard')
    if request.user.is_active:
        return redirect('tutee:dashboard')
    return render(request, 'website/index.html')


def permissionDenied(request):
    return render(request, 'website/permission-denied.html')


def supportCenter(request):
    if request.method == 'POST':
        category = request.POST['subject']
        email = request.POST['email']
        message = request.POST['message']
        UserContact.objects.create(category=category, email=email, message=message, is_open=True)
        if sendUserCopy(request.POST):
            return redirect('website:support-center-success')
    return render(request, 'website/support-center.html')


def supportCenterSuccess(request):
    return render(request, 'website/support-center-success.html')
