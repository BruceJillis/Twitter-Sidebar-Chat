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

# channels/participants list
channels = {}

# send a msg to all people on a channel
def message(key, username, msg):
	if not key in channels:
		return
	data = {
		'username': username,
		'msg': msg
	}
	for name in channels[key]:
		data['test'] = key + name
		channel.send_message(key + name, simplejson.dumps(data))

class JoinHandler(webapp.RequestHandler):
	def post(self):
		key = self.request.get("key")
		username = self.request.get("username")
		if not key in channels:
			channels[key] = []
		channels[key].append(username)
		message(key, username, " has joined");

class LeaveHandler(webapp.RequestHandler):
	def post(self):
		key = self.request.get("key")
		username = self.request.get("username")
		channels[key].remove(username)
		message(key, username, " has left");

class SayHandler(webapp.RequestHandler):
	def post(self):
		key = self.request.get("key")
		username = self.request.get("username")
		msg = self.request.get("msg")
		message(key, username, msg)


class CreateHandler(webapp.RequestHandler):
	def get_key(self):
		m = md5.new()
		m.update(self.request.get("channel"))
		return m.hexdigest()

	def get(self):
		self.redirect("/chat/" + self.get_key() + '/' + self.request.get("username"))

	def post(self):
		self.response.out.write("{'key':"+ self.get_key() +"}");

class ChatHandler(webapp.RequestHandler):
	def get(self, key, username):
		token = channel.create_channel(key + username)
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
		('/join', JoinHandler),
		('/leave', LeaveHandler),
		('/say', SayHandler),
		(r'/chat/(.*)/(.*)', ChatHandler)
	], debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()