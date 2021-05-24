from django.contrib.postgres.fields import ArrayField
from django.db import models


from core.constants import TEST_TYPE_CHOICES
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


class TestBase(models.Model):
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lesson_created_by')
    passed_by = ArrayField(models.UUIDField())
    name = models.CharField(max_length=100)
    duration = models.DurationField()


class TestEstimationByType(models.Model):
    type = models.CharField(max_length=50, choices=TEST_TYPE_CHOICES)
    size = models.PositiveIntegerField()
    estimation = models.PositiveIntegerField()
    test_base = models.ForeignKey(TestBase, on_delete=models.CASCADE, related_name='estimation')


class TestItem(models.Model):
    type = models.CharField(max_length=50, choices=TEST_TYPE_CHOICES)
    test_base = models.ForeignKey(TestBase, on_delete=models.CASCADE, related_name='item')


class AnswerOptions(models.Model):
    name = models.CharField(max_length=300)
    test_item = models.ForeignKey(TestItem, on_delete=models.CASCADE, related_name='answer')
    correct = models.BooleanField()
