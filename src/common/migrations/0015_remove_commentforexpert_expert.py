# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-16 07:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0014_auto_20160216_0720'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentforexpert',
            name='expert',
        ),
    ]
