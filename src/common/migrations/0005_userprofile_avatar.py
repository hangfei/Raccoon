# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-28 00:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_auto_20160222_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='test3339', verbose_name='Avatar'),
        ),
    ]
