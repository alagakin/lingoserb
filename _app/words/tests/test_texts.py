from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from words.models import Word, Text
from words.views.views import WordsListAPIView, WordDetailAPIView, TextForWordAPIView
from rest_framework.test import APITestCase


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


class TestWordsAPIViews(APITestCase):
    def setUp(self) -> None:
        self.user_1 = get_user_model().objects.create(
            username='user 1',
            password='123'
        )
        self.token_user_1 = Token.objects.create(user=self.user_1)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token_user_1.key}')

        self.word_1 = Word.objects.create(
            title='Test word',
        )

        self.text_word_1 = Text.objects.create(
            content='Text for Test word'
        )
        self.word_1.texts.add(self.text_word_1)

    def test_user_can_get_words_list(self):
        response = self.client.get(reverse('word-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Test word')

    def test_user_can_get_word_detail_info(self):
        response = self.client.get(
            reverse('word-detail', kwargs={'pk': self.word_1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Test word')

    def test_user_can_get_texts_for_word(self):
        response = self.client.get(
            reverse('text-for-word', kwargs={'pk': self.word_1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Test word')
        self.assertContains(response, 'Text for Test word')
