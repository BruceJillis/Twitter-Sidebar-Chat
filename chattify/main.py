#!/usr/bin/env python
import os
import md5
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

# path to the template files
TEMPLATES = os.path.join(os.path.dirname(__file__), 'templates')

class CreateHandler(webapp.RequestHandler):
	def get_key(self):
		m = md5.new()
		m.update(self.request.get("title"))
		return m.hexdigest()

	def get(self):
		key = self.get_key();
		self.redirect("/chat/" + key)

	def post(self):
		key = self.get_key();
		self.response.out.write("{'key': ' + key + '}");

class ChatHandler(webapp.RequestHandler):
	def get(self, key):
		path = os.path.join(TEMPLATES, 'chat.html')
		self.response.out.write(template.render(path, {
			'key': key
		}))


class MainHandler(webapp.RequestHandler):
	def get(self):
		path = os.path.join(TEMPLATES, 'index.html')
		self.response.out.write(template.render(path, {}))

def main():
	application = webapp.WSGIApplication([
		('/', MainHandler),
		('/create', CreateHandler),
		(r'/chat/(.*)', ChatHandler)
	], debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()