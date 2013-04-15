import _mypath
import sys
from drinkz import app
from drinkz.app import SimpleApp
import random
import socket
import time




app.load_db("database") #loading a database file

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = random.randint(8000, 9999)
sock.bind((socket.gethostname(), port))
sock.listen(5)#accept 5 connections
print "Accepting connections on port %d..." % port
print "Connect to http://%s:%d/" % \
	  (socket.getfqdn(), port)  
while 1:
        print "Accepting..."
        (clientsocket, address) = sock.accept()
        print str(address)
        
        request = clientsocket.recv(1024)#recieve 1024 bytes
       
        print "******************"
        print request
        print "******************"
        splitrequest = request.split('\r\n')#split into lines
	#print splitrequest
        getting = splitrequest[0].split(' ')
        if len(splitrequest) < 2:
            clientsocket.send("First line is not long enough")
            continue
	if getting[0]!= "GET":
	     print "not get"
	     continue
        if getting[2]!= "HTTP/1.1":
	     print "not http1.1"
	     clientsocket.send("I only get stuff.")
	     continue
        location = getting[1]
	if location == "":
            location = "/"
        environ = {}
	if "?" in location:
	     form = getting[1].split("?")
             formget = form[1]
             environ['QUERY_STRING'] = form[1]
	     location = form[0]
            
        
        
        environ['PATH_INFO'] = location  #set path 
        environ['REQUEST_METHOD'] = (getting[2]) #set request to be http 1.1
        
        d = {}
        def my_start_response(s, h, return_in=d):
            d['status'] = s
            d['headers'] = h
        app_obj = app.SimpleApp()    
        html = app_obj(environ, my_start_response)
	 #print html


        response = "HTTP/1.1 "+ d['status'] +" \n" + (d['headers'][0][0]+": "+d['headers'][0][1]+" \n") + "".join(html)
	 #print response
        clientsocket.send(response)
        clientsocket.close()
