from rest_framework import serializers
from learning.models import SavedWord
from words.serializers import WordTranslationSerializer


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
