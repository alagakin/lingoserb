from django.db import IntegrityError
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from words.models import SavedWord, Word, Category
from rest_framework.permissions import IsAuthenticated
from words.permissions import UserOwsSavedWord
from words.serializers import SavedWordListSerializer, SaveWordCreateSerializer, \
    WordsGameSerializer, TextsOfWithWordSerializer, \
    WordTranslationSerializer, SavedWordsIds, CategorySerializer, \
    CategoryWordsSerializer, CategoryTextsSerializer
from words.services.games import CardsGame


class SavedWordListAPIView(generics.ListAPIView):
    serializer_class = SavedWordListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = SavedWord.objects.filter(user_id=user_id)
        return queryset


class SavedWordCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = SavedWord.objects.all()
    serializer_class = SaveWordCreateSerializer

    def post(self, request, *args, **kwargs):
        if 'word' not in request.data:
            return Response('word is required',
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            saved_word = SavedWord(
                user=request.user,
                word_id=request.data['word']
            )
            saved_word.save()
            return Response(None,
                            status=status.HTTP_201_CREATED)
        except IntegrityError:
            saved_word = SavedWord.all_objects.get(user=request.user,
                                                   word_id=request.data['word'])
            saved_word.deleted = False
            saved_word.save(update_fields=['deleted'])
            return Response(None,
                            status=status.HTTP_201_CREATED)
        except Exception:
            return Response(None,
                            status=status.HTTP_400_BAD_REQUEST)


class DestroySavedWordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        # todo use serializers
        try:
            saved_word = SavedWord.objects.get(user_id=request.user.id,
                                               word_id=request.data.get('word'))
            saved_word.delete()
        except SavedWord.DoesNotExist:
            return Response('not found', status=status.HTTP_404_NOT_FOUND)

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GetGameAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        game = CardsGame(request.user.id)
        saved_words = game.get_saved_words()

        serialized = WordsGameSerializer(saved_words, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class SuccessRepetitionAPIView(APIView):
    permission_classes = (UserOwsSavedWord,)

    def patch(self, request, *args, **kwargs):
        saved_word = SavedWord.objects.get(id=kwargs['pk'])
        saved_word.repetition_count += 1
        saved_word.last_repetition = timezone.now()
        saved_word.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TextForWordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            word = Word.objects.get(pk=kwargs['pk'])
        except Word.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialized = TextsOfWithWordSerializer(word)
        if not serialized.data:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serialized.data, status=status.HTTP_200_OK)


class WordDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            word = Word.objects.get(pk=kwargs['pk'])
        except Word.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialized = WordTranslationSerializer(word)
        return Response(serialized.data, status=status.HTTP_200_OK)


class WordsListAPIView(generics.ListAPIView):
    serializer_class = WordTranslationSerializer
    queryset = Word.objects.all()
    permission_classes = (IsAuthenticated,)


class SavedWordsIDSAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        saved_words = SavedWord.objects.filter(user=request.user.id)
        serialized = SavedWordsIds(saved_words, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class CategoriesListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RetrieveCategoriesAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryWordsAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategoryWordsSerializer


class CategoryTextsAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategoryTextsSerializer
