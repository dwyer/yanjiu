from __future__ import unicode_literals

import logging as logger

from django.contrib.auth.models import User
from django.db import models
from django.utils.html import strip_tags

from .utils import process_text


class Text(models.Model):
    title = models.CharField(max_length=255, blank=False)
    text = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    owner = models.ForeignKey(User, null=False)

    @property
    def processed_text(self):
        import time
        t = time.time()
        s = process_text(self.text)
        print 'finished processed_text in %gs' % (time.time() - t)
        return s

    def save(self, *args, **kwargs):
        self.text = strip_tags(self.text)
        return super(Text, self).save(*args, **kwargs)
