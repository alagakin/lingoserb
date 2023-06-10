from learning.models import SavedWord
from words.serializers import WordTranslationSerializer, WordsWithTexts
import random
from rest_framework import serializers
from words.models import Translation


class SaveWordCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SavedWord
        fields = '__all__'


class SavedWordsIds(serializers.Serializer):
    id = serializers.IntegerField(source='word.id')


class SavedWordListSerializer(serializers.ModelSerializer):
    word = WordTranslationSerializer(read_only=True)
    learned_percent = serializers.IntegerField(read_only=True)

    class Meta:
        model = SavedWord
        fields = '__all__'


class ProgressSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    cnt = serializers.SerializerMethodField()

    def get_id(self, instance):
        return instance.word.id

    def get_cnt(self, instance):
        return instance.repetition_count


class LessonSerializer(serializers.Serializer):
    topic_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        for_watching = [word.word for word in instance.saved_words.all() if
                        word.watched_count == 0]

        leaning_serialized = WordsWithTexts(for_watching, many=True)
        representation['learning'] = leaning_serialized.data

        game_serialized = WordsGameSerializer(
            instance.saved_words.all(), many=True
        )

        representation['game'] = game_serialized.data

        return representation


class WordGameOptionsSerializer(serializers.Serializer):
    # todo track language
    title = serializers.CharField()
    # todo how the fuck does it work?
    correct = serializers.BooleanField(default=True)


class WordsGameSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    word = serializers.CharField(source='word.title')
    word_id = serializers.IntegerField(source='word.id')
    last_repetition = serializers.DateTimeField()
    repetition_count = serializers.IntegerField()
    audio_link = serializers.CharField(source='word.audio_link')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        topic = instance.word.topics.first()
        # todo lang
        incorrect_translations = Translation.objects.filter(lang='ru',
                                                            word__topics__exact=topic).exclude(
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


class GraphSerializer(serializers.Serializer):
    date = serializers.DateField()
    lessons_cnt = serializers.IntegerField()
    words_cnt = serializers.IntegerField()
