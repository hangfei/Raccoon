# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-04 06:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=120, verbose_name='subject')),
                ('body', models.TextField(blank=True, verbose_name='body')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='visitor')),
                ('sent_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='sent at')),
                ('read_at', models.DateTimeField(blank=True, null=True, verbose_name='read at')),
                ('replied_at', models.DateTimeField(blank=True, null=True, verbose_name='replied at')),
                ('sender_archived', models.BooleanField(default=False, verbose_name='archived by sender')),
                ('recipient_archived', models.BooleanField(default=False, verbose_name='archived by recipient')),
                ('sender_deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted by sender at')),
                ('recipient_deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted by recipient at')),
                ('moderation_status', models.CharField(choices=[('p', 'Pending'), ('a', 'Accepted'), ('r', 'Rejected')], default='p', max_length=1, verbose_name='status')),
                ('moderation_date', models.DateTimeField(blank=True, null=True, verbose_name='moderated at')),
                ('moderation_reason', models.CharField(blank=True, max_length=120, verbose_name='rejection reason')),
                ('moderation_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='moderated_messages', to=settings.AUTH_USER_MODEL, verbose_name='moderator')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_messages', to='postman.Message', verbose_name='parent message')),
                ('recipient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL, verbose_name='recipient')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL, verbose_name='sender')),
                ('thread', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_messages', to='postman.Message', verbose_name='root message')),
            ],
            options={
                'verbose_name': 'message',
                'ordering': ['-sent_at', '-id'],
                'verbose_name_plural': 'messages',
            },
        ),
        migrations.CreateModel(
            name='PendingMessage',
            fields=[
            ],
            options={
                'verbose_name': 'pending message',
                'proxy': True,
                'verbose_name_plural': 'pending messages',
            },
            bases=('postman.message',),
        ),
    ]
