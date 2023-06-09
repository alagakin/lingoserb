from django.urls import path, include, re_path

from accounts.views import ProfileView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('acconunts/profile/', ProfileView.as_view(),
         name='profile-update')
]
