from . import db
class Recipe():
    def __init__(self,recipename,ingridients):
        # The constructor for Recipe should take a name (a string) and a list of ingredient 2-tuples, (liquor type, amount).
        if(name):
            self.recipename = recipename
        if(components):
            self.ingrd = ingridients #copy the list of tuples
            self.ingredients= {} #empty dictionary
            for ingridient in self.ingrid:
                self.ingridients[tup[0]] = tup[1] #add key liquor name and set it equal to the amount.

    def need_ingredients(self):
        """ This methode takes in the recipe and returns how many
        components are needed to complete the recipe.  It returns
        the components in the form of a list of 2-tuples"""
        needed = []
        
        for t, amount in self.comp:
            in_inventory = db.check_inventory_for_type(t)
            required = db.convert_to_ml(amount)

            if in_inventory < required:
                print required
                print in_inventory
                needed.append((t,required - in_inventory))
            else:
                continue

        return needed

    def __eq__(self,a):
        if self.name == a.name and self.comp == a.comp:
            return 1
        else:
            return 0