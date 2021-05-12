from django.urls import path, include

from .views import ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path('', include('allauth.urls')),
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('profile/update', ProfileUpdateView.as_view(), name='profile-update'),

]
