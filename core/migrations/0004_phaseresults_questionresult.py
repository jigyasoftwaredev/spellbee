# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-09-30 12:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_profile_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhaseResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_answers', models.CharField(max_length=10)),
                ('wrong_answers', models.CharField(max_length=10)),
                ('is_qualified_for_phase2', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Student')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phase_type', models.CharField(max_length=20)),
                ('student_input', models.CharField(max_length=20)),
                ('is_correct', models.BooleanField(default=False)),
                ('contest_type', models.CharField(max_length=10)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Student')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.AudioInput')),
            ],
        ),
    ]
