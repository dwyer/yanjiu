# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-23 10:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0009_text_words'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='text',
            name='terms',
        ),
    ]