from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class GlossaryItem(models.Model):
    id = models.AutoField(primary_key=True)
    level = models.IntegerField()
    phrase_english = models.TextField()
    phrase_japanese = models.TextField()
    phrase_kana = models.TextField()
    phrase_chinese = models.TextField()
    phrase_pinyin = models.TextField()

    class Meta:
        db_table = 'glossary'


class LeaderboardRecord(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty = models.TextField()
    score = models.IntegerField()

    class Meta:
        db_table = 'leaderboard'
