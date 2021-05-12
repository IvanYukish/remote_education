from allauth.account.forms import SignupForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import CustomUser


GEEKS_CHOICES = (
    ("1", "Student"),
    ("2", "Teacher"),
)

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(label=_('Ім\'я'), max_length=150,
                                 widget=forms.TextInput(attrs={'placeholder': _('Введіть своє ім\'я')}))
    last_name = forms.CharField(label=_('Last Name'), max_length=150,
                                widget=forms.TextInput(attrs={'placeholder': _('Введіть своє прізвище')}))
    user_role = forms.ChoiceField(choices=GEEKS_CHOICES)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'avatar', 'type']
