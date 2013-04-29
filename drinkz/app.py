#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import json as simplejson
import convert
import db      #Import database
import recipes #Import recipe class
import os
import jinja2
import sys
loader = jinja2.FileSystemLoader('./templates')
env = jinja2.Environment(loader=loader)
import uuid
from Cookie import SimpleCookie

dispatch = {
    '/' : 'login',
    '/logem' : 'logem',
    '/login' : 'login',
    '/logout' : 'logout',
    '/register' : 'register',
    '/index' : 'index',
    '/error' : 'error',
    '/form' : 'form',
    '/recv' : 'recv',
    '/recipes' : 'recipes',  
    '/inventory' : 'inventory',
    '/liquort' : 'liquort',
    '/rpc'  : 'dispatch_rpc',
    '/add'  : 'addstuff',
    '/addinv' : 'addinv',
    '/addbottletype' : 'addbottletype',
    '/addrecipe' : 'addrecipe',
    '/upvote' : 'upvote'
}
html_headers = [('Content-type', 'text/html')]
usernames = {}
class SimpleApp(object):
    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')

        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)

        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]

        return fn(environ, start_response)

    def index(self, environ, start_response):
		if self.get_name(environ) != False:
			namenow = self.get_name(environ)
			vars = dict(title="Main",name=namenow)
			template = env.get_template("index.html")
			data = template.render(vars)
        		start_response('200 OK', list(html_headers))
        		return [str(data)]
		else:
			headers = list(html_headers)
			headers.append(('Location', '/login'))
			start_response('302 Found', headers)
			return ["Redirect to /login..."]

		
    def login( self, environ, start_response):
		if self.get_name(environ) != False:
			print "WTF"
			namenow = self.get_name(environ)
			vars = dict(name=namenow)
			template = env.get_template("index.html")
			data = template.render(vars)
        		start_response('200 OK', list(html_headers))
        		return [str(data)]
		else:
			template = env.get_template("login.html")
			data = template.render()
        		start_response('200 OK', list(html_headers))
        		return [str(data)]
    def register( self, environ, start_response):
		template = env.get_template("register.html")
		data = template.render()
        	start_response('200 OK', list(html_headers))
        	return [str(data)]
	

    def recipes(self, environ, start_response):
		if self.get_name(environ) != False:
			namenow = self.get_name(environ)
			allrecipes = db.get_all_recipes()
			canmake = ""
			addin=""
			for recipe in allrecipes:
				if(recipe.need_ingredients() == []):
					lacking = "Yes, drink!"
					canmake = canmake + " " + str(recipe.recipename) 
				else:
					lacking = "Needs more:"
					temp = recipe.need_ingredients()
					lacking += str(temp[0]) + " " 

				addin += "<li><div class=\"ui-grid-c\"><div class=\"ui-block-a\" style=\"width:25%\">" + recipe.recipename + "</div><div class=\"ui-block-b\" style=\"width:25%\">" + lacking +"</div>"
				addin += "<div class=\"ui-block-c\" style=\"width:25%\">" + str(db.get_recipe_rating(recipe)) + "</div>"
				addin += "<div class=\"ui-block-d\" style=\"width:25%\">"
				addin += "<button onclick=\"upvote('" 
				addin += recipe.recipename
				addin += "');\">"
				addin += "Like</button></div></div></li>"
				addin += """\
			<script>
			function upvote(recipe_name){
                 	$.ajax({
                        	url: '/rpc',
                        	data: JSON.stringify ({method:'upvote_recipe', params:[recipe_name,], id:"0"} ),
                        	type: "POST",
                        	dataType: "json",
                        	success: function (data) { success(data)},
                        	error: function (err)  { erroring(err) }
                	});
                }
		function success(data){
			alert('Thanks for your vote!');
			location.reload();
			}
		function erroring(err){
			alert("Something went wrong server side, try again.");
			}
		</script>
"""
			vars = dict(title="Recipes",name=namenow, recipess=addin, canmakee = canmake)
			template = env.get_template("recipes.html")
			data = template.render(vars)
			content_type = 'text/html'
			start_response('200 OK', list(html_headers))
			print str(data)
			return [str(data)]
		else:
			headers = list(html_headers)
			headers.append(('Location', '/login'))
			start_response('302 Found', headers)
			return ["Redirect to /login..."]

    def inventory(self, environ, start_response):
		if self.get_name(environ) != False:
			namenow = self.get_name(environ)
			tlist = set()
			addin=""
			for mfg, liquor in db.get_liquor_inventory():  #for every item returned 
					if (mfg,liquor) in tlist:  #check if in posted list  or go on
						continue
					else:
						tlist.add((mfg,liquor)) #add to posted list 
						quant = db.get_liquor_amount(mfg,liquor) #get quaniity
						newquant=str(quant)

					addin += "<li><div class=\"ui-grid-b\"><div class=\"ui-block-a\" style=\"width:50%\">" + mfg + "</div><div class=\"ui-block-b\" style=\"width:25%\">" + liquor + "</div><div class=\"ui-block-c\" style=\"width:25%\">" + newquant + " (ml)</div></div></li>"
			
			vars = dict(title="Inventory",name=namenow,inventory=addin)
			template = env.get_template("inventory.html")
			data = template.render(vars)
			content_type = 'text/html'
			start_response('200 OK', list(html_headers))
			return [str(data)]
		else:
			headers = list(html_headers)
			headers.append(('Location', '/login'))
			start_response('302 Found', headers)
			return ["Redirect to /login..."]

    def liquort(self, environ, start_response):
		if self.get_name(environ) != False:
			namenow = self.get_name(environ)
			addin=""
			for item in db.get_bottle_types():
				addin += "<li><div class=\"ui-grid-b\"><div class=\"ui-block-a\" style=\"width:50%\">" + item[0] + "</div><div class=\"ui-block-b\" style=\"width:25%\">" + item[1] + "</div><div class=\"ui-block-c\" style=\"width:25%\">" + item[2] + "</div></li>"
			
			vars = dict(title="LiquorTypes",name=namenow,liquort=addin)
			template = env.get_template("liquortypes.html")
			data = template.render(vars)
			content_type = 'text/html'
			start_response('200 OK', list(html_headers))
			return [str(data)]
		else:
			headers = list(html_headers)
			headers.append(('Location', '/login'))
			start_response('302 Found', headers)
			return ["Redirect to /login..."]

    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "<p>Couldn't find your stuff.</p>"
       
        start_response('200 OK', list(html_headers))
        return [data]

    def get_name(self,environ):
	name1 = ''
        name1_key = '*empty*'
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'Name' in c:
                key = c.get('Name').value
                if usernames.get(key, ''):
			return usernames.get(key, '')
		else:
			return False
	else:
		return False
    def recv(self, environ, start_response):
        	formdata = environ['QUERY_STRING']
       		results = urlparse.parse_qs(formdata)
		try:
        		amount = results['amount'][0]
		except KeyError:
			amount = "0"
		try:
    	   		amount = convert.convert_to_ml(amount)
			addin = "<p>Converted to ml: %s.</p>" % (amount)
		except AssertionError:
			addin = """\
	<form action='recv'>
		Please enter amount to convert to ml: <input type='text' name='amount' size'20'>
		<input type='submit' value="Convert">
	</form>
		<a href="#popupBasic" data-role="button" data-rel="popup">How to use?</a>
		<div data-role="popup" id="popupBasic">
			<p>Possible inputs: 25ml 30 gallon  4 liter  9oz<p>
		</div>
"""
		vars = dict(convert=addin)
		template = env.get_template("convert.html")
		data = template.render(vars)
		content_type = 'text/html'
        	start_response('200 OK', list(html_headers))
        	return [str(data)]

    def logem(self, environ, start_response):
		content_type = 'text/html'
		formdata = environ['QUERY_STRING']
        	results = urlparse.parse_qs(formdata)
		try:
        		name = results['user'][0].strip()
			passw = results['passw'][0].strip()
		except KeyError:
			name = ""
			passw = ""
        	if db.verify_user(name,passw)!=False:
        		k = str(db.verify_user(name,passw))
			usernames[k] = name
        		headers = list(html_headers)
        		headers.append(('Location', '/index'))
        		headers.append(('Set-Cookie', 'Name=%s' % k))
        		start_response('302 Found', headers)
        		return ["Redirect to /index..."]
		else:
		
        		headers = list(html_headers)
        		headers.append(('Location', '/login'))
        		start_response('302 Found', headers)
        		return ["Redirect to /login..."]

    def logout(self, environ, start_response):
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'Name' in c:
                key = c.get('Name').value
                name1_key = key
		print key

                if key in usernames:
                   del usernames[key]
                   print 'DELETING'

        pair = ('Set-Cookie',
                'Name=deleted; Expires=Thu, 01-Jan-1970 00:00:01 GMT;')
        headers = list(html_headers)
        headers.append(('Location', '/login'))
        headers.append(pair)

        start_response('302 Found', headers)
        return ["Redirect to /login..."]

    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data via a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP.
        
        if environ['REQUEST_METHOD'].endswith('POST'):
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                body = environ['wsgi.input'].read(length)
                response = self._dispatch(body) + '\n'
                start_response('200 OK', [('Content-Type', 'application/json')])
		print str(response)
                return [response]

        # default to a non JSON-RPC error.
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def _decode(self, json):
        return simplejson.loads(json)


    def _dispatch(self, json):
        rpc_request = self._decode(json)

        method = rpc_request['method']
        params = rpc_request['params']
        rpc_fn_name = 'rpc_' + method
        fn = getattr(self, rpc_fn_name)
        result = fn(*params)

        response = { 'result' : result, 'error' : None, 'id' : 1 }
        response = simplejson.dumps(response)
        return str(response)

    def rpc_hello(self):
        return 'world!'
    
    def rpc_upvote_recipe(self, recipeName):
	print recipeName
	db.upvote_recipe(recipeName)

    def upvote(self, environ, start_response):
	formdata = environ['QUERY_STRING']
	results = urlparse.parse_qs(formdata)
	addin = '<p>Thanks for your vote</p>'
	template = env.get_template("add.html")
	vars = dict(form=addin)
	data = template.render(vars)
	
	#recipe = db.get_recipe(name)
        #db.upvote_recipe(recipe)

	content_type = 'text/html'
	start_response('200 OK', list(html_headers))
	return [str(data)]


    def rpc_add(self, a, b):
        return int(a) + int(b)
    def rpc_addrecipe(self,name,ingridients):
	try:
		name = name.strip()
		ing = ingridients.strip()
		templist = ing.split(',')
		sendoff = []
		counter = 0
		while counter< len(templist):
			temp1 = templist[counter].strip()
			temp2 = templist[counter+1].strip()
			finalamount = str(convert.convert_to_ml(temp2))
			finalamount = finalamount + "ml"
			print temp1,finalamount
			sendoff.append((temp1,finalamount))
			counter = counter + 2
		r = recipes.Recipe(name, sendoff)
		try:
			db.add_recipe(r)
			addin= "Succesfully Added."

		except db.DuplicateRecipeName:
			addin= "There is already a recipe by this name."
	
	except (AssertionError, KeyError, IndexError) :
		addin = "Incorrect format or incomplete. Please try again."

	return addin

    def rpc_addinventory(self,mfg,liquor,amount):
	try:
		mfg = mfg.strip()
		liquor = liquor.strip()
		amount = amount.strip()
	    	print mfg,liquor,amount
		try:
			db.add_to_inventory(mfg,liquor,amount)
	 		addin = "Succesfully added."
		except db.LiquorMissing:
			addin= " You must first add this bottle type " +mfg + " " + liquor + " ."
	except (AssertionError, KeyError, IndexError) :
		addin = """\
		 Incorrect amount format or incomplete. Please try again.
	"""
        return addin

    def rpc_addtype(self,mfg,liquor,type):
	try:
		type = type.strip()
		mfg = mfg.strip()
		liquor = liquor.strip()
		if not db._check_bottle_type_exists(mfg, liquor):
			db.add_bottle_type(mfg,liquor,type)
	 		addin = "Succesfully added."
		else:
			addin= " This bottle type already exists."
	except (AssertionError, KeyError, IndexError) :
		addin = """\
		 Incorrect format or incomplete. Please try again.
	"""
	return addin

    def rpc_convert_units_to_ml(self,amount):
	return str(convert.convert_to_ml(amount))+" ml" 	

    def rpc_get_recipe_names(self):
        return db.get_all_recipenames()

    def rpc_get_liquor_inventory(self):
	list = []
	for mfg, liquor in db.get_liquor_inventory():
		list.append((mfg,liquor))
	return list

    def rpc_register(self,user,passw,passtwo,email):
	if passw==passtwo:
		print user,passw,passtwo,email
		return db.add_user(user,passw,email)
		

	
    def form(self, environ, start_response):
	dataa = """\
		Please enter amount to convert to ml: <input type='text' class="a" name='amount' size='20'>
		Result: <input type='text' class='result' id='resulting' size='20'/>
		
		<a href="#popupBasic" data-role="button" data-rel="popup">How to use?</a>
		<div data-role="popup" id="popupBasic">
			<p>Possible inputs: 25ml 30 gallon  4 liter  9oz</p>
		</div>	
		<p class='toupdate' />
		<script type="text/javascript">	
		function show_textbox(err)
		{
			$('#popupBasic').popup('open');
		}
		function update_result(input,output){
		text = 'Converted '+ input + ' to ml =  ' + output ;
   		$('input.result').val(text);
		}
		function do_convert() {
		 a = $('input.a').val();
		 $.ajax({
    			url: '/rpc', 
     			data: JSON.stringify ({method:'convert_units_to_ml', params:[a,], id:"0"} ),
     			type: "POST",
     			dataType: "json",
     			success: function (data) { update_result(a, data.result) },
     			error: function (err)  { show_textbox(err)}
  		});
		}
		
		$('input.a').change(do_convert);
		$('#resulting').addClass('ui-disabled');
		</script>

"""
	if self.get_name(environ) != False:
			namenow = self.get_name(environ)
			vars = dict(title="Convert",name=namenow,convert=dataa)
			template = env.get_template("convert.html")
			data = template.render(vars)
			content_type = 'text/html'
        		start_response('200 OK', list(html_headers))
        		return [str(data)]
	else:
			headers = list(html_headers)
			headers.append(('Location', '/login'))
			start_response('302 Found', headers)
			return ["Redirect to /login..."]


    def addinv(self, environ, start_response):
	formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
	try:
        	mfg = results['mfg'][0]
		liquor = results['liquor'][0]
		amount = results['amount'][0]
		mfg = mfg.strip()
		liquor = liquor.strip()
		amount = amount.strip()
	    	print mfg,liquor,amount
		try:
			db.add_to_inventory(mfg,liquor,amount)
	 		addin = "<p>Succesfully added.</p>"
		except db.LiquorMissing:
			addin= "<p> You must first add this bottle type " +mfg + " " + liquor + " .</p>"
	except (AssertionError, KeyError, IndexError) :
		addin = """\
		<p> Incorrect amount format or incomplete. Please try again.</p>
	"""
	vars = dict(form=addin)
	template = env.get_template("add.html")
	data = template.render(vars)
	content_type = 'text/html'
        start_response('200 OK', list(html_headers))
        return [str(data)]




    def addbottletype(self, environ, start_response):
    	formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
	try:
        	mfg = results['mfg'][0]
		liquor = results['liquor'][0]
		type = results['type'][0]
		type = type.strip()
		mfg = mfg.strip()
		liquor = liquor.strip()
		if not db._check_bottle_type_exists(mfg, liquor):
			db.add_bottle_type(mfg,liquor,type)
	 		addin = "<p>Succesfully added.</p>"
		else:
			addin= "<p> This bottle type already exists.</p>"
	except (AssertionError, KeyError, IndexError) :
		addin = """\
		<p> Incorrect format or incomplete. Please try again.</p>
	"""
	vars = dict(form=addin)
	template = env.get_template("add.html")
	data = template.render(vars)
	content_type = 'text/html'
        start_response('200 OK', list(html_headers))
        return [str(data)]

    def addrecipe(self, environ, start_response):
    	formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
	try:
        	name = results['name'][0]
		ing = results['ing'][0]
		name = name.strip()
		ing = ing.strip()
		templist = ing.split(',')
		sendoff = []
		counter = 0
		while counter< len(templist):
			temp1 = templist[counter].strip()
			temp2 = templist[counter+1].strip()
			finalamount = str(convert.convert_to_ml(temp2))
			finalamount = finalamount + "ml"
			print temp1,finalamount
			sendoff.append((temp1,finalamount))
			counter = counter + 2
		r = recipes.Recipe(name, sendoff)
		try:
			db.add_recipe(r)
			addin= "<p>Succesfully Added.</p>"

		except db.DuplicateRecipeName:
			addin= "<p>There is already a recipe by this name.</p>"
	
	except (AssertionError, KeyError, IndexError) :
		addin = """\
		<p> Incorrect format or incomplete. Please try again.</p>
	"""
	vars = dict(form=addin)
	template = env.get_template("add.html")
	data = template.render(vars)
	content_type = 'text/html'
        start_response('200 OK', list(html_headers))
        return [str(data)]

def load_db(file_name):
	    db.load_db(file_name)
