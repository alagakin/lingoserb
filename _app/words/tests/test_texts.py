from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from words.models import Word, Category, SavedWord, Translation
from words.views import SavedWordListAPIView, SavedWordCreateAPIView, \
    DestroySavedWordAPIView, SuccessRepetitionAPIView, GetGameAPIView, \
    WordsListAPIView, WordDetailAPIView, TextForWordAPIView
from rest_framework.test import APITestCase
import json


class TestEndpointsResoled(TestCase):
    def test_word_list_resolved(self):
        url = reverse('word-list')
        self.assertEqual(resolve(url).func.view_class, WordsListAPIView)

    def test_word_detail_resolved(self):
        url = reverse('word-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, WordDetailAPIView)

    def test_text_for_word_resolved(self):
        url = reverse('text-for-word', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, TextForWordAPIView)


class TestGameActions(APITestCase):
    pass
