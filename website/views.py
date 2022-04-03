from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def underConstruction(request):
    return render(request, 'website/underConstruction.html')
