from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    if request.user.is_staff:
        return redirect('instructor:dashboard')
    return render(request, 'website/index.html')
