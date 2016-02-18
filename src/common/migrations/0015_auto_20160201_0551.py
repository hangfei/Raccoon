# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-01 05:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0014_auto_20160119_0741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='state',
            field=models.CharField(choices=[('PC', 'Project is created'), ('PS', 'Project is submitted'), ('EA', 'An expert is assigned'), ('ET', 'An expert took this project'), ('CA', 'The client accepted this expert'), ('IP', 'An expert is working on it'), ('PF', 'Project is finished'), ('CC', 'The client has confirmed the project finish'), ('AD', 'The client has appealed the dispute to the administrator'), ('PR', 'Payment is received and the project is closed')], default='PC', max_length=2),
        ),
    ]
