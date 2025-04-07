import uuid
from uuid import UUID
from django.db import models

# Create your models here.
class GlossaryItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phrase_orig = models.TextField()
    phrase_translation = models.TextField()

    class Meta:
        db_table = 'glossary'


class LeaderboardRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.TextField()
    difficulty = models.TextField()
    score = models.IntegerField()

    class Meta:
        db_table = 'leaderboard'
