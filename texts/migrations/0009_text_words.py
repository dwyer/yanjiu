# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-23 10:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0008_phrase_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='words',
            field=models.TextField(blank=True),
        ),
    ]