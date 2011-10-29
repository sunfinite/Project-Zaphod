#!/usr/bin/env python
#Filename: views.py

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from benjy.models import * #FIXME
import datetime
import hashlib

#large questions: done
#check forms
#resources: done
#the cache problem in firefox
#fix preview


########################## Stupid stuff ###########################
# Does replyCount break normalization? Can we break it?
########################## Handlers ################################

def renderCourses(request):
	return render_to_response('main.html', {'courses': Course.objects.all()})

def renderCoursePage(request, code):
	values = {}
	try: values['course'] = Course.objects.get(code = code)
	except: return  the404()
	values['classes'] = list(Class.objects.filter(forCourse = values['course']))
	for classObj in values['classes']:
		values['questions'] =  values.get('questions', []) + list(Question.objects.filter(forClass = classObj))
		values['assignments'] = values.get('assignments', []) + list(Assignment.objects.filter(forClass = classObj))
		values['resources'] =  values.get('resources', []) + list(Resource.objects.filter(forClass = classObj)) 
	values['classes'] = filter(lambda x: x.id > 0, values['classes'])
	return render_to_response('course.html', values) 

def renderClassPage(request, code, classId): 
	values = {}
	try: values['class'] = Class.objects.get(pk = int(classId))
	except: return the404()
	values['questions'] =  Question.objects.filter(forClass = values['class'])
	values['assignments'] = Assignment.objects.filter(forClass = values['class'])
	values['resources'] =  Resource.objects.filter(forClass = values['class']) 
	return render_to_response('class.html', values) 

#TODO: make these generic and combine
def renderQuestionPage(request, code, objId): 
	objId = int(objId)
	values = {}
	values['code'] = code # being simply passed around to make the urls seem logical
	try: values['question'] = Question.objects.get(pk = objId)
	except: return the404()
	values['replies'] = Reply.objects.filter(forQuestion = objId)
	return render_to_response('question.html', values)

def renderAssignmentPage(request, code, objId): 
	objId = int(objId)
	values = {}
	values['code'] = code 
	try: values['assignment'] = Assignment.objects.get(pk = objId)
	except: return the404()
	values['replies'] = Reply.objects.filter(forAssignment = objId)
	return render_to_response('assignment.html', values)


def renderResourcePage(request, code, objId): pass
	


############################ Helper functions #################################

def formscrewup():
	return "Something was not right with your submit, check and try again."

def decideRender(code, forClass):
	values = {}
	values['code'] = code
	values['class'] = 0
	if forClass == 0: 
		values['standalone'] = True
		values['classes'] = Class.objects.filter(forCourse = Course.objects.get(code = code))
	else:
		values['standalone'] = False
		values['class'] = forClass
	return values

def backup(obj, kind):	

	if kind == 'class':
		backupObj = ClassEdits()
		backupObj.forClass_id = obj.id

	elif kind == 'question':
		backupObj = QuestionEdits()	
		backupObj.forQuestion_id = obj.id 

	elif kind == 'assignment':
		backupObj = AssignmentEdits()
		backupObj.forAssignment_id = obj.id
		
	elif kind == 'resource':
		backupObj = ResourceEdits()
		backupObj.forResource_id = obj.id
		
	elif kind == 'reply':
		backupObj = ReplyEdits()
		backupObj.forReply_id = obj.id
	
	backupObj.__dict__.update(obj.__dict__)
	backupObj.__dict__['id'] = None
	backupObj.save()
	obj.dateEdited = datetime.datetime.now()

@csrf_exempt
def checkPassword(request):
	if request.method == 'GET':
		return HttpResponseRedirect(reverse('views.renderCourses'))

	if request.method == 'POST':
		try: User.objects.get(password = hashlib.md5(request.POST['password']).hexdigest())
		except: return HttpResponse('doesnotexist')

		return HttpResponse('exists')



def the404():
	return HttpResponse("<h2>The ghost in the machine says:</h2><h1>\"One day, I'm gonna grow wings. A chemical reaction. Hysterical and useless.\"</h1>")

def useless(request):
	return render_to_response('readme.html', {})

@csrf_exempt
def getPreview(request):
	if request.method == 'GET':
		return HttpResponseRedirect(reverse('views.renderCourses'))

	if request.method == 'POST':
		return render_to_response("preview.html", {'preview': request.POST['preview']})

###################### Forms #######################################

def courseForm(request, courseId):
	values = {}
	values['courseId'] = int(courseId)

	try: 
		if values['courseId']: values['course'] = Course.objects.get(pk = values['courseId'])
 	except: return the404()

	if request.method == 'GET': return render_to_response('courseform.html', values)

	if request.method == 'POST':
		try:
			if request.POST['password'] != 'courseform': raise

			if 'course' not in values: values['course'] = Course()

			#TODO: validate empty fields at the client
			values['course'].title = request.POST['title']
			values['course'].code = request.POST['code']
			values['course'].teacher = request.POST['teacher']
			values['course'].save()

			if values['courseId'] == 0:
				# default class allows questions, assignments, resources unrelated to any class
				defaultClass = Class(date = datetime.datetime.now(), forCourse = values['course']) 
				defaultClass.id = -values['course'].id # ensure the defaultClass falls outside the normal class range
				defaultClass.user_id = 0
				defaultClass.save()

		except Exception, inst:	
			values['message'] =  inst
			return render_to_response('courseform.html', values)	
		return HttpResponseRedirect(reverse('views.renderCoursePage', args = [request.POST['code']]))


@csrf_exempt#FIXME
def classForm(request, code, classId):
	values = {}
	values['classId'] = int(classId)
	
	try:
		values['course'] = Course.objects.get(code = code)
		if values['classId']: values['class'] = Class.objects.get(pk = classId)
	except: return the404()

	if request.method == 'GET': return render_to_response('classform.html', values)

	if request.method == 'POST':
		if 'class' not in values: values['class'] = Class()
		else: backup(values['class'], 'class')
		try:
			if not values['classId']:
				values['class'].forCourse = values['course']
				values['class'].date = datetime.datetime(int(request.POST['year']), int(request.POST['month']), int(request.POST['day']))
				values['class'].type = request.POST['type']
			

		 	values['class'].user = User.objects.get(password = hashlib.md5(request.POST['password']).hexdigest())			
			values['class'].summary = request.POST['summary']
			values['class'].save()
		except:	
		  	values['message'] = formscrewup()	
			return render_to_response('classform.html', values)	

		return HttpResponseRedirect(reverse('views.renderClassPage', args = [code, values['class'].id]))



#questionId: 0 - new, other - obvious
def questionForm(request, code, forClass, questionId):
	forClass = int(forClass)

	try: 
		values = decideRender(code, forClass)
		values['questionId'] = int(questionId) #redundancy of having both questionId and question  object in values can be removed if kwargs are used
		if values['questionId']: 
			values['question'] = Question.objects.get(pk = values['questionId'])
			# We want edit to be standalone and yet want class to be selected
			values['class'] = values['question'].forClass.id
	except: return the404()

	if request.method == 'GET': return render_to_response('questionform.html', values)
	
	if request.method == 'POST':
		#TODO: again, validate someplace else	
		if 'question' not in values: values['question'] = Question()
		else: backup(values['question'], 'question')
		try: 
			values['question'].content = request.POST['content']
			values['question'].forClass = Class.objects.get(pk = forClass or int(request.POST['class']))
		 	values['question'].user = User.objects.get(password = hashlib.md5(request.POST['password']).hexdigest())			
			values['question'].save() 
		except Exception, inst: 
			values['message'] = inst 
			values['standalone'] = True
			return render_to_response('questionform.html', values)
		if forClass == 0:
			return HttpResponseRedirect(reverse('views.renderQuestionPage', args = [code, values['question'].id]))
		else:
			return HttpResponseRedirect(reverse('views.renderClassPage', args = [code, forClass])) 


@csrf_exempt#FIXME
def assignmentForm(request, code, forClass, assignmentId ):
	forClass = int(forClass)

	try: 
		values = decideRender(code, forClass)
		values['assignmentId'] = int(assignmentId) #redundancy of having both assignmentId and assignment  object in values can be removed if kwargs are used
		if values['assignmentId']: 
			values['assignment'] = Assignment.objects.get(pk = values['assignmentId'])
			values['class'] = values['assignment'].forClass.id
	except: return the404()

	if request.method == 'GET': return render_to_response('assignmentform.html', values)	

	if request.method == 'POST':
		#TODO: again, validate someplace else	
		if 'assignment' not in values: values['assignment'] = Assignment()
		else: backup(values['assignment'], 'assignment')
		try: 
			values['assignment'].description = request.POST['description']
			values['assignment'].submissionDate = request.POST.get('submission', False) and datetime.datetime(int(request.POST['year']), int(request.POST['month']), int(request.POST['day'])) or None
			values['assignment'].forClass = Class.objects.get(pk = forClass or int(request.POST['class']))
		 	values['assignment'].user = User.objects.get(password = hashlib.md5(request.POST['password']).hexdigest())			
			values['assignment'].save() 
		except: 
			values['message'] = formscrewup() 
			values['standalone'] = True
			return render_to_response('assignmentform.html', values)
		return HttpResponseRedirect(reverse('views.renderAssignmentPage', args = [code, values['assignment'].id]))



#replyFor : 1-Question , 2-Assignment, 3-Resource
def replyForm(request, code, objId, replyFor, replyId):
	values = {}
	values['code'] = code
	values['objId'] = int(objId)
	values['replyFor'] = int(replyFor)
	values['replyId'] = int(replyId) 

	try: 
		if values['replyId']: values['reply'] = Reply.objects.get(pk = values['replyId'])
	except: return the404()

	if request.method == 'GET': return render_to_response('replyform.html', values)

	if request.method == 'POST':
		#FIXME: clumsy code, again.
		if 'reply' not in values: values['reply'] = Reply()
		else: backup(values['reply'], 'reply')
		try:
			values['reply'].content = request.POST['content']

			if values['replyFor'] == 1: 
				obj = Question.objects.get(pk = values['objId']) 
				values['reply'].forQuestion = obj	
				redirect = 'views.renderQuestionPage'
			elif values['replyFor'] == 2:
				obj = Assignment.objects.get(pk = values['objId']) 
				values['reply'].forAssignment = obj	
				redirect = 'views.renderAssignmentPage'
			else: 
				obj = Resource.objects.get(pk = values['objId']) 
				values['reply'].forResource = obj	
				redirect = 'views.renderResourcePage'
			
		 	values['reply'].user = User.objects.get(password = hashlib.md5(request.POST['password']).hexdigest())			
			values['reply'].save()
			if values['replyId'] == 0: 
				obj.replyCount += 1
				obj.save()
			return HttpResponseRedirect(reverse(redirect, args=[values['code'], values['objId']])) 
		except: return the404()


@csrf_exempt#FIXME
def resourceForm(request, code, forClass, resourceId ):
	forClass = int(forClass)

	try: 
		values = decideRender(code, forClass)
		#useless piece of code for now, resources not editable
		values['resourceId'] = int(resourceId) 
		if values['resourceId']: 
			values['resource'] = Resource.objects.get(pk = values['resourceId'])
			values['class'] = values['resource'].forClass.id
	except: return the404()

	if request.method == 'GET': return render_to_response('resourceform.html', values)
	
	if request.method == 'POST':
		try:
			forClassObj = Class.objects.get(pk = forClass or int(request.POST['class']))
			user = User.objects.get(
				password = hashlib.md5(request.POST['password']).hexdigest())	
			if 'file1' in request.FILES:
				for count in range(1, int(request.POST['filecount']) + 1):
					try:
						fileObj = request.FILES['file' + str(count)]
					except KeyError:
						continue
					Resource.objects.create(
						file = fileObj, 
						forClass = forClassObj,
						user = user)
			else:
				for count in range(1, int(request.POST['linkcount']) + 1):
					 try:
						link = request.POST['link' + str(count)]
						if not link:
							raise KeyError
					 except KeyError:
						continue
				       	 Resource.objects.create(
						link = link,
						forClass = forClassObj,
						user = user)
					
		except Exception,inst: 
			values['message'] = inst 
			values['standalone'] = True
			return render_to_response('resourceform.html', values)
		if forClass == 0:
			return HttpResponseRedirect(reverse('views.renderCoursePage', args = [code]))
		else:
			return HttpResponseRedirect(reverse('views.renderClassPage', args = [code, forClass])) 


def passwordForm(request) :
	if request.method == "GET":
		return render_to_response('passwordform.html', {})
	
	if request.method == "POST":
		values = {}
		try: user = User.objects.get(password = hashlib.md5(request.POST['old']).hexdigest())
		except: 
			values['message'] = formscrewup()
			return render_to_response('passwordform.html', values)
		user.password = request.POST['new']
		try:
			match = User.objects.get(password = request.POST['new'])
			import random
			match.password = 'master reset ' + str(random.randint(42, 42000))
			match.save()
			#FIXME: notify and master reset MIGHT collide, change it.
			values['message'] = "Whoa, what coincidence ! Someone else had chosen the same password, please choose another one."
			return render_to_response('passwordform.html', values)

		except: user.save()	
		return HttpResponseRedirect(reverse('views.renderCourses'))	



################# Projects - move to frankie ##################

def renderProjectHome(request):
	values = {}
	values['projects'] = Project.objects.all()
	values['log'] = Log.objects.filter(isPrivate = False).order_by('-datePosted')
	return render_to_response('projecthome.html', values)


def renderProjectPage(request, projectId):
	projectId = int(projectId)
	values = {}
	#for the embedded add tool form
	values['tools'] = Tool.objects.all()
	try:
		values['project'] = Project.objects.get(pk = projectId)
		if projectId == 1729:
			values['members'] = User.objects.filter(pk__in = [89, 116])
		else:
			values['members'] = User.objects.filter(project = projectId)
		values['milestones'] = Milestone.objects.filter(forProject = projectId).order_by('estimate')
		values['log'] = Log.objects.filter(forProject = projectId)
	except Exception, inst: 
		values['message'] = inst
	return render_to_response('project.html', values)


def checkProjectPassword(password, projectId):		
	password = hashlib.md5(password).hexdigest()
	try:
		project = Project.objects.get(pk = projectId)
		if projectId == 1729:
			users = User.objects.filter(pk__in = [89, 116])
		else: 
			users = User.objects.filter(project = project)
		for user in users:
			if user.password == password:
				return True
		if project.guide.password == password:
			return True
	except: pass
	return False
			

def toolForm(request, projectId):
	#projectId is for the redirect and a simpler life
	values = {}
	values['projectId'] = int(projectId)
	if request.method == 'GET':
		return render_to_response("toolform.html", values) 
	elif request.method == 'POST':
		try:
			if not checkProjectPassword(request.POST['password'], values['projectId']):
				 raise 
			toolId = int(request.POST['tool'])
			if toolId > 0:
				tool = Tool.objects.get(pk = toolId)
			else: 
				tool = Tool.objects.create(name = request.POST['name'], description = request.POST['description'])
			Project.objects.get(pk = projectId).tools.add(tool)
		except:
			values['message'] = 'Something is not right. Remember you have to be a project member to mess with it in the first place. If you are indeed a project member, try again.'
			return render_to_response('toolform.html', values)
		return HttpResponseRedirect(reverse('views.renderProjectPage', args = [projectId])) 


def milestoneForm(request, projectId):
	values = {}
	values['projectId'] = int(projectId)
	if request.method == 'GET':
		return render_to_response("milestoneform.html", values) 
	elif request.method == 'POST':
		try:
			if not checkProjectPassword(request.POST['password'], values['projectId']):
				raise
			Milestone.objects.create(description = request.POST['description'], estimate = datetime.datetime(int(request.POST['year']), int(request.POST['month']), int(request.POST['day'])), forProject_id = projectId)

		except:
			values['message'] = 'Something is not right. Remember you have to be a project member to mess with it in the first place. If you are indeed a project member, try again.'		
			return render_to_response('milestoneform.html', values)
		return HttpResponseRedirect(reverse('views.renderProjectPage', args = [projectId])) 

def logForm(request, projectId): 
	values = {}
	values['projectId'] = int(projectId)
	if request.method == 'GET':
		return render_to_response("logform.html", values) 
	elif request.method == 'POST':
		try:
			values['entry'] = Log()
			values['entry'].content = request.POST['content']
		 	values['entry'].user = User.objects.get(password = hashlib.md5(request.POST['password']).hexdigest())			
			values['entry'].forProject_id = projectId
			values['entry'].isPrivate = False
			values['entry'].isMeeting = False
			
			values['entry'].save()
		except Exception, inst:
			values['message'] = inst 
			return render_to_response('logform.html', values)
		return HttpResponseRedirect(reverse('views.renderProjectPage', args = [projectId])) 




