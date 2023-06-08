from django.urls import path, include, re_path

from accounts.views import ProfileUpdateView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('acconunts/profile/', ProfileUpdateView.as_view(),
         name='profile-update')
]
