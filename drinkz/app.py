#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import json as simplejson
import convert
import db      #Import database
import recipes #Import recipe class
import os

dispatch = {
    '/' : 'index',
    '/content' : 'somefile',
    '/error' : 'error',
    '/helmet' : 'helmet',
    '/form' : 'form',
    '/recv' : 'recv',
    '/recipes' : 'recipes',  
    '/inventory' : 'inventory',
    '/liquort' : 'liquort',
    '/rpc'  : 'dispatch_rpc'
}

html_headers = [('Content-type', 'text/html')]

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
	data = """\
<html> 
    <head> 
    <title>CSE491Drinkz - Main</title> 
    <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="http://code.jquery.com/mobile/1.3.0/jquery.mobile-1.3.0.min.css" />
        <script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
        <script src="http://code.jquery.com/mobile/1.3.0/jquery.mobile-1.3.0.min.js"> </script>
	 <script>
		function javatest()
		{
			alert("I'm a drinkers dream site!");
		}
	</script>
	<style>
	.ui-header .ui-title {color:red;}
	</style>
</head> 
<body> 
    <!-- Start page -->
    <div data-role="page" id="index" >

        <div data-role="header" data-id="header" data-position="fixed">
            <h1>CSE491Drinkz - Main</h1>
            <div data-role="navbar">
                <ul>
                    <li><a href="/" data-icon="home" data-iconpos="top" >Index</a></li>
                    <li><a href="/recipes" data-icon="arrow-l" data-iconpos="top"  >Recipes</a></li>
			<li><a href="/inventory" data-icon="arrow-r" data-iconpos="top" >Inventory</a></li>
                    <li><a href="/liquort" data-icon="arrow-u" data-iconpos="top"  >Liquor Types</a></li>
                    <li><a href="/form" data-icon="gear" data-iconpos="top" >Convert</a></li>
                </ul>            </div><!-- /navbar -->
        </div><!-- /header -->

        <div data-role="content">
		<div align="center">
		<img src="http://www2.chemistry.msu.edu/courses/cem352/SS2013_Jackson/MichiganState.jpg" >
		</div>
		<input type="button" onclick="javatest()" value="What is this site for?">
              </div><!-- /content -->
	<div data-role="footer" data-id="footer" data-position="fixed"><h1>CSE491-Drinkz</div>
    </div><!-- /page -->

</body>
</html>
"""
        start_response('200 OK', list(html_headers))
        return [data]
        
    def somefile(self, environ, start_response):
        content_type = 'text/html'
        data = open('somefile.html').read()

        start_response('200 OK', list(html_headers))
        return [data]

    def recipes(self, environ, start_response):
	addin = """\
<ul id="mylist" data-role="listview"  data-inset="false" >
<li><div class="ui-grid-a">
<div class="ui-block-a" style="width:50%">Recipe Names</div>
<div class="ui-block-b" style="width:50%">Are all ingridients available?</div></div></li>
"""
	allrecipes = db.get_all_recipes()
	for recipe in allrecipes:
		if(recipe.need_ingredients() == []):
			lacking = "Yes, drink!"
		else:
			lacking = "Needs more:"
			temp = recipe.need_ingredients()
			lacking += str(temp[0]) + " " 

		addin += "<li><div class=\"ui-grid-a\"><div class=\"ui-block-a\" style=\"width:50%\">" + recipe.recipename + "</div><div class=\"ui-block-b\" style=\"width:50%\">" + lacking + "</div></div></li>"
	

	addin+="</ul>"

	
        content_type = 'text/html'
        data = """\
<html> 
    <head> 
    <title>CSE491Drinkz - Recipes</title> 
    <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="http://code.jquery.com/mobile/1.3.0/jquery.mobile-1.3.0.min.css" />
        <script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
        <script src="http://code.jquery.com/mobile/1.3.0/jquery.mobile-1.3.0.min.js"> </script>
</head> 
<body> 
    <!-- Start page -->
    <div data-role="page" id="convert" >

        <div data-role="header" data-id="header" data-position="fixed">
            <h1>CSE491Drinkz - Recipes</h1>
            <div data-role="navbar">
                <ul>
                    <li><a href="/" data-icon="home" data-iconpos="top" >Index</a></li>
                    <li><a href="/recipes" data-icon="arrow-l" data-iconpos="top"  >Recipes</a></li>
			<li><a href="/inventory" data-icon="arrow-r" data-iconpos="top" >Inventory</a></li>
                    <li><a href="/liquort" data-icon="arrow-u" data-iconpos="top"  >Liquor Types</a></li>
                    <li><a href="/form" data-icon="gear" data-iconpos="top" >Convert</a></li>
                </ul>            </div><!-- /navbar -->
        </div><!-- /header -->

        <div data-role="content">
"""
        data += addin
	data +="""\
</div><!-- /content -->
	<div data-role="footer" data-id="footer" data-position="fixed"><h1>CSE491-Drinkz</div>
    </div><!-- /page -->

</body>
</html>
"""


        start_response('200 OK', list(html_headers))
        return [data]


    def inventory(self, environ, start_response):
        addin = """\
<ul id="mylist" data-role="listview"  data-inset="false" >
<li><div class="ui-grid-b">
<div class="ui-block-a" style="width:50%">Manufacturer</div>
<div class="ui-block-b" style="width:25%">Liquor</div>
<div class="ui-block-c" style="width:25%">Liquor</div></div></li>
"""	
	tlist = set()
	for mfg, liquor in db.get_liquor_inventory():  #for every item returned 
    		if (mfg,liquor) in tlist:  #check if in posted list  or go on
			continue
    		else:
			tlist.add((mfg,liquor)) #add to posted list 
    			quant = db.get_liquor_amount(mfg,liquor) #get quaniity
			newquant=str(quant)

		addin += "<li><div class=\"ui-grid-b\"><div class=\"ui-block-a\" style=\"width:50%\">" + mfg + "</div><div class=\"ui-block-b\" style=\"width:25%\">" + liquor + "</div><div class=\"ui-block-c\" style=\"width:25%\">" + newquant + " (ml)</div></div></li>"
	

	addin+="</ul>"

        content_type = 'text/html'
        data = """\
<html> 
    <head> 
    <title>CSE491Drinkz - Inventory</title> 
    <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="http://code.jquery.com/mobile/1.3.0/jquery.mobile-1.3.0.min.css" />
        <script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
        <script src="http://code.jquery.com/mobile/1.3.0/jquery.mobile-1.3.0.min.js"> </script>
</head> 
<body> 
    <!-- Start page -->
    <div data-role="page" id="convert" >

        <div data-role="header" data-id="header" data-position="fixed">
            <h1>CSE491Drinkz - Inventory</h1>
            <div data-role="navbar">
                <ul>
                    <li><a href="/" data-icon="home" data-iconpos="top" >Index</a></li>
                    <li><a href="/recipes" data-icon="arrow-l" data-iconpos="top"  >Recipes</a></li>
			<li><a href="/inventory" data-icon="arrow-r" data-iconpos="top" >Inventory</a></li>
                    <li><a href="/liquort" data-icon="arrow-u" data-iconpos="top"  >Liquor Types</a></li>
                    <li><a href="/form" data-icon="gear" data-iconpos="top" >Convert</a></li>
                </ul>            </div><!-- /navbar -->
        </div><!-- /header -->

        <div data-role="content">
"""
	data += addin
	data +="""\
</div><!-- /content -->
	<div data-role="footer" data-id="footer" data-position="fixed"><h1>CSE491-Drinkz</div>
    </div><!-- /page -->

</body>
</html>
"""


        start_response('200 OK', list(html_headers))
        return [data]

    def liquort(self, environ, start_response):
        addin = """\
<ul id="mylist" data-role="listview"  data-inset="false" >
<li><div class="ui-grid-a">
<div class="ui-block-a" style="width:50%">Manufacturer</div>
<div class="ui-block-b" style="width:50%">Liquor</div></div></li>
"""
	for mfg, liquor in db.get_liquor_inventory():
		addin += "<li><div class=\"ui-grid-a\"><div class=\"ui-block-a\" style=\"width:50%\">" + mfg + "</div><div class=\"ui-block-b\" style=\"width:50%\">" + liquor + "</div></div></li>"
	

	addin+="</ul>"

        content_type = 'text/html'
        data = """\
<html> 
    <head> 
    <title>CSE491Drinkz - Liquor Types</title> 
    <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="http://code.jquery.com/mobile/1.3.0/jquery.mobile-1.3.0.min.css" />
        <script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
        <script src="http://code.jquery.com/mobile/1.3.0/jquery.mobile-1.3.0.min.js"> </script>
</head> 
<body> 
    <!-- Start page -->
    <div data-role="page" id="convert" >

        <div data-role="header" data-id="header" data-position="fixed">
            <h1>CSE491Drinkz - Liquor Types</h1>
            <div data-role="navbar">
                <ul>
                    <li><a href="/" data-icon="home" data-iconpos="top" >Index</a></li>
                    <li><a href="/recipes" data-icon="arrow-l" data-iconpos="top"  >Recipes</a></li>
			<li><a href="/inventory" data-icon="arrow-r" data-iconpos="top" >Inventory</a></li>
                    <li><a href="/liquort" data-icon="arrow-u" data-iconpos="top"  >Liquor Types</a></li>
                    <li><a href="/form" data-icon="gear" data-iconpos="top" >Convert</a></li>
                </ul>            </div><!-- /navbar -->
        </div><!-- /header -->

        <div data-role="content">
"""
	data += addin
	data +="""\
</div><!-- /content -->
	<div data-role="footer" data-id="footer" data-position="fixed"><h1>CSE491-Drinkz</div>
    </div><!-- /page -->

</body>
</html>
"""

        start_response('200 OK', list(html_headers))
        return [data]


    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def helmet(self, environ, start_response):
        content_type = 'image/gif'
        data = open('Spartan-helmet-Black-150-pxls.gif', 'rb').read()

        start_response('200 OK', [('Content-type', content_type)])
        return [data]

    def form(self, environ, start_response):
        data = form()

        start_response('200 OK', list(html_headers))
        return [data]
   
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
	

	
	
        content_type = 'text/html'
	data = """\
<html> 
    <head> 
    <title>CSE491Drinkz - Results</title> 
    <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="http://code.jquery.com/mobile/1.3.0/jquery.mobile-1.3.0.min.css" />
        <script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
        <script src="http://code.jquery.com/mobile/1.3.0/jquery.mobile-1.3.0.min.js"> </script>
</head> 
<body> 
    <!-- Start page -->
    <div data-role="page" id="convert" >

        <div data-role="header" data-id="header" data-position="fixed">
            <h1>CSE491Drinkz - Results</h1>
            <div data-role="navbar">
                <ul>
                    <li><a href="/" data-icon="home" data-iconpos="top" >Index</a></li>
                    <li><a href="/recipes" data-icon="arrow-l" data-iconpos="top"  >Recipes</a></li>
			<li><a href="/inventory" data-icon="arrow-r" data-iconpos="top" >Inventory</a></li>
                    <li><a href="/liquort" data-icon="arrow-u" data-iconpos="top"  >Liquor Types</a></li>
                    <li><a href="/form" data-icon="gear" data-iconpos="top" >Convert</a></li>
                </ul>            </div><!-- /navbar -->
        </div><!-- /header -->

        <div data-role="content">
"""
	data += addin
	data +="""\
</div><!-- /content -->
	<div data-role="footer" data-id="footer" data-position="fixed"><h1>CSE491-Drinkz</div>
    </div><!-- /page -->

</body>
</html>
"""



        start_response('200 OK', list(html_headers))
        return [data]

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

    def rpc_add(self, a, b):
        return int(a) + int(b)
    
    def rpc_convert_units_to_ml(self,amount):
	return convert.convert_to_ml(amount) 	

    def rpc_get_recipe_names(self):
        return db.get_all_recipenames()

    def rpc_get_liquor_inventory(self):
	list = []
	for mfg, liquor in db.get_liquor_inventory():
		list.append((mfg,liquor))
	return list
def form():
	return """\
<html> 
    <head> 
    <title>CSE491Drinkz - Convert</title> 
    <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="http://code.jquery.com/mobile/1.3.0/jquery.mobile-1.3.0.min.css" />
        <script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
        <script src="http://code.jquery.com/mobile/1.3.0/jquery.mobile-1.3.0.min.js"> </script>
</head> 
<body> 
    <!-- Start page -->
    <div data-role="page" id="form" >

        <div data-role="header" data-id="header" data-position="fixed">
            <h1>CSE491Drinkz - Convert</h1>
            <div data-role="navbar">
                <ul>
                    <li><a href="/" data-icon="home" data-iconpos="top" >Index</a></li>
                    <li><a href="/recipes" data-icon="arrow-l" data-iconpos="top"  >Recipes</a></li>
			<li><a href="/inventory" data-icon="arrow-r" data-iconpos="top" >Inventory</a></li>
                    <li><a href="/liquort" data-icon="arrow-u" data-iconpos="top"  >Liquor Types</a></li>
                    <li><a href="/form" data-icon="gear" data-iconpos="top" >Convert</a></li>
                </ul>
            </div><!-- /navbar -->
        </div><!-- /header -->

        <div data-role="content">
	<form action='recv'>
		Please enter amount to convert to ml: <input type='text' name='amount' size'20'>
		<input type='submit' value="Convert">
	</form>
		<a href="#popupBasic" data-role="button" data-rel="popup">How to use?</a>
		<div data-role="popup" id="popupBasic">
			<p>Possible inputs: 25ml 30 gallon  4 liter  9oz<p>
		</div>
              </div><!-- /content -->
		
	<div data-role="footer" data-id="footer" data-position="fixed"><h1>CSE491-Drinkz</div>
    </div><!-- /page -->
	<div data-role="page" id="form" >
		<p> Please enter like this:</p>
	</div>


</body>
</html>
"""

