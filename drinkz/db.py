"""
Yevgeny Khessin
A39652176
HOMEWORK 2 
CSE491
Database functionality for drinkz information.
"""

# private singleton variables at module level
_bottle_types_db = set([])
_inventory_db = {}
_recipe_db={}

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db
    _bottle_types_db =set([])
    _inventory_db = {}
    _recipe_db= {}

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

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
    try:
    	current = _inventory_db[(mfg, liquor)] #get curent amount
    except KeyError:
    	current = 0
    	pass
    add = convert_to_ml(amount) #new amount to add
    finalamount = add+current
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


def convert_to_ml(amount):
    if("ml") in amount:
        amount = amount.strip('ml')
        amount = amount.strip()
        result = float(amount)
    elif("oz") in amount:
        amount = amount.strip('oz')
        amount = amount.strip()
        result = (float(amount)*29.5735)#1 oz=29.57ml
    elif("gallon") in amount:
        amount = amount.strip('gallon')
        amount = amount.strip()
        result = (float(amount)*3785.41)
    elif("liter") in amount:
        amount = amount.strip('liter')
        amount = amount.strip()
        result = (float(amount)*1000)
    else:
        assert 0, amount

    return result 


    return 0


add_recipe(r):
    #add this recipe to dictionary, the name is the key and the ingridients are value
   if(r.name in _recipe_db.keys()):
      print "This recipe already exists"
   else:
      _recipe_db[r.name] = r.ingridients
 

get_recipe(name):
    #retrieve the recipe
   if(name in _recipe_db.keys()):
      return _recipe_db[name]
   else:
      print "There is no recipe by this name."
      return 0
   

get_all_recipes():
    return _recipe_db
