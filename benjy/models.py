from django.db import models
import hashlib


#TODO: Though not relevant, on_delete will do no harm

class Course(models.Model):
	code = models.CharField(max_length = 5, unique = True)
	title = models.CharField(max_length = 145)
	teacher = models.CharField(max_length = 145)
	
class User(models.Model):
	usn = models.CharField(max_length = 11, null = True)
	name = models.CharField(max_length = 100)
	email = models.EmailField(null = True, blank = True)
	password = models.CharField(max_length = 100, unique = True)
	project = models.ForeignKey('Project', null = True)
	isTeacher = models.BooleanField()

	def save(self):
		self.password = hashlib.md5(self.password).hexdigest()
		super(User, self).save()


class ClassAbstract(models.Model):
	type = models.IntegerField(default = 0)
	summary = models.TextField(blank = True, null = True)
	date = models.DateTimeField(null = True)
	forCourse = models.ForeignKey(Course)
	user = models.ForeignKey(User)
	datePosted = models.DateTimeField(auto_now_add = True)
	dateEdited = models.DateTimeField(blank = True, null = True)

	class Meta: 
		abstract = True
	
class Class(ClassAbstract): pass

class ClassEdits(ClassAbstract):
	forClass = models.ForeignKey(Class)



class PostAbstract(models.Model):
	datePosted = models.DateTimeField(auto_now_add = True)
	#stupid: dateEdited has to be manual because of replyCount(one good thing is nullable?)
	dateEdited = models.DateTimeField(blank = True, null = True)
	replyCount = models.IntegerField(default = 0)
	forClass = models.ForeignKey(Class)
	user = models.ForeignKey(User)

	class Meta:
		abstract = True



###################### Questions ####################

class QuestionAbstract(PostAbstract):
	content = models.TextField()
	
	class Meta:
		abstract = True

class Question(QuestionAbstract): pass
	
class QuestionEdits(QuestionAbstract):
	forQuestion = models.ForeignKey(Question)

####################### Assignments #####################

class AssignmentAbstract(PostAbstract):
	description = models.TextField()
	submissionDate = models.DateTimeField(null = True)

	class Meta:
		abstract = True


class Assignment(AssignmentAbstract): pass

class AssignmentEdits(AssignmentAbstract): 
	forAssignment = models.ForeignKey(Assignment)

##################### Resources ######################

class ResourceAbstract(PostAbstract):
	link = models.CharField(max_length = 420, null = True, blank = True)
	file = models.FileField(upload_to = 'uploads/', null = True, blank = True) 

	class Meta:
		abstract = True
	
class Resource(ResourceAbstract): pass

class ResourceEdits(ResourceAbstract): 
	forResource = models.ForeignKey(Resource)

######################## Replies ###########################
class ReplyAbstract(models.Model):
	content = models.TextField()
	datePosted = models.DateTimeField(auto_now_add = True)
	dateEdited = models.DateTimeField(blank = True, null = True)
	forQuestion = models.ForeignKey(Question, default = 0)
	forAssignment = models.ForeignKey(Assignment, default = 0)
	forResource = models.ForeignKey(Resource, default = 0)
	user = models.ForeignKey(User)

	class Meta:
		abstract = True

class Reply(ReplyAbstract): pass

class ReplyEdits(ReplyAbstract): 
	forReply = models.ForeignKey(Reply)



################ Projects - move to frankie ###########################
class Tool(models.Model):
	name = models.TextField()
	description = models.TextField()


class Project(models.Model):
	title = models.TextField()
	guide = models.ForeignKey(User, related_name = "guideFor")
	abstract = models.TextField(blank = True, null = True)
	tools = models.ManyToManyField(Tool, null = True, blank = True)
	similar = models.ManyToManyField('self', symmetrical = True, null = True, blank = True)


class Milestone(models.Model):
	description = models.TextField()
	estimate = models.DateTimeField()
	forProject = models.ForeignKey(Project)

class Log(models.Model):
	content = models.TextField()
	datePosted = models.DateTimeField(auto_now_add = True)
	dateEdited = models.DateTimeField(blank = True, null = True)
	user = models.ForeignKey(User)
	forProject = models.ForeignKey(Project)
	isPrivate = models.BooleanField()
	isMeeting = models.BooleanField()
	replyTo = models.ForeignKey('self', default = 0)



