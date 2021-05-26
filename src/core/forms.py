from django.forms import ModelForm, ModelMultipleChoiceField

from core.models import Lecture, PracticalLesson
from user.constants import STUDENT
from user.models import CustomUser


class LectureForm(ModelForm):
    class Meta:
        model = Lecture
        fields = ('name', 'description', 'published_at', 'pdf_file')


class PracticalLessonForm(ModelForm):
    students = ModelMultipleChoiceField(queryset=CustomUser.objects.filter(type=STUDENT))

    class Meta:
        model = PracticalLesson
        fields = ('name', 'description', 'published_at', 'pdf_file', 'students')
