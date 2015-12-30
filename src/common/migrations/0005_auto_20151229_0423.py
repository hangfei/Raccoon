# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-29 04:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_auto_20151229_0401'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='first_name_text',
        ),
        migrations.RemoveField(
            model_name='client',
            name='last_name_text',
        ),
        migrations.RemoveField(
            model_name='client',
            name='password',
        ),
        migrations.AddField(
            model_name='account',
            name='first_name',
            field=models.CharField(default='Hangfei', max_length=30, verbose_name='First Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='last_name',
            field=models.CharField(default='Lin', max_length=30, verbose_name='Last Name'),
            preserve_default=False,
        ),
    ]