from django.urls import path
from . import views

app_name = "instructor"
urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
]
