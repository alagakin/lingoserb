from rest_framework import serializers
from topics.models import Topic
from words.serializers import WordTranslationSerializer, TextSerializer


class TopicsForWordSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'title', 'description', 'picture', 'words_count')


class TopicWordsSerializer(serializers.Serializer):
    words = WordTranslationSerializer(many=True)


class TopicTextsSerializer(serializers.Serializer):
    texts = TextSerializer(many=True)
