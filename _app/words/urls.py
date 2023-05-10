from django.urls import path

from words.views import SavedWordListAPIView

urlpatterns = [
    path('saved/<int:user_id>/', SavedWordListAPIView.as_view())
]
