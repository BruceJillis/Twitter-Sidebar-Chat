#!/usr/bin/env python
import os
import random
from django.utils import simplejson
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.api import channel
from google.appengine.ext import db

import counter

# path to the template files
TEMPLATES = os.path.join(os.path.dirname(__file__), 'templates')

# localhost / live switch
local = os.environ['HTTP_HOST'].startswith('localhost')

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
		if key in channels:
			if username in channels[key]:
				channels[key].remove(username)
			if len(channels[key]) == 0:
				del channels[key]
			else:
				message(key, username, " has left");

class SayHandler(webapp.RequestHandler):
	def post(self):
		key = self.request.get("key")
		username = self.request.get("username")
		msg = self.request.get("msg")
		message(key, username, msg)

class ChatHandler(webapp.RequestHandler):
	def get(self, key, username):
		token = channel.create_channel(key + username)
		path = os.path.join(TEMPLATES, 'chat.html')
		if local:
			host = 'http://localhost:8085/'
		else:
			host = 'http://chattify.appspot.com/'
		counter.increment('users')
		users = counter.get_count('users') + 1
		self.response.out.write(template.render(path, {
			'key': key,
			'token': token,
			'username': username,
			'host': host,
			'users': users
		}))

class NewNameHandler(webapp.RequestHandler):
	def get(self, title):
		counter.increment('users')
		users = counter.get_count('users')
		if title == '':
			self.redirect("/");
		else:
			self.redirect("/chat/"+title+"/guest"+str(users));
		
class MainHandler(webapp.RequestHandler):
	def get(self):
		path = os.path.join(TEMPLATES, 'index.html')
		if local:
			host = 'http://localhost:8085/'
		else:
			host = 'http://chattify.appspot.com/'
		users = counter.get_count('users') + 1
		self.response.out.write(template.render(path, {
			'host': host,
			'users': users,
			'active': channels
		}))

def main():
	application = webapp.WSGIApplication([
		('/', MainHandler),
		('/join', JoinHandler),
		('/leave', LeaveHandler),
		('/say', SayHandler),
		(r'/chat/(.*)/(.*)', ChatHandler),
		(r'/chat/(.*)/?', NewNameHandler)
	], debug=local)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()