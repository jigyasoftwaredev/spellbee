# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-16 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20191016_0628'),
    ]

    operations = [
        migrations.AddField(
            model_name='showintroduction',
            name='into_id',
            field=models.CharField(default='1', max_length=10),
        ),
    ]
