# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-19 08:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expert',
            name='comments_num',
            field=models.PositiveIntegerField(default=0),
        ),
    ]