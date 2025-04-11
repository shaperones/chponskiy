"""Configures models used in the app - glossary items and leaderboard records"""

from secrets import randbelow
from django.contrib.auth.models import User     # pylint: disable=E5142
from django.db import models
from django.db.models import Max

class GlossaryItem(models.Model):
    """Glossary item model - provides fields for phrase
    translations in different languages and difficulty level."""

    id = models.AutoField(primary_key=True)
    level = models.IntegerField()
    phrase_english = models.TextField()
    phrase_japanese = models.TextField()
    phrase_kana = models.TextField()
    phrase_chinese = models.TextField()
    phrase_pinyin = models.TextField()

    @classmethod
    def get_random(cls) -> 'GlossaryItem':
        """Returns a random glossary item."""
        max_id = cls.objects.all().aggregate(max_id=Max("id"))['max_id']
        max_tries = 32
        while max_tries:
            pk = randbelow(max_id) + 1
            glossary_item = GlossaryItem.objects.get(pk=pk)
            if glossary_item:
                return glossary_item
            max_tries -= 1
        raise ValueError("Failed to find existing object")

    @classmethod
    def get_randoms(cls, num: int) -> list['GlossaryItem']:
        """Returns specified number of distinct glossary items."""
        max_id = cls.objects.all().aggregate(max_id=Max("id"))['max_id']
        glossary_items: list[GlossaryItem] = []
        ids: set[int] = set()
        for _ in range(num):
            max_tries = 32
            while max_tries:
                pk = randbelow(max_id) + 1
                if pk not in ids:
                    glossary_item = GlossaryItem.objects.get(pk=pk)
                    if glossary_item:
                        glossary_items.append(glossary_item)
                        break
                max_tries -= 1
            else:
                raise ValueError("Failed to collect enough distinct items")
        return glossary_items

    class Meta:
        db_table = 'glossary'


class LeaderboardRecord(models.Model):
    """Leaderboard record model - provides fields for the record holder username,
    difficulty played and the actual score.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty = models.TextField()
    score = models.IntegerField()

    @classmethod
    def get_top10(cls) -> dict[str, list['LeaderboardRecord']]:
        """Returns 10 highest records in every category."""
        return {
            'easy':
                list(LeaderboardRecord.objects.filter(difficulty='easy')
                     .order_by('-score')[:10]),
            'medium':
                list(LeaderboardRecord.objects.filter(difficulty='medium')
                     .order_by('-score')[:10]),
            'nightmare':
                list(LeaderboardRecord.objects.filter(difficulty='nightmare')
                     .order_by('-score')[:10]),
        }

    @classmethod
    def get_users_recent(cls, user: User) -> list['LeaderboardRecord']:
        """Returns 10 most recent user played games"""
        return list(LeaderboardRecord.objects.filter(user=user).order_by('-id')[:10])

    class Meta:
        db_table = 'leaderboard'
