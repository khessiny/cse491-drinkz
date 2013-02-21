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



db._reset_db() #Reset database

db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
        
db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

#Add recipes
r = recipes.Recipe('scotch on the rocks', [('blended scotch','4 oz')])
db.add_recipe(r)
r = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),('vermouth', '1.5 oz')])
db.add_recipe(r)
r = recipes.Recipe('vomit inducing martini', [('orange juice','6 oz'),('vermouth','1.5 oz')])
db.add_recipe(r)
r = recipes.Recipe('whiskey bath', [('blended scotch', '5.5 liter')])
db.add_recipe(r)


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
for mfg, liquor in db.get_liquor_inventory():  #for every item returned 
    if (mfg,liquor) in list:  #check if in posted list  or go on
	continue
    else:
	list.add((mfg,liquor)) #add to posted list 
    	quant = db.get_liquor_amount(mfg,liquor) #get quaniity
    	print >> fp,"<p>%s\t%s\t%s</p>" % (mfg, liquor, quant)

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

print >> fp, "<p>Manufacturer              Liquor</p>"
print >> fp, "<p>------------------|-------------</p>"
for mfg, liquor in db.get_liquor_inventory():
    print >> fp,"<p>%s\t%s</p>" % (mfg, liquor)


print >>fp, """

<p>OTHER PAGES:</p>
<p><a href='index.html'>Back to Index</a></p>
<p><a href='inventory.html'>Inventory</a></p>
<p><a href='liquor_types.html'>Liquor Types</a></p>
"""
fp.close()



