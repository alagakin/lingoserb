from django.test import TestCase
from django.urls import resolve, reverse

from words.views import SavedWordListAPIView, SavedWordCreateAPIView, \
    DestroySavedWordAPIView


class TestEndpointsResoled(TestCase):
    def test_get_saved_words_list_resolved(self):
        url = reverse('saved-word-list')
        self.assertEqual(resolve(url).func.view_class, SavedWordListAPIView)

    def test_saved_word_create_resolved(self):
        url = reverse('saved-word-create')
        self.assertEqual(resolve(url).func.view_class, SavedWordCreateAPIView)

    def test_saved_word_destroy_resolved(self):
        url = reverse('saved-word-destroy', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, DestroySavedWordAPIView)
