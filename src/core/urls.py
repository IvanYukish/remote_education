from django.urls import path

from core.views import HomeView, LectureCreateView, LectureDeleteView, LectureListView, LectureUpdateView, \
    PracticalLessonCreateView, PracticalLessonUpdateView, PracticalLessonDeleteView, PracticalLessonListView, \
    LectureDetailView, TestCreateView, TestDetailView, TestListView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('lectures/', LectureListView.as_view(), name='lectures-list'),
    path('lectures/create', LectureCreateView.as_view(), name='lectures-create'),
    path('lectures/<int:pk>/', LectureDetailView.as_view(), name='lectures-detail'),
    path('lectures/<int:pk>/update', LectureUpdateView.as_view(), name='lectures-update'),
    path('lectures/<int:pk>/delete', LectureDeleteView.as_view(), name='lectures-delete'),

    path('p-lessons/', PracticalLessonListView.as_view(), name='p-lessons-list'),
    path('p-lessons/create', PracticalLessonCreateView.as_view(), name='p-lessons-create'),
    path('p-lessons/<int:pk>/update', PracticalLessonUpdateView.as_view(), name='p-lessons-update'),
    path('p-lessons/<int:pk>/delete', PracticalLessonDeleteView.as_view(), name='p-lessons-delete'),

    path('tests/', TestListView.as_view(), name='tests-list'),
    path('tests/create', TestCreateView.as_view(), name='tests-create'),
    path('tests/<int:pk>/', TestDetailView.as_view(), name='tests-detail'),

]
