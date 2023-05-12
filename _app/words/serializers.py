import random
from rest_framework import serializers
from words.models import SavedWord, Word, Translation, Text, TextTranslation


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'


class SavedWordListSerializer(serializers.ModelSerializer):
    word = WordSerializer(read_only=True)

    class Meta:
        model = SavedWord
        fields = '__all__'


class SaveWordCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SavedWord
        fields = '__all__'


class WordGameOptionsSerializer(serializers.Serializer):
    # todo track language
    title = serializers.CharField()
    # todo how the fuck does it work?
    correct = serializers.BooleanField(default=True)


class WordsGameSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    word = serializers.CharField(source='word.title')
    last_repetition = serializers.DateTimeField()
    repetition_count = serializers.IntegerField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # todo lang
        # todo random is too bad, need to get words from the same category
        incorrect_translations = Translation.objects.filter(lang='ru').exclude(
            word__id=instance.word.id).order_by('?')[:3]

        for obj in incorrect_translations:
            obj.correct = False

        correct_translation = Translation.objects.filter(lang='ru').filter(
            word__id=instance.word.id)
        correct_translation.correct = True

        options = list(incorrect_translations) + list(correct_translation)
        random.shuffle(options)
        options = WordGameOptionsSerializer(options, many=True)

        representation['options'] = options.data

        return representation


class TextSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    content = serializers.CharField()

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
