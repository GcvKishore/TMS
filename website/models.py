from django.db import models


# Create your models here.
class UserContact(models.Model):
    date_time = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField()
    is_open = models.BooleanField()
