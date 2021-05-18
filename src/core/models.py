
from django.db import models
from django.utils import timezone
from django.views.generic import ListView

from user.models import CustomUser

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
    for_student = models.ManyToManyField(CustomUser)


    def get_name(self):
        return self.name_practical


class Test_for_Student(models.Model):
    name_test = models.CharField(max_length=200, null=True)
    questions = models.CharField(max_length=200, null=True)
    answer = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.questions and self.answer

