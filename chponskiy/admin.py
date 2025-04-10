from django.contrib import admin
from django.http import HttpRequest
from django.urls import path
from django.shortcuts import redirect, render
from django import forms
from pydantic import BaseModel
from chponskiy.models import GlossaryItem, LeaderboardRecord
import csv
from io import StringIO

class GlossaryItemCSVRecord(BaseModel):
    level: int
    phrase_english: str
    phrase_japanese: str
    phrase_kana: str
    phrase_chinese: str
    phrase_pinyin: str


@admin.register(GlossaryItem)
class GlossaryItemAdmin(admin.ModelAdmin):
    search_fields = ('phrase_english', 'phrase_japanese', 'phrase_kana', 'phrase_chinese', 'phrase_pinyin')
    list_display = ('level', 'phrase_english', 'phrase_japanese', 'phrase_kana', 'phrase_chinese', 'phrase_pinyin')

    change_list_template = "admin_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request: HttpRequest):
        if request.method == "POST":
            csv_content = request.FILES["csv_file"].read().decode("utf-8")
            reader = csv.DictReader(StringIO(csv_content), delimiter=';', lineterminator='\n', skipinitialspace=True, strict=True)
            records = [GlossaryItemCSVRecord.model_validate(row) for row in reader]

            for record in records:
                glossary_item = GlossaryItem(
                    level=record.level,
                    phrase_english=record.phrase_english,
                    phrase_japanese=record.phrase_japanese,
                    phrase_kana=record.phrase_kana,
                    phrase_chinese=record.phrase_chinese,
                    phrase_pinyin=record.phrase_pinyin,
                )
                glossary_item.save()

            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin_csv_form.html", payload
        )

@admin.register(LeaderboardRecord)
class LeaderboardRecordAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'score', 'difficulty')

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()
