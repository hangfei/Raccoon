# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-28 07:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentForClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('rating', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='comments_num',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='client',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='avatar/', verbose_name='Avatar'),
        ),
        migrations.AddField(
            model_name='commentforclient',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Client'),
        ),
        migrations.AddField(
            model_name='commentforclient',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Project'),
        ),
    ]