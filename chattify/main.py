#!/usr/bin/env python
import os
import md5
from django.utils import simplejson
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.api import channel

# path to the template files
TEMPLATES = os.path.join(os.path.dirname(__file__), 'templates')

class SayHandler(webapp.RequestHandler):
	def post(self):
		data = {
			'username': self.request.get("username"),
			'text': self.request.get("msg")
		}
		key = self.request.get("key")
		channel.send_message(key, simplejson.dumps(data))

class CreateHandler(webapp.RequestHandler):
	def get_key(self):
		m = md5.new()
		m.update(self.request.get("title"))
		return m.hexdigest()

	def get(self):
		self.redirect("/chat/" + self.get_key() + '/' + self.request.get("username"))

	def post(self):
		self.response.out.write("{'key':"+ self.get_key() +"}");

class ChatHandler(webapp.RequestHandler):
	def get(self, key, username):
		token = channel.create_channel(key)
		path = os.path.join(TEMPLATES, 'chat.html')
		self.response.out.write(template.render(path, {
			'key': key,
			'token': token,
			'username': username
		}))


class MainHandler(webapp.RequestHandler):
	def get(self):
		path = os.path.join(TEMPLATES, 'index.html')
		self.response.out.write(template.render(path, {}))

def main():
	application = webapp.WSGIApplication([
		('/', MainHandler),
		('/create', CreateHandler),
		('/say', SayHandler),
		(r'/chat/(.*)/(.*)', ChatHandler)
	], debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()