from django.db import models
from django.utils import timezone
from django.views.generic import ListView

# from src.user.models import


class Allstudents():
    pass


class Lecture(models.Model):
    name_lecture = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    download = models.FileField(upload_to='media/')

class Practical(models.Model, ListView):
    name_lecture = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    download = models.FileField(upload_to='media/')
    # take_student = models.Choices(choices=)





