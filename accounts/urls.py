from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = "account"
urlpatterns = [
    path('sign-up', views.signUpAs, name="sign-up-as"),
    path('sign-up/instructor/', views.instructorSignUp, name="sign-up-as-instructor"),
    path('sign-up/tutee/', views.tuteeSignUp, name="sign-up-as-tutee"),
    path('sign-in/', LoginView.as_view(template_name='accounts/sign-in.html'), name="sign-in"),
    path('sign-out/', LogoutView.as_view(), name="sign-out"),
]
