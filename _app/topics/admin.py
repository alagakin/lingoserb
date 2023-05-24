from django.contrib import admin

from topics.models import Topic


class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'words_count', 'title', 'picture', 'parent']
    readonly_fields = ['get_words']

    def get_words(self, obj):
        return ", ".join(obj.words.values_list('title', flat=True))

    get_words.short_description = 'Words'


admin.site.register(Topic, TopicAdmin)
