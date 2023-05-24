from django.contrib import admin
from topics.models import Topic


class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'words_count', 'title', 'picture', 'get_translations',
                    'parent']
    readonly_fields = ['get_words', 'get_translations']

    def get_translations(self, obj):
        return ", ".join(obj.translations.values_list('title', flat=True))

    def get_words(self, obj):
        return ", ".join(obj.words.values_list('title', flat=True))

    get_words.short_description = 'Words'


admin.site.register(Topic, TopicAdmin)
