from rest_framework import serializers
from topics.models import Topic
from words.serializers import WordTranslationSerializer, TextSerializer


class TopicsForWordSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class TopicMultilangRepresentation(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        ru = instance.translations.filter(lang='ru').first()
        en = instance.translations.filter(lang='en').first()
        if en:
            representation['title_en'] = en.title

        if ru:
            representation['title_ru'] = ru.title

        return representation


class SubtopicSerializer(TopicMultilangRepresentation):
    class Meta:
        model = Topic
        fields = ('id', 'title', 'description', 'picture', 'words_count')


class TopicSerializer(TopicMultilangRepresentation):
    subtopics = SubtopicSerializer(many=True)

    class Meta:
        model = Topic
        fields = ('id', 'title', 'description', 'picture', 'subtopics')


class TopicWordsSerializer(serializers.Serializer):
    words = WordTranslationSerializer(many=True)


class TopicTextsSerializer(serializers.Serializer):
    texts = TextSerializer(many=True)
