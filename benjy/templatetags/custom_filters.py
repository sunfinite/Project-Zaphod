from django import template
import datetime

register = template.Library()	

@register.filter
def firstObjDate(value):
	return value[0].date

@register.filter
def days(value):
	return range(1, 32)

@register.filter
def months(value):
	return range(1, 13)

@register.filter
def years(value):
	return range(2011, 2013)

@register.filter
def typeVal(value):
	types = ['Theory', 'Lab', 'Test', 'Other']
	return types[int(value) - 1]

@register.filter
def limit(value):
	if len(value) > 100:
		return value[:100] + '...'
	else: return value

@register.filter
def fileName(value):
	return value.name.split('/')[1]

@register.filter
def fileLink(value):
	return '/static/' + value.name

@register.filter
def manyToManyIterator(value):
	return value.all()
	
@register.filter
def currentTask(milestones):
	#milestones have an order_by on them
	for milestone in milestones:
		if milestone.estimate > datetime.datetime.now():
			return milestone.description
			
@register.filter
def decideProjectId(projectId):
	if(int(projectId) == 1729):
		return 'ZZ9'
	else: 
		return projectId
	
		
