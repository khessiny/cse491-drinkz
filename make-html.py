#! /usr/bin/env python
from drinkz import db      #Import database
from drinkz import recipes #Import recipe class
import os

#Reference: github.com/ctb/cse491-linkz
try:
    os.mkdir('html')
except OSError:
    # already exists
    pass



#db._reset_db() #Reset database

#db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
#db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

#db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
#db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
        
#db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
#db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

#db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
#db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

#Add recipes
#r = recipes.Recipe('scotch on the rocks', [('blended scotch','4 oz')])
#db.add_recipe(r)
#r = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),('vermouth', '1.5 oz')])
#db.add_recipe(r)
#r = recipes.Recipe('vomit inducing martini', [('orange juice','6 oz'),('vermouth','1.5 oz')])
#db.add_recipe(r)
#r = recipes.Recipe('whiskey bath', [('blended scotch', '5.5 liter')])
#db.add_recipe(r)
filename = "database"
db.load_db(filename)


#PAGE MAIN 

fp = open('html/index.html', 'w')
print >>fp, "<b>CSE491-DRINKZ <p><a href='recipes.html'>Recipes</a>"
print >>fp, """
<p><a href='inventory.html'>Inventory</a></p>
<p><a href='liquor_types.html'>Liquor Types</a></p>
"""
fp.close()







#PAGE RECIPIES
fp = open('html/recipes.html', 'w')

print >>fp, "<b>Recipes</b><p></p>"
allrecipes = db.get_all_recipes()
sendtopage = "<ol>"
for recipe in allrecipes:
	if(recipe.need_ingredients() == []):
		lacking = "Yes, needs more!"
	else:
		lacking = "No, drink now!"
	sendtopage += "<li>" + recipe.recipename + "Have all the Ingridients? " + lacking + "</li>\n"

sendtopage = sendtopage + "</ol>"
print >> fp, sendtopage

print >>fp, """

OTHER PAGES:
<p><a href='index.html'>Back to Index</a></p>
<p><a href='inventory.html'>Inventory</a></p>
<p><a href='liquor_types.html'>Liquor Types</a></p>
"""
fp.close()







#PAGE INV
fp = open('html/inventory.html', 'w')

print >>fp, "<b>Inventory</b><p></p>"

list = set()

print >> fp, "<p>Manufacturer             Liquor          Amount(ml)</p>"
print >> fp, "-------------------|-------------------|------------------"
sendtopage = "<ol>"
for mfg, liquor in db.get_liquor_inventory():  #for every item returned 
    if (mfg,liquor) in list:  #check if in posted list  or go on
	continue
    else:
	list.add((mfg,liquor)) #add to posted list 
    	quant = db.get_liquor_amount(mfg,liquor) #get quaniity
	newquant=str(quant)
    	sendtopage +="<li>" + mfg + " " + liquor + " " + newquant +"<li>\n"
sendtopage = sendtopage + "</ol>"
print >>fp, sendtopage
print >>fp, """
OTHER PAGES:
<p><a href='index.html'>Back to Index</a></p>
<p><a href='inventory.html'>Inventory</a></p>
<p><a href='liquor_types.html'>Liquor Types</a></p>
"""
fp.close()







#PAGE LIQUOR TYPES

fp = open('html/liquor_types.html', 'w')

print >>fp, "<b>Liquor Types</b><p></p>"
sendtopage = "<ol>"
print >> fp, "<p>Manufacturer              Liquor</p>"
print >> fp, "<p>------------------|-------------</p>"
for mfg, liquor in db.get_liquor_inventory():
    sendtopage +="<li>" + mfg + " " + liquor + "<li>\n"


print >>fp, sendtopage
print >>fp, """
<p>OTHER PAGES:</p>
<p><a href='index.html'>Back to Index</a></p>
<p><a href='inventory.html'>Inventory</a></p>
<p><a href='liquor_types.html'>Liquor Types</a></p>
"""
fp.close()



