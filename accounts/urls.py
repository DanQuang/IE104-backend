from django.urls import path, include
from .views import UserProfileView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('profile/', UserProfileView.as_view(), name='user-profile'),  # Add the path for UserProfileView
]
