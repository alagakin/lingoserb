from rest_framework import serializers
from words.models import SavedWord, Word


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
