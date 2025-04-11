from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max
from secrets import randbelow

# Create your models here.
class GlossaryItem(models.Model):
    id = models.AutoField(primary_key=True)
    level = models.IntegerField()
    phrase_english = models.TextField()
    phrase_japanese = models.TextField()
    phrase_kana = models.TextField()
    phrase_chinese = models.TextField()
    phrase_pinyin = models.TextField()

    @classmethod
    def get_random(cls) -> 'GlossaryItem':
        max_id = cls.objects.all().aggregate(max_id=Max("id"))['max_id']
        max_tries = 32
        while max_tries:
            pk = randbelow(max_id) + 1
            glossary_item = GlossaryItem.objects.get(pk=pk)
            if glossary_item:
                return glossary_item
            max_tries -= 1
        raise ValueError("Failed to find existing object")

    class Meta:
        db_table = 'glossary'


class LeaderboardRecord(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty = models.TextField()
    score = models.IntegerField()

    class Meta:
        db_table = 'leaderboard'
