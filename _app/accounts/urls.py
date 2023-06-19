from django.urls import path, include, re_path

from accounts.views import ProfileView, GoogleLogin
from learn_serbian.views import get_csrf_token

urlpatterns = [
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('acconunts/profile/', ProfileView.as_view(),
         name='profile-update'),
    path('csrf/', get_csrf_token, name='csrf'),
]
