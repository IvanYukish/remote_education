from django.urls import path, include
from .views import LectureCreate

urlpatterns = [
    path('lecture/', LectureCreate.as_view(), name='lecture')
]
