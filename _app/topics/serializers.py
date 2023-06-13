from rest_framework import serializers
from django.core.cache import cache

from accounts.models import CustomUser
from learning.models import SavedWord
from topics.models import Topic, TopicTranslation
from topics.utils import topic_progress_cache_key
from words.serializers import WordTranslationSerializer, TextSerializer


# todo: consider skipped words
def learned_percent(topic: Topic, user: CustomUser):
    cache_key = topic_progress_cache_key(topic.id, user.id)
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result

    words_of_topic = topic.words.all()
    if words_of_topic.count() == 0:
        return 0

    saved_from_topic = SavedWord.objects.filter(user=user,
                                                word__in=words_of_topic,
                                                repetition_count__gt=0)
    total_score = 0
    for saved in saved_from_topic:
        total_score += saved.repetition_count

    percent = round(total_score / (5 * words_of_topic.count()) * 100)

    cache.set(cache_key, percent, timeout=3600)

    return percent


class SubtopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'title', 'description', 'picture', 'words_count')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['learned_percent'] = learned_percent(instance,
                                                            self.context[
                                                                'request'].user)
        request = self.context['request']

        if request.LANGUAGE_CODE:
            translation = instance.translations.filter(
                lang=request.LANGUAGE_CODE).all()
            serialized_translations = TopicTranslationSerializer(translation,
                                                                 many=True)
            representation['translation'] = serialized_translations.data

        return representation


class TopicSerializer(serializers.ModelSerializer):
    subtopics = SubtopicSerializer(many=True)

    class Meta:
        model = Topic
        fields = ('id', 'title', 'description', 'picture', 'subtopics')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.context['request']
        return context

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context['request']
        if request.LANGUAGE_CODE:
            translation = instance.translations.filter(
                lang=request.LANGUAGE_CODE).all()
            serialized_translations = TopicTranslationSerializer(translation,
                                                                 many=True)
            representation['translation'] = serialized_translations.data
        return representation


class TopicTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicTranslation
        fields = '__all__'


class TopicWordsSerializer(serializers.Serializer):
    words = WordTranslationSerializer(many=True)


class TopicTextsSerializer(serializers.Serializer):
    texts = TextSerializer(many=True)
