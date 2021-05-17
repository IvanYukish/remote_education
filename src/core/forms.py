from django import forms
from .models import Lecture, Practical




class LectureModelForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['name_lecture', 'description', 'date', 'download']

class PracticalModelForms(forms.ModelForm):
    class Meta:
        model = Practical
        fields = ['name_practical', 'description', 'date', 'download', 'take_student']
        widgets = {
            'take_student': forms.ChoiceField(choices=Student.objects.order_by('name'))
        }

