# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-12 16:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainers', '0002_trainer_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainerbadge',
            name='note',
        ),
    ]