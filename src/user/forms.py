from allauth.account.forms import SignupForm
from django import forms
from django.utils.translation import ugettext_lazy as _

from .constants import USER_TYPE_CHOICES
from .models import CustomUser


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(label=_('Ім\'я'), max_length=150,
                                 widget=forms.TextInput(attrs={'placeholder': _('Введіть своє ім\'я')}))
    last_name = forms.CharField(label=_('Прізвище'), max_length=150,
                                widget=forms.TextInput(attrs={'placeholder': _('Введіть своє прізвище')}))
    type = forms.ChoiceField(label=_('Тип'), choices=USER_TYPE_CHOICES)

    def save(self, request):
        user = super().save(request)
        user.type = self.cleaned_data['type']
        user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'avatar']
