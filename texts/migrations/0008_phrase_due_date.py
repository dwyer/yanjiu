# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-23 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0007_phrase_translation'),
    ]

    operations = [
        migrations.AddField(
            model_name='phrase',
            name='due_date',
            field=models.DateTimeField(null=True),
        ),
    ]