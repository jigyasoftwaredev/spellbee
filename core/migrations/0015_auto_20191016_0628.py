# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-16 06:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_showintroduction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='showintroduction',
            old_name='show',
            new_name='round_finished',
        ),
    ]
