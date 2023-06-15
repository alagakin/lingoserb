from django.urls import path, include, re_path

from accounts.views import ProfileView, GoogleLogin
from learn_serbian.views import get_csrf_token

urlpatterns = [
    path('acconunts/profile/', ProfileView.as_view(),
         name='profile-update'),
    path('csrf/', get_csrf_token, name='csrf'),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('allauth/', include('allauth.urls')),
]
