# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class AudioInput(models.Model):
	SPELL_BEE_CHOICES = (
		('JSB','JSB'),
		('SSB','SSB')
		)
	PHASE_CHOICES = (
		('Phase 1','Phase 1'),
		('Phase 2','Phase 2')
		)
	DIFFICULTY_CHOICES = (
		('Easy','Easy'),
		('Medium','Medium'),
		('Difficult','Difficult')
		)
	word = models.CharField(max_length=30)
	file_name = models.CharField(max_length=30)
	pronunciation = models.CharField(max_length=30)
	pos = models.CharField(max_length=30)
	land_of_origin = models.CharField(max_length=30)
	additional_info = models.CharField(max_length=30)
	added_by = models.CharField(max_length=30)
	created_by = models.CharField(max_length=30)
	spellbee_type = models.CharField(max_length=30,choices=SPELL_BEE_CHOICES)
	phase = models.CharField(max_length=30,choices=PHASE_CHOICES)
	year = models.CharField(max_length=30)
	status = models.CharField(max_length=40,default='Active')
	difficulty_level = models.CharField(max_length=30,choices=DIFFICULTY_CHOICES,default='Easy')

class Student(models.Model):
	SPELL_BEE_CHOICES = (
		('JSB','JSB'),
		('SSB','SSB')
		)
	PHASE_CHOICES = (
		('Phase 1','Phase 1'),
		('Phase 2','Phase 2')
		)
	GENDER_CHOICES = (
		('1','1'),
		('2','2'),
		('3','3'),
		)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	father_name = models.CharField(max_length=30)
	gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
	dob = models.DateField()
	class_name = models.CharField(max_length=30)
	spellbee_type = models.CharField(max_length=30,choices=PHASE_CHOICES)
	phase= models.CharField(max_length=30)
	school_name = models.CharField(max_length=50)

class Profile(models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=128)
	email = models.CharField(max_length=120)


class PhaseResults(models.Model):
	student = models.ForeignKey(Student,on_delete=models.CASCADE)
	correct_answers = models.CharField(max_length=10)
	wrong_answers = models.CharField(max_length=10,null=True,blank=True)
	is_qualified_for_phase2 = models.BooleanField(default=False)

class PhaseQuestions(models.Model):
	word = models.ForeignKey(AudioInput,on_delete=models.CASCADE)
	phase_type = models.CharField(max_length=20)
	student = models.ForeignKey(Student,on_delete=models.CASCADE,null=True,blank=True)
	student_input = models.CharField(max_length=20,null=True,blank=True)
	is_correct = models.BooleanField(default=False)
	is_answered = models.BooleanField(default=False)

class Phase2Result(models.Model):
	student = models.ForeignKey(Student,on_delete=models.CASCADE)
	correct_answers = models.CharField(max_length=10)
	wrong_answers = models.CharField(max_length=10)