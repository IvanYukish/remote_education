from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView

from .models import Lecture
from .forms import CreateLecture

class LectureCreate(LoginRequiredMixin, CreateView):
    template_name = 'educations/lectures/lecture.html'
    form_class = CreateLecture

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super().form_valid(form)
        except:
            return redirect('lecture')


