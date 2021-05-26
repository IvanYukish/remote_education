from django.contrib.postgres.fields import ArrayField
from django.db import models

from user.models import CustomUser


class Lesson(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    published_at = models.DateTimeField()
    pdf_file = models.FileField()

    class Meta:
        abstract = True


class PracticalLesson(Lesson):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='practical_lesson')
    students = ArrayField(models.UUIDField())


class TaskSolving(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='task_solving')
    solution = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)


class Lecture(Lesson):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lecture')
