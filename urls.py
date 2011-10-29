from django.conf.urls.defaults import patterns, include, url
from projectzaphod import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
		url(r'^projectlog/$', 'views.useless'),
		url(r'^$', 'views.renderCourses'),
		url(r'^(\w+)/class/(\d+)/$', 'views.renderClassPage'),
		url(r'^(\w+)/question/(\d+)/$', 'views.renderQuestionPage'),
		url(r'^(\w+)/resource/(\d+)/$', 'views.renderResourcePage'),
		url(r'^(\w+)/assignment/(\d+)/$', 'views.renderAssignmentPage'),

		url(r'^courseform/(\d+)/$', 'views.courseForm'),
		url(r'^(\w+)/classform/(\d+)/$', 'views.classForm'),
		url(r'^(\w+)/(\d+)/questionform/(\d+)/$', 'views.questionForm'),
		url(r'^(\w+)/(\d+)/assignmentform/(\d+)/$', 'views.assignmentForm'),
		url(r'^(\w+)/(\d+)/resourceform/(\d+)/$', 'views.resourceForm'),
		url(r'^(\w+)/(\d+)/replyform/(\d+)/(\d+)/$', 'views.replyForm'),
		
		url(r'^changepassword/$', 'views.passwordForm'),
		url(r'^checkpassword/$', 'views.checkPassword'),

		url(r'^getpreview/$', 'views.getPreview'),


		url(r'^projects/(\d+)/$','views.renderProjectPage'),	
		url(r'^projects/$','views.renderProjectHome'),	
		url(r'^projects/(\d+)/toolform/$','views.toolForm'),
		url(r'^projects/(\d+)/milestoneform/$','views.milestoneForm'),
		url(r'^projects/(\d+)/logform/$','views.logForm'),

		url(r'^(\w+)','views.renderCoursePage')
		
		#(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/favicon.ico'}),
    # Examples:
    # url(r'^$', 'projectzaphod.views.home', name='home'),
    # url(r'^projectzaphod/', include('projectzaphod.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
