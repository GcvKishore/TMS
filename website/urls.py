from django.urls import path
from . import views

app_name = "website"
urlpatterns = [
    path('', views.index, name="index"),
    path('support-center/', views.supportCenter, name="support-center"),
    path('support-center/success', views.supportCenterSuccess, name="support-center-success"),
    path('permission-denied', views.permissionDenied, name="permission-denied")

]
