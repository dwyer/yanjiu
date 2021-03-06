# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-29 19:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [(b'cedict', '0001_initial'), (b'cedict', '0002_translationstar'), (b'cedict', '0003_phrasestar'), (b'cedict', '0004_profile'), (b'cedict', '0005_auto_20160129_1909')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Phrase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('traditional', models.CharField(max_length=255)),
                ('simplified', models.CharField(max_length=255)),
                ('pinyin', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translation', models.TextField()),
                ('phrase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cedict.Phrase')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starred_phrases', models.ManyToManyField(to=b'cedict.Phrase')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
