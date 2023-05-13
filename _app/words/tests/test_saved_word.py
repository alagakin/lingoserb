from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from words.models import Word, Category, SavedWord
from words.views import SavedWordListAPIView, SavedWordCreateAPIView, \
    DestroySavedWordAPIView
from rest_framework.test import APITestCase


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


class TestSavedWordsActions(APITestCase):
    def setUp(self) -> None:
        self.user_1 = get_user_model().objects.create(
            username='user 1',
            password='123'
        )
        self.token_user_1 = Token.objects.create(user=self.user_1)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token_user_1.key}')
        self.user_2 = get_user_model().objects.create(
            username='user 2',
            password='123'
        )
        self.token_user_2 = Token.objects.create(user=self.user_2)

        self.word_1 = Word.objects.create(
            title='Test word',
        )

        self.word_2 = Word.objects.create(
            title='Second word'
        )

    def test_user_can_add_saved_word(self):
        response = self.client.post(reverse('saved-word-create'), data={
            'word': self.word_1.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user_1.saved.count(), 1)

    def test_user_can_delete_saved_word(self):
        saved_word = SavedWord.objects.create(
            word=self.word_1,
            user=self.user_1
        )
        self.assertEqual(self.user_1.saved.count(), 1)
        response = self.client.delete(
            reverse('saved-word-destroy', kwargs={'pk': saved_word.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.user_1.saved.count(), 0)

    def test_user_can_get_saved_words(self):
        SavedWord.objects.create(
            word=self.word_1,
            user=self.user_1
        )
        response = self.client.get(
            reverse('saved-word-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Test word')

    def test_user_cant_access_another_users_saved_words(self):
        SavedWord.objects.create(
            word=self.word_2,
            user=self.user_2
        )
        response = self.client.get(
            reverse('saved-word-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotContains(response, 'Second word')

    def test_user_cant_delete_another_users_saved_words(self):
        saved_word = SavedWord.objects.create(
            word=self.word_2,
            user=self.user_2
        )
        self.assertEqual(self.user_2.saved.count(), 1)
        response = self.client.delete(
            reverse('saved-word-destroy', kwargs={'pk': saved_word.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.user_2.saved.count(), 1)
