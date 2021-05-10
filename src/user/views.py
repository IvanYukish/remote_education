from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from user.forms import ProfileUpdateForm
from user.models import CustomUser


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'user/profile_detail.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'user/profile_update.html'
    context_object_name = 'user'
    form_class = ProfileUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile')
