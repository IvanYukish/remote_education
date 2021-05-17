from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from .models import Lecture

class LectureList(DetailView):
    model = Lecture
    template_name = 'educations/lectures/lecture.html'


