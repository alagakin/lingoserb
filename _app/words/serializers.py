from rest_framework import serializers
from words.models import Word, TextTranslation


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'


class TextSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    content = serializers.CharField()
    audio_link = serializers.CharField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # todo lang
        try:
            translation = TextTranslation.objects.get(text=instance,
                                                      lang='ru').content
        except TextTranslation.DoesNotExist:
            translation = None

        representation['translation'] = translation
        return representation


class TextsOfWithWordSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    texts = TextSerializer(many=True, read_only=True)

    class Meta:
        model = Word
        fields = ['title', 'texts']


class TranslationsForWordSerializer(serializers.Serializer):
    title = serializers.CharField()
    lang = serializers.CharField()


class WordTranslationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    topics = serializers.CharField()
    texts_count = serializers.IntegerField(source='texts.count')
    audio_link = serializers.CharField()

    def to_representation(self, instance):
        from topics.serializers import SubtopicSerializer
        request = self.context.get('request')

        representation = super().to_representation(instance)
        topics = instance.topics.all()
        serialized_topics = SubtopicSerializer(topics,
                                               many=True,
                                               context={'request': request})

        representation['topics'] = serialized_topics.data

        if request.LANGUAGE_CODE == 'ru':
            representation['translation'] = TranslationsForWordSerializer(
                instance.translations.filter(lang='ru'), many=True).data
        else:
            representation['translation'] = TranslationsForWordSerializer(
                instance.translations.filter(lang='en'), many=True).data

        return representation


class WordsWithTexts(WordTranslationSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        serialized_texts = TextSerializer(instance.texts, many=True)
        representation['texts'] = serialized_texts.data
        return representation
