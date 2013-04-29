"""
Yevgeny Khessin
A39652176
HOMEWORK 3
CSE491
Database functionality for drinkz information.


I chose to use a dictionary to store the class recipe by the recipe name. This preserves the structure
of the class and makes it easy to get the item and edit the item.

"""
import convert
import os 
import sys
import sqlite3, os
import recipes
from cPickle import dump, load
import uuid

# private singleton variables at module level
_bottle_types_db = set([])
_inventory_db = dict()
_recipe_db=dict()
_auth=set([])

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipe_db, _auth
    _bottle_types_db =set([])
    _inventory_db = dict()
    _recipe_db= dict()
    _auth=set([])

def save_db(filename):
	try:
		os.unlink(filename)
	except OSError:
		pass
	db = sqlite3.connect(filename)
	with db:
		cur = db.cursor()
		cur.execute("CREATE TABLE BottleTypes(mfg STRING, liquor STRING, typ STRING)")
		cur.execute("CREATE TABLE Auth(user STRING, pass STRING, email STRING)")
		cur.execute("CREATE TABLE Inventory(mfg STRING, liquor STRING, amount FLOAT)")
		cur.execute("CREATE TABLE Recipes(name STRING, ing BUFFER)")
		for (m, l) in _inventory_db:
			mfg = m
			liquor = l
			amount = _inventory_db[(mfg, liquor)]
			cur.execute("insert into Inventory values (?, ?, ?)", (mfg, liquor,amount))
		for (m, l, typ) in _bottle_types_db:
			cur.execute("insert into BottleTypes values (?, ?, ?)", (m,l,typ))
		for (u, p, e) in _auth:
			cur.execute("insert into Auth values (?, ?, ?)", (u,p,e))
		allrecipes = get_all_recipes()
		for recipe in allrecipes:
			name = recipe.recipename
			templist = recipe.singridients
			finallist = buffer(myListToStr(templist))
			cur.execute("insert into Recipes values (?,?)",(name,finallist))
		
		db.commit()
		cur.close()
		#db.close()
#from stackoverflow
def myListToStr(myList):
    """This method takes a list of (int, str) tuples and converts them to a string"""

    strList = ""
    for item in myList:
        name, amount = item #split the tuple

        strList += "{}:{};".format(name, amount) #append the tuple in "num:name" format with a " " delimiter
    return strList[:-1] #remove the final space (unneeded)

def strToMyList(myStr):
    """This method takes a string in the format "int:str int:str int:str..."
    and converts it to a list of (str, str) tuples"""

    myList = []
    for tup in myStr.split(";"): #for each converted tuple
        name, amount = tup.split(":") #split the tuple

        myList.append((name, amount))

    return myList



def load_db(filename):
	db = sqlite3.connect(filename)
	with db:
		cur = db.cursor()
		cur.execute("SELECT * FROM BottleTypes")
		rows = cur.fetchall()
		for row in rows:
			mfg,liquor,typ = row
			_bottle_types_db.add((mfg, liquor, typ))
		cur.execute("SELECT * FROM Auth")
		rows = cur.fetchall()
		for row in rows:
			mfg,liquor,typ = row
			_auth.add((mfg, liquor, typ))

		cur.execute("Select * FROM Inventory")
		rows = cur.fetchall()
		for row in rows:
			mfg,liquor,amount = row
			#print mfg
			#print liquor
			#print amount
			_inventory_db[(mfg, liquor)]=amount
		cur.execute("Select * FROM Recipes")
		rows = cur.fetchall()
		#print rows
		for row in rows:
			name,ing = row
			#print name
			#print str(ing)
			my_list2 = strToMyList(str(ing))
			r = recipes.Recipe(name,my_list2)
			add_recipe(r)
		#for k,v in _recipe_db.items():
    			# k,v.singridients
		db.commit()
		cur.close()


# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass

class UserExists(Exception):
    pass

def get_bottle_types():
    return list(_bottle_types_db)
	

def add_bottle_type(mfg, liquor, typ):
    #"Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def add_user(user,passw,email):
    if check_user(user):
	err = "This username already exists, please use another one'%s'" % (user)
	raise UserExists(err)
    else:
	_auth.add((user,passw,email))
	return user
    

def verify_user(user,passw):
   for (u, p, _) in _auth:
        if user == u and passw == p:
	     k = str(uuid.uuid4())
             return k

   return False

def check_user(user):
    for (u, _, _) in _auth:
        if user == u:
            return True

    return False

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    # just add it to the inventory database as a tuple, for now.
    if check_inventory(mfg,liquor): #try to gsee if it is in the inventory 
    	current = _inventory_db[(mfg, liquor)] #get current amount if it is 
    else:
    	current = 0 #if it isnt, adding to inventory, current amount is 0 
    	pass
    add = convert.convert_to_ml(amount) #new amount to add #convert new amount 
    finalamount = add+current #new total 
    _inventory_db[(mfg, liquor)]=finalamount #put the final value back in

def check_inventory(mfg, liquor):
    for (m, l) in _inventory_db:
        if mfg == m and liquor == l:
            return True
        
    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    amounts = []
    liquorvolume = 0
    for (m, l) in _inventory_db:
        if mfg == m and liquor == l:
	     liquorvolume = _inventory_db[(mfg, liquor)]
	#amounts.append( temp )
    #go through the list of amounts and calcualte the volume in ml
	#for liquor in amounts:
	#try: 
	#liquorvolume = convert_to_ml(liquor)
	#except IndexError:
	#print "Incorrectly Formatted Amount"
    return liquorvolume   #return amount




def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (m, l) in _inventory_db:
        yield m, l 



class DuplicateRecipeName(Exception):
    pass



def add_recipe(recipe):
    #add this recipe to dictionary, the name is the key and the ingridients are value
   if recipe.recipename in _recipe_db:  # if the value is in the keys, raise duplicate exception
	raise DuplicateRecipeName()
   else:
      _recipe_db[recipe.recipename] = recipe   #store the whole recipe object


def get_recipe(name):
    #retrieve the recipe
   if name in _recipe_db: #if the recipe exists
	return _recipe_db[name]  

def get_all_recipes():
    return _recipe_db.values() #returns all the values as a list


def check_inventory_for_type(types):
    listtypes=[]
    for (m, l, t) in _bottle_types_db:
         if types == t:
         	listtypes.append((m,l))
    return listtypes

def get_all_recipenames():
	return _recipe_db.keys()
