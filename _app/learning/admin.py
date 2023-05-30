from django.contrib import admin
from learning.models import SavedWord
from learning.models import Lesson


class SavedWordAdmin(admin.ModelAdmin):
    list_display = ["word", "user", "last_repetition", "repetition_count"]


class LessonAdmin(admin.ModelAdmin):
    list_display = ["user", "topic", "created_at", "finished_at"]
    readonly_fields = ["created_at"]


admin.site.register(Lesson, LessonAdmin)
admin.site.register(SavedWord, SavedWordAdmin)
