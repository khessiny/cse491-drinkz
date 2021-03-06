import app
import urllib
from wsgiref.simple_server import make_server
import urlparse
import json as simplejson
import db      #Import database
import recipes #Import recipe class
import os
import sys
import StringIO
from drinkz import convert


def test_rpc_addrecipe_1():
	db._reset_db()
	text = call_remote(jsonrpc='1.0', method='addrecipe', params = ["gotdrunk", "Black Label,1234 ml, tommy, 5 gallon"], id='1')
	rpc_request = simplejson.loads(text)
	#print rpc_request
        result = rpc_request['result']
	print result
	assert "gotdrunk" in db.get_all_recipenames()
	testing = "Succesfully Added."
	assert result == testing

def test_rpc_addrecipe_2():
	#should fail, incorrect formatting
	db._reset_db()
	text = call_remote(jsonrpc='1.0', method='addrecipe', params = ["gotdrunk", "Black Label,1234 ml, tommy, 5 gallon,"], id='1')
	rpc_request = simplejson.loads(text)
	#print rpc_request
        result = rpc_request['result']
	print result
	assert "gotdrunk" not in db.get_all_recipenames()
	testing = "Incorrect format or incomplete. Please try again."
	assert result == testing


def test_rpc_addinventory_1():
	text = call_remote(jsonrpc='1.0', method='addinventory', params = ["Greyer", "goose", "25 gallon"], id='1')
	db._reset_db()
	rpc_request = simplejson.loads(text)
	#print rpc_request
        result = rpc_request['result']
	print result
	assert "You must first add this bottle" in result

def test_rpc_addinventory_2():
	db._reset_db()
	db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
	text = call_remote(jsonrpc='1.0', method='addinventory', params = ["Johnnie Walker", "black label", "25 gallon"], id='1')
	
	

	rpc_request = simplejson.loads(text)
	#print rpc_request
        result = rpc_request['result']
	print result
	check = db.check_inventory("Johnnie Walker", "black label")
	assert "Succesfully added." in result
	assert check 

def test_rpc_addtype_1():
	db._reset_db()
	text = call_remote(jsonrpc='1.0', method='addtype', params = ["Johnnie Walker", "black label", "scotch"], id='1')
	
	rpc_request = simplejson.loads(text)
        result = rpc_request['result']
	print result
	check = db._check_bottle_type_exists("Johnnie Walker", "black label")
	assert "Succesfully added." in result
	assert check 

def test_rpc_addtype_2():
	db._reset_db()
	db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
	text = call_remote(jsonrpc='1.0', method='addtype', params = ["Johnnie Walker", "black label", "blended scotch"], id='1')
	
	rpc_request = simplejson.loads(text)
        result = rpc_request['result']
	print result
	assert "This bottle type already exists." in result

def test_rpc_convert():
	
	text = call_remote(jsonrpc='1.0', method='convert_units_to_ml', params = ["25gallon"], id='1')
	rpc_request = simplejson.loads(text)
	#print rpc_request
        result = rpc_request['result']
	print result
	resultt = convert.convert_to_ml("25gallon")
	resultt = str(resultt) + " ml"
	assert result == resultt


def test_getnames():
	db._reset_db() #Reset database

	r = recipes.Recipe('scotch on the rocks', [('blended scotch','4 oz')])
	db.add_recipe(r)
	r = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),('vermouth', '1.5 oz')])
	db.add_recipe(r)
	r = recipes.Recipe('vomit inducing martini', [('orange juice','6 oz'),('vermouth','1.5 oz')])
	db.add_recipe(r)
	r = recipes.Recipe('whiskey bath', [('blended scotch', '5.5 liter')])
	db.add_recipe(r)
	
	
	text = call_remote(jsonrpc='1.0', method='get_recipe_names', params = [], id='1')
	rpc_request = simplejson.loads(text)
	#print rpc_request
        result = rpc_request['result']
	print result
	assert ('scotch on the rocks') in result
    	assert ('vodka martini') in result
    	assert ('vomit inducing martini') in result
    	assert ('whiskey bath') in result


def test_getinventory():
	db._reset_db() #Reset database
	db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
	db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

	db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
	db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
        
	db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
	db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

	db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
	db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

	
	
	text = call_remote(jsonrpc='1.0', method='get_liquor_inventory', params = [], id='1')
	rpc_request = simplejson.loads(text)
	print rpc_request
        result = rpc_request['result']
	assert result[0][0] == 'Johnnie Walker'
	assert result[0][1] == 'black label'
	assert result[2][1] == 'moonshine'
	assert result[3][0] == 'Gray Goose'
	assert result[1][1] == 'extra dry vermouth'





def call_remote( jsonrpc,method, params, id):
	app_obj = app.SimpleApp()
	d = dict(jsonrpc=jsonrpc,method=method, params=params, id=id)
    	encoded = simplejson.dumps(d)
	
	output = StringIO.StringIO(encoded)
	length = len(encoded)
	
#	test=output.getvalue()
#	print test

    	environ = {}
	environ['PATH_INFO'] = '/rpc'
	environ['REQUEST_METHOD'] = 'POST'
	environ['CONTENT_LENGTH'] = length
	environ['wsgi.input'] = output
    	d = {}

    	def my_start_response(s, h, return_in=d):
        	d['status'] = s
        	d['headers'] = h

	
    	results = app_obj(environ, my_start_response)

    	text = "".join(results)
    	status, headers = d['status'], d['headers']
    	assert ('Content-Type', 'application/json') in headers
    	assert status == '200 OK'
	return text
