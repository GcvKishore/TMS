from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ResetPassword(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    forgot_password_token = models.CharField(max_length=100, unique=True)
    creates_on = models.DateTimeField()
