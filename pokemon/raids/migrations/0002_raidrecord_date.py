# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-24 19:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raids', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='raidrecord',
            name='date',
            field=models.DateField(default=datetime.date(2018, 4, 24)),
            preserve_default=False,
        ),
    ]
