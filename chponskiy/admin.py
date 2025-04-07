from django.contrib import admin
from chponskiy.models import GlossaryItem, LeaderboardRecord
# Register your models here.

@admin.register(GlossaryItem)
class GlossaryItemAdmin(admin.ModelAdmin):
    search_fields = ('phrase_orig', 'phrase_translation')


@admin.register(LeaderboardRecord)
class LeaderboardRecordAdmin(admin.ModelAdmin):
    search_fields = ('username', 'score', 'difficulty')
