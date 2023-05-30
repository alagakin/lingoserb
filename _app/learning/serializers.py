from rest_framework import serializers

from game.serializers import WordsGameSerializer
from learning.models import SavedWord
from words.serializers import WordTranslationSerializer, WordsWithTexts


class SaveWordCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SavedWord
        fields = '__all__'


class SavedWordsIds(serializers.Serializer):
    id = serializers.IntegerField(source='word.id')


class SavedWordListSerializer(serializers.ModelSerializer):
    word = WordTranslationSerializer(read_only=True)

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
