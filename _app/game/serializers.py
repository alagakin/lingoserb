import random
from rest_framework import serializers
from words.models import Translation


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
    audio_link = serializers.CharField(source='word.audio_link')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # todo lang
        # todo random is too bad, need to get words from the same Topic
        incorrect_translations = Translation.objects.filter(lang='ru').exclude(
            word__id=instance.word.id).order_by('?')[:3]

        for obj in incorrect_translations:
            obj.correct = False

        correct_translation = Translation.objects.filter(lang='ru').filter(
            word__id=instance.word.id).first()
        correct_translation.correct = True

        options = list(incorrect_translations)
        options.append(correct_translation)
        random.shuffle(options)
        options = WordGameOptionsSerializer(options, many=True)

        representation['options'] = options.data

        return representation
