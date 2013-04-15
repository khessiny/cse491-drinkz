"""
Yevgeny Khessin
A39652176
HOMEWORK 2 
CSE491
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db                        # import from local package
from . import recipes
from . import convert


#new function just for reading in files
def filereader(fp):
	readline = csv.reader(fp)
	for line in readline:  #for every line in the file
		try:
			if not line[0].strip():  #remove all 
				continue	#continue on 
			if line[0].startswith('#'):  #check if its a comment
				continue #continue on to next line
		except IndexError: #failure to read, dont fail
			print "Something wasnt formatted correctly."
			continue
		#now we just have the lines we wan
		try:
			(maker,name,value) = line  #get them separate
		except ValueError:
			print "Not enough arguments, please use maker,name,amount"
			continue
		yield maker,name,value #return the mfg, name and quanitity



def r_filereader(fp):
	readline = csv.reader(fp)
	for line in readline:  #for every line in the file
		try:
			if not line[0].strip():  #remove all 
				continue	#continue on 
			if line[0].startswith('#'):  #check if its a comment
				continue #continue on to next line
		except IndexError: #failure to read, dont fail
			print "Something wasnt formatted correctly."
			continue
		#now we just have the lines we wan
		yield line #return the mfg, name and quanitity



def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    typloader = filereader(fp)#initialize our file loader

    n = 0 #set count to 0
    while True: #forever loop 
	for maker,name,value in typloader:  #get values out of generator
		n=n+1 #increase count 
		db.add_bottle_type(maker,name,value) #add it to the database
	try:  #try to go to next line
		typloader.next()  #go to next line  
	except StopIteration: #catche error
		print "The next line was incorrectly formatted."
		return n #return final value
	
    return n #return the final value

		 

def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    invloader = filereader(fp)#initialize our file loader

    n = 0 #set count to 0
    while True: #forever loop 
	for maker,name,value in invloader:  #get values out of generator
		n=n+1 #increase count 
		db.add_to_inventory(maker,name,value) #add it to the database
	try:  #catch formatting errors
		invloader.next()  #go to next line 
	except StopIteration: #caught error
		print "The next line was incorrectly formatted."
		return n #return the value 
    return n #return the final value

def load_recipes(fp):
	"""
    Loads in data of the form recipe name, liquor type,amount, liquor type, amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
	invloader=r_filereader(fp)
	n=0
	while True: #forever loop 
		for templist in invloader:  #get values out of generator
			try:
				name = templist[0]
				sendoff = []
				counter = 1
				while counter< len(templist):
					temp1 = templist[counter].strip()
					temp2 = templist[counter+1].strip()
					finalamount = str(convert.convert_to_ml(temp2))
					finalamount = finalamount + "ml"
					#print temp1,finalamount
					sendoff.append((temp1,finalamount))
					counter = counter + 2
				r = recipes.Recipe(name, sendoff)
				try:
					db.add_recipe(r)
				except db.DuplicateRecipeName:
					print "There is already a recipe by this name."
				n=n+1 #increase count
				#print db.get_all_recipes()
			except (IndexError, AssertionError):
				print "The line was incorrectly formatted."
		try:  #catch formatting errors
			invloader.next()  #go to next line 
		except StopIteration: #caught error
			print "The next line was incorrectly formatted."
			return n #return the value 
    	return n #return the final value