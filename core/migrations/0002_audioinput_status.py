# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-09-27 09:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='audioinput',
            name='status',
            field=models.CharField(default='Active', max_length=40),
        ),
    ]
