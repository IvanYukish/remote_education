from django import forms
from .models import Lecture, Practical

class CreateLecture(forms.ModelForm):

    class Meta:
        model = Lecture
        fields = ['name_lecture', 'description', 'date', 'file_pdf']


