
from django.db import models
from django.utils import timezone
from django.views.generic import ListView

# Create your models here.
class Lecture(models.Model):
    name_lecture = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    file_pdf = models.FileField(upload_to='media/', null=True)

    def get_name(self):
        return self.name_lecture

class Practical(models.Model):
    name_practical = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    file_pdf = models.FileField(upload_to='media/', null=True)

    def get_name(self):
        return self.name_practical