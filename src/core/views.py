import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DeleteView, UpdateView, CreateView, ListView, DetailView, RedirectView

from core.forms import LectureForm, PracticalLessonForm
from core.models import Lecture, PracticalLesson
from core.utils import prepare_date_time_field
from user.constants import TEACHER, STUDENT


class HomeView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.type == STUDENT:
            return reverse_lazy('profile')
        return reverse_lazy('index')


class TestPage(TemplateView):
    template_name = 'test_page.html'


class LectureListView(LoginRequiredMixin, ListView):
    model = Lecture
    template_name = 'core/lecture/lecture_crud.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LectureListView, self).get_context_data(**kwargs)
        context.update({'form': LectureForm()})
        for query in self.get_queryset():
            context.update({f'form_{query.pk}': LectureForm(instance=query)})

        return context

    def get_queryset(self):
        if self.request.user.type == TEACHER:
            return self.model.objects.all()
        return self.model.objects.filter(published_at__lt=datetime.datetime.now())


class LectureDetailView(LoginRequiredMixin, DetailView):
    model = Lecture
    template_name = 'core/lecture/lecture_detail.html'


class LectureCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'core/lecture/lecture_crud.html'
    model = Lecture
    form_class = LectureForm
    context_object_name = 'lecture'
    success_url = reverse_lazy('lectures-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.POST.get('published_at'):
            post = self.request.POST.copy()
            post['published_at'] = prepare_date_time_field(post['published_at'])
            post._mutable = False
            kwargs.update({'data': post})
        return kwargs

    def test_func(self):
        return self.request.user.type == TEACHER

    def form_valid(self, form):
        lecture = form.save(commit=False)
        lecture.user = self.request.user
        return super().form_valid(form)


class LectureUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'core/lecture/lecture_crud.html'
    model = Lecture
    form_class = LectureForm
    context_object_name = 'lecture'
    success_url = reverse_lazy('lectures-list')

    def test_func(self):
        return self.request.user == self.get_object().user


class LectureDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Lecture
    success_url = reverse_lazy('lectures-list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def test_func(self):
        return self.request.user == self.get_object().user


class PracticalLessonListView(LoginRequiredMixin, ListView):
    model = PracticalLesson
    template_name = 'core/practical_lesson/practical_lesson_crud.html'
    context_object_name = 'practical_lesson_list'

    def get_queryset(self):
        return self.model.objects.filter(published_at__lt=datetime.datetime.now())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'form': PracticalLessonForm()})

        for query in self.get_queryset():
            context.update({f'form_{query.pk}': PracticalLessonForm(instance=query)})

        return context


class PracticalLessonCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'core/practical_lesson/practical_lesson_crud.html'
    model = PracticalLesson
    form_class = PracticalLessonForm
    context_object_name = 'practical_lesson'
    success_url = reverse_lazy('p-lessons-list')

    def form_invalid(self, form):
        print(form.errors)
        return super(PracticalLessonCreateView, self).form_invalid(form)

    def form_valid(self, form):
        practical_lesson = form.save(commit=False)
        practical_lesson.students = [str(i.id) for i in form.cleaned_data['students']]
        practical_lesson.user = self.request.user
        print('SUCCESS')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.POST.get('published_at'):
            post = self.request.POST.copy()
            post['published_at'] = prepare_date_time_field(post['published_at'])
            post._mutable = False
            kwargs.update({'data': post})
        return kwargs

    def test_func(self):
        return self.request.user.type == TEACHER


class PracticalLessonUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'core/practical_lesson/practical_lesson_crud.html'
    model = PracticalLesson
    form_class = PracticalLessonForm
    context_object_name = 'practical_lesson'
    success_url = reverse_lazy('p-lessons-list')

    def form_valid(self, form):
        practical_lesson = form.save(commit=False)
        practical_lesson.students = [str(i.id) for i in form.cleaned_data['students']]
        practical_lesson.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user == self.get_object().user


class PracticalLessonDetailView(LoginRequiredMixin, DetailView):
    model = PracticalLesson
    template_name = 'core/practical_lesson/practical_lesson_detail.html'


class PracticalLessonDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PracticalLesson
    success_url = reverse_lazy('p-lessons-list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def test_func(self):
        return self.request.user == self.get_object().user
