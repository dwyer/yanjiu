# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-31 17:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cedict', '0003_text_video_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='text',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Text',
        ),
    ]
