# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-01 13:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20191001_1257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionresult',
            name='question',
        ),
        migrations.RemoveField(
            model_name='questionresult',
            name='student',
        ),
        migrations.AddField(
            model_name='phasequestions',
            name='is_answered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='phasequestions',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='phasequestions',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Student'),
        ),
        migrations.AddField(
            model_name='phasequestions',
            name='student_input',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.DeleteModel(
            name='QuestionResult',
        ),
    ]