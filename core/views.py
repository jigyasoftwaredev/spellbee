# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import AudioInput,Student,PhaseQuestions,Phase2Result,PhaseResults

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from dateutil.parser import parse

from django.http import HttpResponse
import json
# Create your views here.
def save_audio(request):
	if request.method == 'POST':
		# import pdb;pdb.set_trace()
		myfile = ''
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		input_name = AudioInput()
		input_name.word = request.POST['word']
		input_name.file_name = filename
		input_name.pronunciation = request.POST['pronunciation']
		input_name.pos = request.POST['pos']
		input_name.land_of_origin = request.POST['land_of_origin']
		input_name.additional_info = request.POST['additional_info']
		input_name.added_by = request.POST['added_by']
		input_name.created_by = request.POST['created_by']
		input_name.spellbee_type = request.POST['spellbee_type']
		input_name.phase = request.POST['phase']
		input_name.year = request.POST['year']
		input_name.difficulty_level = request.POST['difficulty']
		input_name.save()
		# book = xlrd.open_workbook('media/' + filename)
		# return HttpResponse(json.dumps({
	 #                        'type': 'success',
	 #                        'message': 'Audio Saved Successfully'
	 #                    }))
		jsb_words = AudioInput.objects.filter(spellbee_type='JSB (Junior Spell Bee)')
		ssb_words = AudioInput.objects.filter(spellbee_type='SSB (Senior Spell Bee)')
		return render(request,'words.html',{'jsb_words':jsb_words,'ssb_words':ssb_words})
	jsb_words = AudioInput.objects.filter(spellbee_type='JSB (Junior Spell Bee)')
	ssb_words = AudioInput.objects.filter(spellbee_type='SSB (Senior Spell Bee)')
	return render(request,'words.html',{'jsb_words':jsb_words,'ssb_words':ssb_words})


def contests(request):
	return render(request,'contest-select.html')

def students(request):
	if request.method == 'POST':
		import pdb;pdb.set_trace()
		input_name = Student()
		input_name.first_name = request.POST['first_name']
		input_name.last_name = request.POST['last_name']
		input_name.father_name = request.POST['father_name']
		input_name.gender = request.POST['optionsRadios']
		input_name.dob = parse(request.POST['dob'])
		input_name.class_name = request.POST['class_name']
		input_name.spellbee_type = request.POST['spellbee_type']
		input_name.phase = request.POST['phase']
		input_name.school_name = request.POST['school_name']
		input_name.save()
		jsb_students = Student.objects.filter(spellbee_type='JSB (Junior Spell Bee)')
		ssb_students = Student.objects.filter(spellbee_type='SSB (Senior Spell Bee)')
		# book = xlrd.open_workbook('media/' + filename)
		return render(request,'SpellBee-1.html',{'jsb_students':jsb_students,'ssb_students':ssb_students})	
	jsb_students = Student.objects.filter(spellbee_type='JSB (Junior Spell Bee)')
	ssb_students = Student.objects.filter(spellbee_type='SSB (Senior Spell Bee)')
	return render(request,'SpellBee-1.html',{'jsb_students':jsb_students,'ssb_students':ssb_students})

def home(request):
	return render(request,'index.html')

def junior_spellbee(request):
	import pdb;pdb.set_trace()
	# student=Student.objects.get(id=pk)
	students = Student.objects.filter(phase='Phase 2')
	for student in students:
		words = AudioInput.objects.filter(spellbee_type='JSB (Junior Spell Bee)',phase='Phase 2')
		# word = words.order_by('?').first()
		easy_words = words.filter(difficulty_level='Easy')
		medium_words = words.filter(difficulty_level='Medium')
		hard_words = words.filter(difficulty_level='Hard')
		easy_word = easy_words.order_by('?').first()
		medium_word = medium_words.order_by('?').first()
		hard_word = hard_words.order_by('?').first()
		easy_word
		question = PhaseQuestions.objects.filter(word__difficulty_level='Easy',student=student,phase_type='Phase 2')
		if question:
			print 'pass'
		else:
			question = PhaseQuestions()
			question.word = easy_word
			question.student= student
			question.phase_type = 'Phase 2'
			question.save()
		mquestion = PhaseQuestions.objects.filter(word__difficulty_level='Medium',student=student,phase_type='Phase 2')	
		if mquestion:
			print 'pass'
		else:
			question = PhaseQuestions()
			question.word = medium_word
			question.student= student
			question.phase_type = 'Phase 2'
			question.save()
		hquestion = PhaseQuestions.objects.filter(word__difficulty_level='Hard',student=student,phase_type='Phase 2')	
		if hquestion:
			print 'pass'
		else:
			question = PhaseQuestions()
			question.word = hard_word
			question.student= student
			question.phase_type = 'Phase 2'
			question.save()
	# questions_answered = 
	if request.method == 'POST':
		# import pdb;pdb.set_trace()
		phase_type = request.POST['phase_type']
		word = request.POST['word']
		student_input = request.POST['response']
		school = request.POST['school']
		student = request.POST['student']
		student = Student.objects.get(id=student)
		question_asked = PhaseQuestions.objects.get(student=student,word__word=word)
		audio_word = AudioInput.objects.get(word=word)
		# phasequestions = PhaseQuestions.objects.filter(student=student,is_answered=False)
		# question = phasequestions.order_by('?').first()
		question_asked.is_answered = True
		if word.lower() == student_input.lower():
			question_asked.is_correct= True
		question_asked.student_input = student_input.lower()
		question_asked.save()
		return HttpResponse(json.dumps({
						'type': 'success',
						'data': 'None'
					}))
	# import pdb;pdb.set_trace()
	test_complete = False
	show_next = True
	show_next_round =False
	phase_easy_questions = PhaseQuestions.objects.filter(is_answered=False,word__difficulty_level='Easy',phase_type='Phase 2')
	phase_medium_questions = PhaseQuestions.objects.filter(is_answered=False,word__difficulty_level='Medium',phase_type='Phase 2')
	phase_hard_questions = PhaseQuestions.objects.filter(is_answered=False,word__difficulty_level='Hard',phase_type='Phase 2')
	difficulty_level = 'Easy'
	if len(phase_easy_questions)>0:
		question = phase_easy_questions.order_by('?').first()
		difficulty_level = 'Easy'
	elif len(phase_medium_questions)>0 and len(phase_easy_questions) == 0:
		question = phase_medium_questions.order_by('?').first()
		difficulty_level = 'Medium'
	elif len(phase_hard_questions) > 0 and len(phase_medium_questions) == 0:
		question = phase_hard_questions.order_by('?').first()
		difficulty_level = 'Hard'
	elif len(phase_hard_questions) == 0 and len(phase_medium_questions) == 0 and len(phase_easy_questions) == 0:
		question = None
		test_complete = True
	# if len()
	answered_questions = []	
	ans_questions = PhaseQuestions.objects.filter(is_answered=True,phase_type='Phase 2')
	for aq in ans_questions:
		answered_questions.append(aq)
	if question is not None:
		answered_questions.append(question)
		#easy question
		# for student in students:
		# 	easy_question = PhaseQuestions.objects.filter(is_answered=True,word__difficulty_level='Easy',student=student)
		# 	if len(easy_question) == 0:

			# medium_question = PhaseQuestions.objects.filter(is_answered=True,word__difficulty_level='Medium',student=student)
			# # hard_questions = PhaseQuestions.objects.filter(is_answered=True,word__difficulty_level='Hard',student=student)
			# if len(easy_question)==1:

	# test_complete = False
	# show_next_round = False
	# show_next = True
	# easy_questions_answered = PhaseQuestions.objects.filter(student=student,phase_type='Phase 2',is_answered=True,word__difficulty_level='Easy')
	# if len(easy_questions_answered)==1:
	# 	show_next = False
	# 	show_next_round = True
	# 	phase_questions = PhaseQuestions.objects.filter(student=student,phase_type='Phase 2',is_answered=False,word__difficulty_level='Easy') 	
	# # elif len(easy_questions_answered)>1:
	# 	# show_next_round = True
	# 	# phase_questions = PhaseQuestions.objects.filter(student=student,phase_type='Phase 2',is_answered=False,word__difficulty_level='Medium')
	# else:
	# 	phase_questions = PhaseQuestions.objects.filter(student=student,phase_type='Phase 2',is_answered=False,word__difficulty_level='Easy') 	
	# medium_questions_answered = PhaseQuestions.objects.filter(student=student,phase_type='Phase 2',is_answered=True,word__difficulty_level='Medium')
	# if len(medium_questions_answered)==1:
	# 	show_next = False
	# 	show_next_round = True
	# 	phase_questions = PhaseQuestions.objects.filter(student=student,phase_type='Phase 2',is_answered=False,word__difficulty_level='Medium')
	# # elif len(medium_questions_answered)>1:
	# # 	show_next_round = True
	# # 	phase_questions = PhaseQuestions.objects.filter(student=student,phase_type='Phase 2',is_answered=False,word__difficulty_level='Difficult')
	# elif len(easy_questions_answered) == 2:
	# 	phase_questions = PhaseQuestions.objects.filter(student=student,phase_type='Phase 2',is_answered=False,word__difficulty_level='Medium')
	# 	show_next = True
	# 	show_next_round = False	
	# hard_questions_answered = PhaseQuestions.objects.filter(student=student,phase_type='Phase 2',is_answered=True,word__difficulty_level='Hard')	
	# if len(hard_questions_answered)==1:
	# 	show_next =True
	# 	show_next_round = False
	# 	phase_questions = PhaseQuestions.objects.filter(student=student,phase_type='Phase 2',is_answered=False,word__difficulty_level='Hard')
	# elif len(hard_questions_answered)>1:
	# 	test_complete = True
	# 	show_next = False
	# 	phase_questions = []
	# elif len(medium_questions_answered) == 2:
	# 	phase_questions = PhaseQuestions.objects.filter(student=student,phase_type='Phase 2',is_answered=False,word__difficulty_level='Hard')
	# 	show_next = True
	# 	show_next_round = False
	# questions_answered = PhaseQuestions.objects.filter(student=student,is_answered=True)
	# # phase_questions = PhaseQuestions.objects.filter(student=student,phase_type='Phase 2',is_answered=False)
	# if phase_questions !=[]:
	# 	question = phase_questions.order_by('?').first()
	# 	difficulty_level = question.word.difficulty_level
	# else:
	# 	question = []
	# 	difficulty_level = 'Hard'
	return render(request,'contest-jr.html',{'question':question,'answered':answered_questions,'show_next':show_next,'show_next_round':show_next_round,'test_complete':test_complete,'difficulty_level':difficulty_level})
def display_all_junior_spellbee(request):
	junior_students = Student.objects.filter(spellbee_type='JSB (Junior Spell Bee)',phase='Phase 2')
	return render(request,'student-select-jr.html',{'jsb_students':junior_students})
def senior_spellbee(request):
	return render(request,'contest-sr.html')

def senior_spellbee(request,pk):
	student=Student.objects.get(id=pk)
	words = AudioInput.objects.filter(spellbee_type='SSB (Senior Spell Bee)',phase='Phase 2')
	# word = words.order_by('?').first()
	for word in words:
		try:
			question = PhaseQuestions.objects.get(word=word,student=student,phase_type='Phase 2')
		except:
			question = PhaseQuestions()
		question.word = word
		question.student= student
		question.phase_type = 'Phase 2'
		question.save()
	# questions_answered = 
	if request.method == 'POST':
		import pdb;pdb.set_trace()
		phase_type = request.POST['phase_type']
		word = request.POST['word']
		student_input = request.POST['response']
		school = request.POST['school']
		student = request.POST['student']
		student = Student.objects.filter(school_name=school,first_name=student,spellbee_type='SSB (Senior Spell Bee)')
		question_asked = PhaseQuestions.objects.get(student=student[0],word__word=word)
		audio_word = AudioInput.objects.get(word=word)
		# phasequestions = PhaseQuestions.objects.filter(student=student,is_answered=False)
		# question = phasequestions.order_by('?').first()
		question_asked.is_answered = True
		if word.lower() == student_input.lower():
			question_asked.is_correct= True
		question_asked.save()
		return HttpResponse(json.dumps({
						'type': 'success',
						'data': 'None'
					}))
	questions_answered = PhaseQuestions.objects.filter(student=student,is_answered=True)
	phase_questions = PhaseQuestions.objects.filter(student=student,phase_type='Phase 2',is_answered=False)
	question = phase_questions.order_by('?').first()
	return render(request,'contest-jr.html',{'question':question,'answered':questions_answered})


def select_phase_junior(request):
	return render(request,'select_phase_junior.html')
def phase1_results(request):
	junior_students = Student.objects.filter(spellbee_type='JSB (Junior Spell Bee)')
	for student in junior_students:
		try:
			phase_result = PhaseResults.objects.get(student=student)
		except:
			phase_result = PhaseResults()
			phase_result.correct_answers = '0'
			phase_result.student = student
			phase_result.save()
	phase_results = PhaseResults.objects.all()
	if request.method == 'POST':

		import pdb;pdb.set_trace()
		result_data = data = json.loads(request.POST['data'])
		for rdata in result_data:
			student = Student.objects.get(id=rdata['student_id'])
			phase_result = PhaseResults.objects.get(student=student)
			phase_result.student = student
			phase_result.is_qualified_for_phase2 = True
			phase_result.correct_answers = rdata['score']
			phase_result.save()

	return render(request,'update_phase1_results.html',{'phase_results':phase_results})

def junior_phase1(request):
	words = AudioInput.objects.filter(spellbee_type='JSB (Junior Spell Bee)',phase='Phase 1')
	# word = words.order_by('?').first()
	for word in words:
		try:
			question = PhaseQuestions.objects.get(word=word,phase_type='Phase 1')
		except:
			question = PhaseQuestions()
		question.word = word
		question.phase_type = 'Phase 1'
		question.save()
	if request.method == 'POST':
		pk = request.POST['id']
		asked = PhaseQuestions.objects.get(id=pk)
		asked.is_answered = True
		asked.save()
	phase1_finished = False
	question_ans = PhaseQuestions.objects.filter(is_answered=True,phase_type='Phase 1')
	if len(question_ans)>2:
		phase1_finished = True
	ask_question = PhaseQuestions.objects.filter(is_answered=False,phase_type='Phase 1').first()
	return render(request,'juniorphase1.html',{'question':ask_question,'finished':phase1_finished})

def check_total_score(request):
	# import pdb;pdb.set_trace()
	students = Student.objects.filter(phase='Phase 2')
	phase_results = []
	for student in students:
		results = PhaseQuestions.objects.filter(student=student)
		score = phase_results.filter(is_correct=True).count()
	return render(request,'phase2testresults.html',{'results':phase_results,'score':score})


# def phase(request):
# 	
# def check_phase_result(request):
# 	phase_type = request.POST['phase_type']
# 	word = request.POST['word']
# 	student_input = request.POST['user_input']
# 	school = request.POST['school']
# 	student = request.POST['student']
# 	student = Student.objects.filter(school_name=school,first_name=student)
# 	question_asked = PhaseQuestions.objects.get(student=student,word__word=word)
# 	audio_word = AudioInput.objects.get(word=word)
# 	phasequestions = PhaseQuestions.objects.filter(student=student,is_answered=False)
# 	question = phase_questions.order_by('?').first()
# 	question_asked.is_answered = True
# 	if word.lower == student_input.lower():
# 		question_asked.is_correct= True
# 	question_asked.save()
# 	questions_answered = PhaseQuestions.objects.filter(student=student,is_answered=True)
# 	# nodes = PostPatchSchedule.objects.filter(scheduledate=schedule_date)
# 	list_data = []
# 	for node in questions_answered:
# 		answer_data = {}
# 		answer_data['student'] = node.student.student
# 		answer_data['school'] = node.student.school_name
# 		answer_data['class'] = node.student.class_name
# 		answer_data['word'] = node.word.word
# 		answer_data['input'] = node.student_input
# 		answer_data['result'] = node.is_correct
# 		list_data.append(answer_data)
# 		patch_data = None
# 	# data = serializers.serialize("json", nodes)
# 	# data = serializers.serialize('json', nodes, fields=('scheduledate','time','rni_name','rni_id'))
# 	# nodes= json.dumps(nodes)
# 	return HttpResponse(json.dumps({
# 						'type': 'success',
# 						'data': list_data
# 					}))
# 	return HttpResponse(json.dumps())

		

