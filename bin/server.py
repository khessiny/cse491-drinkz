import _mypath
import sys
from drinkz import app
from drinkz.app import SimpleApp
import random
import socket
import json
import sys
import StringIO
import time
from drinkz.app import SimpleApp

the_app = SimpleApp()

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = random.randint(8000, 9999)
s.bind((host, port))        # Bind to the port

print 'Starting server on', host, port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr

   buffer = c.recv(1024)

   while "\r\n\r\n" not in buffer:
      data = c.recv(1024)
      if not data:
         break
      buffer += data
      print (buffer,)
      time.sleep(1)

   print 'got entire request:', (buffer,)

   # now, parse the HTTP request.
   lines = buffer.splitlines()
   request_line = lines[0]
   request_type, path, protocol = request_line.split()
   print 'GOT', request_type, path, protocol
   if request_type == "GET":
   
	   request_headers = lines[1:]                  # irrelevant, discard for GET.
	   query_string = ""
	   if '?' in path:
		  path, query_string = path.split('?', 1)

	   # build environ & start_response
	   environ = {}
	   environ['PATH_INFO'] = path
	   environ['QUERY_STRING'] = query_string

	   d = {}
	   def start_response(status, headers):
		  d['status'] = status
		  d['headers'] = headers

	   results = the_app(environ, start_response)
	   # note -- start_response is called by the_app.

	   response_headers = []
	   for k, v in d['headers']:
		  h = "%s: %s" % (k, v)
		  response_headers.append(h)
		  
	   response = "\r\n".join(response_headers) + "\r\n\r\n" + "".join(results)

	   c.send("HTTP/1.0 %s\r\n" % d['status'])
	   c.send(response)
	   c.close()
	
   if request_type == "POST":
	
	   environ = {}
	   request_json = lines[-1:][0]
	   output = StringIO.StringIO(request_json)
	   length = len(request_json)# get post
	   environ['PATH_INFO'] = path
	   environ['REQUEST_METHOD'] = request_type 
	   environ['CONTENT_LENGTH'] = length
	   environ['wsgi.input'] = output
	   def start_response(status, headers):
		  d['status'] = status
		  d['headers'] = headers
	   try:
	   	results = the_app(environ, start_response)
	   except AssertionError:
		pass
		
		
	   # note -- start_response is called by the_app.

	   response_headers = []
	   for k, v in d['headers']:
		  h = "%s: %s" % (k, v)
		  response_headers.append(h)
		  
	   response = "\r\n".join(response_headers) + "\r\n\r\n" + "".join(results)

	   c.send("HTTP/1.0 %s\r\n" % d['status'])
	   c.send(response)
	   c.close()