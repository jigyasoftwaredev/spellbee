# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-22 10:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_showintroduction_into_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='school_name',
            new_name='region',
        ),
    ]
