from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('words.urls')),
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('topics.urls')),
    path('api/v1/', include('learning.urls')),
    path('api/v1/', include('achievements.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
