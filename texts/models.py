from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User
from django.db import models

from .utils import get_terms


class GetOrInstatiateMixin(models.Model):

    class Meta:
        abstract = True

    @classmethod
    def get_or_instantiate(cls, defaults=None, **kwargs):
        try:
            obj = cls.objects.get(**kwargs)
            created = False
        except cls.DoesNotExist:
            if defaults is not None:
                kwargs.update(defaults)
            obj = cls(**kwargs)
            created = True
        return (obj, created)


class Text(models.Model):

    title = models.CharField(max_length=255, blank=False)
    text = models.TextField(blank=True)
    audio_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)
    owner = models.ForeignKey(User, null=False)
    words = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.words = '\n'.join(get_terms(self.text))
        return super(Text, self).save(*args, **kwargs)

    def phrases(self, user):
        phrases = []
        for word in self.words.splitlines():
            phrases.append(
                Phrase.get_or_instantiate(phrase=word, owner=user)[0])
        return phrases


class Phrase(GetOrInstatiateMixin, models.Model):

    REVIEW_TIMES_BY_LEVEL = {
        1: datetime.timedelta(days=0),
        2: datetime.timedelta(days=1),
        3: datetime.timedelta(days=3),
        4: datetime.timedelta(days=7),
        5: datetime.timedelta(days=30),
    }

    phrase = models.CharField(max_length=255, blank=False)
    translation = models.CharField(max_length=255, blank=True)
    romanization = models.CharField(max_length=255, blank=True)
    level = models.IntegerField(null=False, default=0)
    due_date = models.DateTimeField(null=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, null=False)

    class Meta:
        unique_together = ('phrase', 'owner')

    def __init__(self, *args, **kwargs):
        super(Phrase, self).__init__(*args, **kwargs)
        self._old_level = self.level

    def save(self, *args, **kwargs):
        delta = self.REVIEW_TIMES_BY_LEVEL.get(self.level)
        if delta is not None:
            self.due_date = datetime.datetime.now() + delta
        else:
            self.due_date = None
        super(Phrase, self).save(*args, **kwargs)
