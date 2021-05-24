from django.forms import ModelForm, DateTimeField, ModelMultipleChoiceField, \
    modelformset_factory

from core.models import Lecture, PracticalLesson, TestItem, AnswerOptions, TestBase
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


class TestBaseForm(ModelForm):
    class Meta:
        model = TestBase
        fields = ('created_by', 'name', 'duration')


TestItemFormSet = modelformset_factory(
    TestItem, fields=("type", "test_base"), extra=1
)

AnswerOptionsFormSet = modelformset_factory(
    AnswerOptions, fields=("name", "test_item", "correct"), extra=1
)
