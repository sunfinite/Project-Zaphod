from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template 

class Zaphod(webapp.RequestHandler):
	def get(self):
		self.response.out.write(template.render('templates/main.html',{}))

class Web(webapp.RequestHandler):
	def get(self):	
		self.response.out.write(template.render('templates/web.html',{}))

application = webapp.WSGIApplication(
				 [('/', Zaphod),
				  ('/web',Web)],
			         debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()				    

