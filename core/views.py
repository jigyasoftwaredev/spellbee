# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import AudioInput,Student,PhaseQuestions,Phase2Result,PhaseResults,ShowIntroduction

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from dateutil.parser import parse

from django.http import HttpResponse
import json
# Create your views here.
def save_audio(request):
	jsb_words = AudioInput.objects.filter(spellbee_type='JSB (Junior Spell Bee)')
	ssb_words = AudioInput.objects.filter(spellbee_type='SSB (Senior Spell Bee)')
	if request.method == 'POST':
		try:
			myfile = ''
			myfile = request.FILES['myfile']
			try:
				sentence_file = request.FILES['sentencefile']
				fs = FileSystemStorage()
				file_sentence = fs.save(sentence_file.name, sentence_file)
				uploaded_file_sentence_url = fs.url(file_sentence)
			except:
				file_sentence = None
				pass
			try:
				definition_file = request.FILES['definitionfile']
				fs = FileSystemStorage()
				file_definition = fs.save(definition_file.name, definition_file)
				uploaded_file_sentence_url = fs.url(file_definition)
			except:
				file_definition = None
				pass
			try:
				origin_file = request.FILES['originfile']
				fs = FileSystemStorage()
				file_origin = fs.save(origin_file.name,origin_file)
				uploaded_file_sentence_url = fs.url(file_origin)
			except:
				file_origin = None
				pass
			try:
				complete_file = request.FILES['completefile']
				fs = FileSystemStorage()
				file_complete = fs.save(complete_file.name,complete_file)
				uploaded_file_sentence_url = fs.url(file_complete)
			except:
				file_complete = None
				pass
			fs = FileSystemStorage()
			filename = fs.save(myfile.name, myfile)
			uploaded_file_url = fs.url(filename)
			input_name = AudioInput()
			input_name.word = request.POST['word']
			input_name.file_name = filename
			input_name.file_name_origin = file_origin
			input_name.file_name_sentence = file_sentence
			input_name.file_name_complete = file_complete
			input_name.fill_name_definition = file_definition
			input_name.pronunciation = request.POST['pronunciation']
			input_name.pos = request.POST['pos']
			input_name.land_of_origin = request.POST['land_of_origin']
			input_name.additional_info = request.POST['additional_info']
			input_name.sentence = request.POST['added_by']
			input_name.created_by = request.POST['created_by']
			input_name.spellbee_type = request.POST['spellbee_type']
			input_name.phase = request.POST['phase']
			input_name.year = request.POST['year']
			input_name.difficulty_level = request.POST['difficulty']
			try:
				word = AudioInput.objects.filter(word=input_name.word)
				if word:
					return render(request,'words.html',{'jsb_words':jsb_words,'ssb_words':ssb_words,'failure':'exist'})		
			except:
				pass
			input_name.save()
		except:
			return render(request,'words.html',{'jsb_words':jsb_words,'ssb_words':ssb_words,'failure':'failure'})
			pass
		return render(request,'words.html',{'jsb_words':jsb_words,'ssb_words':ssb_words,'failure':'success'})
	jsb_words = AudioInput.objects.filter(spellbee_type='JSB (Junior Spell Bee)')
	ssb_words = AudioInput.objects.filter(spellbee_type='SSB (Senior Spell Bee)')
	return render(request,'words.html',{'jsb_words':jsb_words,'ssb_words':ssb_words,'failure':'donno'})


def contests(request):
	return render(request,'contest-select.html')

def students(request):
	if request.method == 'POST':
		input_name = Student()
		input_name.first_name = request.POST['first_name']
		input_name.last_name = request.POST['last_name']
		input_name.father_name = request.POST['father_name']
		input_name.gender = request.POST['optionsRadios']
		input_name.dob = parse(request.POST['dob'])
		input_name.class_name = request.POST['class_name']
		input_name.spellbee_type = request.POST['spellbee_type']
		input_name.phase = request.POST['phase']
		input_name.region = request.POST['school_name']
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

def update_next_round(request):
	intro = ShowIntroduction.objects.get(into_id='1')
	intro.round_finished = False
	intro.save()
	return HttpResponse(json.dumps({
			'type':'success',
			'msg':'Saved Successfully'
			}))


def check_usage(word):
	check = PhaseQuestions.objects.filter(word__word=word)
	if check:
		return True
	else:
		return False
def junior_spellbee(request):
	show = 'junior_phase2'
	# import pdb;pdb.set_trace()
	# student=Student.objects.get(id=pk)
	students = Student.objects.filter(spellbee_type='JSB (Junior Spell Bee)')
	for student in students:
		words = AudioInput.objects.filter(spellbee_type='JSB (Junior Spell Bee)',phase='Phase 2')
		# word = words.order_by('?').first()
		easy_words = words.filter(difficulty_level='Easy')
		medium_words = words.filter(difficulty_level='Medium')
		hard_words = words.filter(difficulty_level='Hard')
		for word in easy_words:
			usage = check_usage(word.word)
			if usage == False:
				easy_word = word
				break
		for mword in medium_words:
			usage = check_usage(mword.word)
			if usage == False:
				medium_word = mword
		for hword in hard_words:
			usage = check_usage(hword.word)
			if usage == False:
				hard_word = hword

		# easy_word = easy_words.order_by('?').first()
		# medium_word = medium_words.order_by('?').first()
		# hard_word = hard_words.order_by('?').first()
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
	round_name=''
	try:
		intro = ShowIntroduction.objects.get(into_id='1')
	except:
		intro = ShowIntroduction()
		intro.round_finished = True
		intro.save() 
	test_complete = False
	show_next = True
	show_next_round =False
	check_round = '1'
	phase_easy_questions = PhaseQuestions.objects.filter(is_answered=False,word__difficulty_level='Easy',phase_type='Phase 2')
	phase_medium_questions = PhaseQuestions.objects.filter(is_answered=False,word__difficulty_level='Medium',phase_type='Phase 2')
	phase_hard_questions = PhaseQuestions.objects.filter(is_answered=False,word__difficulty_level='Hard',phase_type='Phase 2')
	difficulty_level = 'Easy'
	if len(phase_easy_questions)>0:
		question = phase_easy_questions.order_by('?').first()
		difficulty_level = 'Easy'
	elif len(phase_medium_questions)>0 and len(phase_easy_questions) == 0:
		if intro.round_finished:
			difficulty_level ='Easy'
			show_next_round =True
			round_name = '2'
			question = None
			show_next =False
		else:
			question = phase_medium_questions.order_by('?').first()
			difficulty_level = 'Medium'
			if len(phase_medium_questions) ==1:
				intro.round_finished = True
				intro.save()
	elif len(phase_hard_questions) > 0 and len(phase_medium_questions) == 0:
		if intro.round_finished:
			difficulty_level ='Medium'
			show_next_round =True
			round_name = '3'
			question = None
			show_next =False
		else:
			question = phase_hard_questions.order_by('?').first()
			difficulty_level = 'Hard'
	elif len(phase_hard_questions) == 0 and len(phase_medium_questions) == 0 and len(phase_easy_questions) == 0:
		question = None
		test_complete = True
		show_next = False
		difficulty_level = 'Hard'
		intro.round_finished = True
		intro.save()
	student_response = []
	if difficulty_level == 'Easy':
		questions_asked = PhaseQuestions.objects.filter(word__difficulty_level='Easy',is_answered=True,phase_type='Phase 2')
 	elif difficulty_level == 'Medium':
 		questions_asked = PhaseQuestions.objects.filter(word__difficulty_level='Medium',is_answered=True,phase_type='Phase 2')
 	elif difficulty_level == 'Hard':
 		questions_asked = PhaseQuestions.objects.filter(word__difficulty_level='Hard',is_answered=True,phase_type='Phase 2')
 	# import pdb;pdb.set_trace()
 	for aquestion in questions_asked:
 		student_name = str(aquestion.student.first_name)+str(aquestion.student.last_name)
 		student_response.append([student_name,aquestion.student.class_name,aquestion.word.word,aquestion.student_input,str(aquestion.is_correct)])
 	if question:	
 		student_name = str(question.student.first_name)+str(question.student.last_name)
 		student_response.append([student_name,question.student.class_name,question.word.word,'','NO'])
 	# for student in students:
		# results = []
		# student_name = str(student.first_name)+str(student.last_name)
		# class_name = student.class_name
		# round1_response = PhaseQuestions.objects.filter(student=student,word__difficulty_level='Easy')
		# if round1_response:
		# 	word_round1_response = ''
		# 	if round1_response[0].student_input:
		# 		word_round1_response = round1_response[0].student_input
		# 	word_round1 = round1_response[0].word.word
		# 	word_round1_iscorrect = str(round1_response[0].is_correct)
		# 	# import pdb;pdb.set_trace()
		# 	if round1_response[0].student_input is None:
		# 		word_round1_iscorrect = 'NO'
		# else:
		# 	word_round1_response = ''
		# 	word_round1_iscorrect = 'NO'
		# round2_response = PhaseQuestions.objects.filter(student=student,word__difficulty_level='Medium')
		# if round2_response:
		# 	word_round2_response = ''
		# 	if round2_response[0].student_input:
		# 		word_round2_response = round2_response[0].student_input
		# 	word_round2 = round2_response[0].word.word
		# 	word_round2_iscorrect = str(round2_response[0].is_correct)
		# 	if round2_response[0].student_input is None:
		# 		word_round2_iscorrect = 'NO'
		# else:
		# 	word_round2_response = ''
		# 	word_round2_iscorrect = 'NO'
		# round3_response = PhaseQuestions.objects.filter(student=student,word__difficulty_level='Hard')
		# if round3_response:
		# 	word_round3_response = ''
		# 	if round3_response[0].student_input:
		# 		word_round3_response = round3_response[0].student_input
		# 	word_round3 = round3_response[0].word.word
		# 	word_round3_iscorrect = str(round3_response[0].is_correct)
		# 	if round3_response[0].student_input is None:
		# 		word_round3_iscorrect = 'NO'
		# else:
		# 	word_round3_response = ''
		# 	word_round3_iscorrect = 'NO'
		# # student_response.append([student_name,class_name,word_round1_response,word_round1_iscorrect,word_round2_response,word_round2_iscorrect,word_round3_response,word_round3_iscorrect])
		# if difficulty_level == 'Easy':
		# 	student_response.append([student_name,class_name,word_round1,word_round1_response,word_round1_iscorrect])
		# elif difficulty_level == 'Medium':
		# 	student_response.append([student_name,class_name,word_round2,word_round2_response,word_round2_iscorrect])
		# elif difficulty_level == 'Hard':
		# 	student_response.append([student_name,class_name,word_round3,word_round3_response,word_round3_iscorrect])

		# student_response.append(results)
	# import pdb;pdb.set_trace()
	# if len()
	# answered_questions = []	
	# ans_questions = PhaseQuestions.objects.filter(is_answered=True,phase_type='Phase 2')
	# for aq in ans_questions:
	# 	answered_questions.append(aq)
	# if question is not None:
	# 	answered_questions.append(question)
	return render(request,'contest-jr.html',{'question':question,'answered':student_response,'show_next':show_next,'show_next_round':show_next_round,'test_complete':test_complete,'difficulty_level':difficulty_level,'round_name':round_name})
def display_all_junior_spellbee(request):
	junior_students = Student.objects.filter(spellbee_type='JSB (Junior Spell Bee)',phase='Phase 2')
	return render(request,'student-select-jr.html',{'jsb_students':junior_students})
def senior_spellbee(request):
	return render(request,'contest-sr.html')

def senior_spellbee(request):
	show = 'junior_phase2'
	# import pdb;pdb.set_trace()
	# student=Student.objects.get(id=pk)
	students = Student.objects.filter(spellbee_type='SSB (Senior Spell Bee)')
	for student in students:
		words = AudioInput.objects.filter(spellbee_type='SSB (Senior Spell Bee)',phase='Phase 2')
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
	try:
		intro = ShowIntroduction.objects.get(into_id='1')
	except:
		intro = ShowIntroduction()
		intro.round_finished = True
		intro.save() 
	test_complete = False
	show_next = True
	show_next_round =False
	check_round = '1'
	phase_easy_questions = PhaseQuestions.objects.filter(is_answered=False,word__difficulty_level='Easy',phase_type='Phase 2',student__spellbee_type='SSB (Senior Spell Bee)')
	phase_medium_questions = PhaseQuestions.objects.filter(is_answered=False,word__difficulty_level='Medium',phase_type='Phase 2',student__spellbee_type='SSB (Senior Spell Bee)')
	phase_hard_questions = PhaseQuestions.objects.filter(is_answered=False,word__difficulty_level='Hard',phase_type='Phase 2',student__spellbee_type='SSB (Senior Spell Bee)')
	difficulty_level = 'Easy'
	if len(phase_easy_questions)>0:
		question = phase_easy_questions.order_by('?').first()
		difficulty_level = 'Easy'
	elif len(phase_medium_questions)>0 and len(phase_easy_questions) == 0:
		if intro.round_finished:
			difficulty_level ='Easy'
			show_next_round =True
			question = None
			show_next =False
		else:
			question = phase_medium_questions.order_by('?').first()
			difficulty_level = 'Medium'
			if len(phase_medium_questions) ==1:
				intro.round_finished = True
				intro.save()
	elif len(phase_hard_questions) > 0 and len(phase_medium_questions) == 0:
		if intro.round_finished:
			difficulty_level ='Medium'
			show_next_round =True
			question = None
			show_next =False
		else:
			question = phase_hard_questions.order_by('?').first()
			difficulty_level = 'Hard'
	elif len(phase_hard_questions) == 0 and len(phase_medium_questions) == 0 and len(phase_easy_questions) == 0:
		question = None
		test_complete = True
		show_next = False
		difficulty_level = 'Hard'
		intro.round_finished = True
		intro.save()
	student_response = []
	for student in students:
		results = []
		student_name = str(student.first_name)+str(student.last_name)
		class_name = student.class_name
		round1_response = PhaseQuestions.objects.filter(student=student,word__difficulty_level='Easy')
		if round1_response:
			word_round1_response = ''
			if round1_response[0].student_input:
				word_round1_response = round1_response[0].student_input
			word_round1 = round1_response[0].word.word
			word_round1_iscorrect = str(round1_response[0].is_correct)
			# import pdb;pdb.set_trace()
			if round1_response[0].student_input is None:
				word_round1_iscorrect = 'NO'
		else:
			word_round1_response = ''
			word_round1_iscorrect = 'NO'
		round2_response = PhaseQuestions.objects.filter(student=student,word__difficulty_level='Medium')
		if round2_response:
			word_round2_response = ''
			if round2_response[0].student_input:
				word_round2_response = round2_response[0].student_input
			word_round2 = round2_response[0].word.word
			word_round2_iscorrect = str(round2_response[0].is_correct)
			if round2_response[0].student_input is None:
				word_round2_iscorrect = 'NO'
		else:
			word_round2_response = ''
			word_round2_iscorrect = 'NO'
		round3_response = PhaseQuestions.objects.filter(student=student,word__difficulty_level='Hard')
		if round3_response:
			word_round3_response = ''
			if round3_response[0].student_input:
				word_round3_response = round3_response[0].student_input
			word_round3 = round3_response[0].word.word
			word_round3_iscorrect = str(round3_response[0].is_correct)
			if round3_response[0].student_input is None:
				word_round3_iscorrect = 'NO'
		else:
			word_round3_response = ''
			word_round3_iscorrect = 'NO'
		# student_response.append([student_name,class_name,word_round1_response,word_round1_iscorrect,word_round2_response,word_round2_iscorrect,word_round3_response,word_round3_iscorrect])
		if difficulty_level == 'Easy':
			student_response.append([student_name,class_name,word_round1,word_round1_response,word_round1_iscorrect])
		elif difficulty_level == 'Medium':
			student_response.append([student_name,class_name,word_round2,word_round2_response,word_round2_iscorrect])
		elif difficulty_level == 'Hard':
			student_response.append([student_name,class_name,word_round3,word_round3_response,word_round3_iscorrect])

		# student_response.append(results)
	# import pdb;pdb.set_trace()
	# if len()
	# answered_questions = []	
	# ans_questions = PhaseQuestions.objects.filter(is_answered=True,phase_type='Phase 2')
	# for aq in ans_questions:
	# 	answered_questions.append(aq)
	# if question is not None:
	# 	answered_questions.append(question)
	return render(request,'contest-sr.html',{'question':question,'answered':student_response,'show_next':show_next,'show_next_round':show_next_round,'test_complete':test_complete,'difficulty_level':difficulty_level})

def select_phase_junior(request):
	return render(request,'select_phase_junior.html')
def phase1_results(request):
	show_phase = 'phase_one_result'
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
		# import pdb;pdb.set_trace()
		result_data = data = json.loads(request.POST['data'])
		for rdata in result_data:
			student = Student.objects.get(id=rdata['student_id'])
			phase_result = PhaseResults.objects.get(student=student)
			phase_result.student = student
			phase_result.is_qualified_for_phase2 = True
			phase_result.correct_answers = rdata['score']
			phase_result.save()
		return HttpResponse(json.dumps({
                        'type': 'success',
                        'message': 'Phase I Results Updated Successfully'
                    }))   

	return render(request,'update_phase1_results.html',{'phase_results':phase_results})

def senior_phase1_results(request):
	show_phase = 'phase_one_result'
	junior_students = Student.objects.filter(spellbee_type='SSB (Senior Spell Bee)')
	for student in junior_students:
		try:
			phase_result = PhaseResults.objects.get(student=student)
		except:
			phase_result = PhaseResults()
			phase_result.correct_answers = '0'
			phase_result.student = student
			phase_result.save()
	phase_results = PhaseResults.objects.filter(student__spellbee_type='SSB (Senior Spell Bee)')
	if request.method == 'POST':
		# import pdb;pdb.set_trace()
		result_data = data = json.loads(request.POST['data'])
		for rdata in result_data:
			student = Student.objects.get(id=rdata['student_id'])
			phase_result = PhaseResults.objects.get(student=student)
			phase_result.student = student
			phase_result.is_qualified_for_phase2 = True
			phase_result.correct_answers = rdata['score']
			phase_result.save()
		return HttpResponse(json.dumps({
                        'type': 'success',
                        'message': 'Phase I Results Updated Successfully'
                    }))   

	return render(request,'update_phase1_results_senior.html',{'phase_results':phase_results})

# def change_introduction(request):
# 	from core.models import ShowIntroduction
# 	try:
# 		ss = ShowIntroduction.objects.get(id=1)
# 	except:
# 		ss = ShowIntroduction()

# 	ss.show = False
# 	ss.save()


def senior_phase1(request):
	show_intro =False
	from core.models import ShowIntroduction
	try:
		ss = ShowIntroduction.objects.get(id=1)
	except:
		ss = ShowIntroduction()
	ss.show = False
	ss.save()
	show_phase = 'junior_phase1'
	words = AudioInput.objects.filter(spellbee_type='SSB (Senior Spell Bee)',phase='Phase 1')
	# word = words.order_by('?').first()
	easy_words = AudioInput.objects.filter(spellbee_type='SSB (Senior Spell Bee)',phase='Phase 1',difficulty_level='Easy')
	medium_words = AudioInput.objects.filter(spellbee_type='SSB (Senior Spell Bee)',phase='Phase 1',difficulty_level='Medium')
	hard_words = AudioInput.objects.filter(spellbee_type='SSB (Senior Spell Bee)',phase='Phase 1',difficulty_level='Hard')
	for word in easy_words:
		question = PhaseQuestions.objects.filter(phase_type='Phase 1',word__difficulty_level='Easy')
		if question:
			show_intro = False
			print 'Pass'
		else:
			show_intro =True
			question = PhaseQuestions()
			question.word = word
			question.phase_type = 'Phase 1'
			question.save()
	for word in medium_words:
		question = PhaseQuestions.objects.filter(phase_type='Phase 1',word__difficulty_level='Medium')
		if question:
			print 'Pass'
		else:
			show_intro =True	
			question = PhaseQuestions()
			question.word = word
			question.phase_type = 'Phase 1'
			question.save()
	for word in hard_words:
		question = PhaseQuestions.objects.filter(phase_type='Phase 1',word__difficulty_level='Hard')
		if question:
			print 'Pass'
		else:
			show_intro =True	
			question = PhaseQuestions()
			question.word = word
			question.phase_type = 'Phase 1'
			question.save()
	# import pdb;pdb.set_trace()
	if request.method == 'POST':
		pk = request.POST['id']
		asked = PhaseQuestions.objects.get(id=pk)
		asked.is_answered = True
		asked.save()
	phase1_finished = False
	question_ans = PhaseQuestions.objects.filter(is_answered=True,phase_type='Phase 1')
	# if len(question_ans) == 0:
	# 	show_intro = True
	# import pdb;pdb.set_trace()
	show_next = True
	if len(question_ans)>=2:
		phase1_finished = True
		show_next = False
	ask_question = PhaseQuestions.objects.filter(is_answered=False,phase_type='Phase 1').first()
	return render(request,'seniorphase1.html',{'question':ask_question,'finished':phase1_finished,'show_intro':show_intro,'show_next':show_next,'show_intro':show_intro})


def junior_phase1(request):
	show_intro =False
	from core.models import ShowIntroduction
	try:
		ss = ShowIntroduction.objects.get(id=1)
	except:
		ss = ShowIntroduction()
	ss.show = False
	ss.save()
	show_phase = 'junior_phase1'
	words = AudioInput.objects.filter(spellbee_type='JSB (Junior Spell Bee)',phase='Phase 1')
	# word = words.order_by('?').first()
	easy_words = AudioInput.objects.filter(spellbee_type='JSB (Junior Spell Bee)',phase='Phase 1',difficulty_level='Easy')
	medium_words = AudioInput.objects.filter(spellbee_type='JSB (Junior Spell Bee)',phase='Phase 1',difficulty_level='Medium')
	hard_words = AudioInput.objects.filter(spellbee_type='JSB (Junior Spell Bee)',phase='Phase 1',difficulty_level='Hard')
	for word in easy_words:
		question = PhaseQuestions.objects.filter(phase_type='Phase 1',word__difficulty_level='Easy')
		if question:
			show_intro = False
			print 'Pass'
		else:
			show_intro =False
			show_next =False
			question = PhaseQuestions()
			question.word = word
			question.phase_type = 'Phase 1'
			question.save()
	for word in medium_words:
		question = PhaseQuestions.objects.filter(phase_type='Phase 1',word__difficulty_level='Medium')
		if question:
			print 'Pass'
		else:
			show_intro =False	
			question = PhaseQuestions()
			question.word = word
			question.phase_type = 'Phase 1'
			question.save()
	for word in hard_words:
		question = PhaseQuestions.objects.filter(phase_type='Phase 1',word__difficulty_level='Hard')
		if question:
			print 'Pass'
		else:
			show_intro =False
			question = PhaseQuestions()
			question.word = word
			question.phase_type = 'Phase 1'
			question.save()
	# import pdb;pdb.set_trace()
	if request.method == 'POST':
		pk = request.POST['id']
		asked = PhaseQuestions.objects.get(id=pk)
		asked.is_answered = True
		asked.save()
	phase1_finished = False
	question_ans = PhaseQuestions.objects.filter(is_answered=True,phase_type='Phase 1')
	# if len(question_ans) == 0:
	# 	show_intro = True
	# import pdb;pdb.set_trace()
	show_next = True
	if show_intro == True:
		show_next = False
	if len(question_ans)>=2:
		phase1_finished = True
		show_next = False
	ask_question = PhaseQuestions.objects.filter(is_answered=False,phase_type='Phase 1').first()
	return render(request,'juniorphase1.html',{'question':ask_question,'finished':phase1_finished,'show_intro':show_intro,'show_next':show_next,'show_intro':show_intro})

def check_total_score(request):
	# import pdb;pdb.set_trace()
	# import pdb;pdb.set_trace()
	student_response = []
	students = Student.objects.filter(spellbee_type='JSB (Junior Spell Bee)')
	phase_results = []
	for student in students:
		results = []
		student_name = str(student.first_name)+str(student.last_name) + '( '+str(student.class_name) + ' )'
		round1_response = PhaseQuestions.objects.filter(student=student,word__difficulty_level='Easy')
		phase1_questions_count = PhaseQuestions.objects.filter(phase_type='Phase 1').count()
		phase1 = PhaseResults.objects.filter(student=student)
		if phase1:
			phase1_score = phase1[0].correct_answers
		if round1_response:
			word_round1_response = round1_response[0].student_input
			word_round1_iscorrect = str(round1_response[0].is_correct)
			word_round1_input = round1_response[0].word.word
			# import pdb;pdb.set_trace()
			if round1_response[0].student_input is None:
				word_round1_iscorrect = 'NO'
		else:
			word_round1_response = ''
			word_round1_iscorrect = 'NO'
		round2_response = PhaseQuestions.objects.filter(student=student,word__difficulty_level='Medium')
		if round2_response:
			word_round2_response = round2_response[0].student_input
			word_round2_iscorrect = str(round2_response[0].is_correct)
			word_round2_input = round2_response[0].word.word
			if round2_response[0].student_input is None:
				word_round2_iscorrect = 'NO'
		else:
			word_round2_response = ''
			word_round2_iscorrect = 'NO'
		round3_response = PhaseQuestions.objects.filter(student=student,word__difficulty_level='Hard')
		if round3_response:
			word_round3_response = round3_response[0].student_input
			word_round3_iscorrect = str(round3_response[0].is_correct)
			word_round3_input = round3_response[0].word.word
			if round3_response[0].student_input is None:
				word_round3_iscorrect = 'NO'
		else:
			word_round3_response = ''
			word_round3_iscorrect = 'NO'
		phase2_score = PhaseQuestions.objects.filter(student=student,is_correct=True).count()
		total_score = int(phase1_score) + phase2_score
		student_response.append([student_name,phase1_questions_count,phase1_score,word_round1_input,word_round1_response,word_round1_iscorrect,word_round2_input,word_round2_response,word_round2_iscorrect,word_round3_input,word_round3_response,word_round3_iscorrect,phase2_score,total_score])
	# import pdb;pdb.set_trace()
	return render(request,'phase2testresults.html',{'results':student_response})


def check_total_score_senior(request):
	# import pdb;pdb.set_trace()
	# import pdb;pdb.set_trace()
	student_response = []
	students = Student.objects.filter(spellbee_type='SSB (Senior Spell Bee)')
	phase_results = []
	for student in students:
		results = []
		student_name = str(student.first_name)+str(student.last_name) + '( '+str(student.class_name) + ' )'
		round1_response = PhaseQuestions.objects.filter(student=student,word__difficulty_level='Easy')
		phase1_questions_count = PhaseQuestions.objects.filter(phase_type='Phase 1').count()
		phase1 = PhaseResults.objects.filter(student=student)
		if phase1:
			phase1_score = phase1[0].correct_answers
		if round1_response:
			word_round1_response = round1_response[0].student_input
			word_round1_iscorrect = str(round1_response[0].is_correct)
			word_round1_input = round1_response[0].word.word
			# import pdb;pdb.set_trace()
			if round1_response[0].student_input is None:
				word_round1_iscorrect = 'NO'
		else:
			word_round1_response = ''
			word_round1_iscorrect = 'NO'
		round2_response = PhaseQuestions.objects.filter(student=student,word__difficulty_level='Medium')
		if round2_response:
			word_round2_response = round2_response[0].student_input
			word_round2_iscorrect = str(round2_response[0].is_correct)
			word_round2_input = round2_response[0].word.word
			if round2_response[0].student_input is None:
				word_round2_iscorrect = 'NO'
		else:
			word_round2_response = ''
			word_round2_iscorrect = 'NO'
		round3_response = PhaseQuestions.objects.filter(student=student,word__difficulty_level='Hard')
		if round3_response:
			word_round3_response = round3_response[0].student_input
			word_round3_iscorrect = str(round3_response[0].is_correct)
			word_round3_input = round3_response[0].word.word
			if round3_response[0].student_input is None:
				word_round3_iscorrect = 'NO'
		else:
			word_round3_response = ''
			word_round3_iscorrect = 'NO'
		phase2_score = PhaseQuestions.objects.filter(student=student,is_correct=True).count()
		total_score = int(phase1_score) + phase2_score
		student_response.append([student_name,phase1_questions_count,phase1_score,word_round1_input,word_round1_response,word_round1_iscorrect,word_round2_input,word_round2_response,word_round2_iscorrect,word_round3_input,word_round3_response,word_round3_iscorrect,phase2_score,total_score])
	# import pdb;pdb.set_trace()
	return render(request,'phase2testresultssenior.html',{'results':student_response})



def update_phase_results_phase_questions(request):
	if request.method == 'POST':
		sss = PhaseQuestions.objects.all()
		for ss in sss:
			ss.delete()
		rrr = PhaseResults.objects.all()
		for rr in rrr:
			rr.delete()
		return HttpResponse(json.dumps({
			'type':'Success',
			'msg':'Deleted Successfully'
			}))
	return render(request,'erase_contest.html')

def show_intro(request):
	return render(request,'intro.html')