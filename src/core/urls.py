from django.urls import path, include
from .views import LectureList

urlpatterns = [
    path('lecture/', LectureList, name='lecture')
]
