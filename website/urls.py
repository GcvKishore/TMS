from django.urls import path
from . import views

app_name = "website"
urlpatterns = [
    path('', views.index, name="index"),
    path('permission-denied', views.permissionDenied, name="permission-denied")

]
