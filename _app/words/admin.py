from django.contrib import admin
from words.models import Word, Translation


class TranslationInlineAdmin(admin.TabularInline):
    model = Translation
    extra = 3


class WordAdmin(admin.ModelAdmin):
    list_display = ['title', 'part']
    inlines = [TranslationInlineAdmin]


class TranslationAdmin(admin.ModelAdmin):
    list_display = ['title', 'lang', 'word']


admin.site.register(Word, WordAdmin)
admin.site.register(Translation, TranslationAdmin)
