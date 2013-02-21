from . import db
class Recipe():
    def __init__(self,recipename,ingridients):
        # The constructor for Recipe should take a name (a string) and a list of ingredient 2-tuples, (liquor type, amount).
        if(recipename):
            self.recipename = recipename
        if(ingridients):
            self.singridients= ingridients #empty dictionary

    def need_ingredients(self):
	 volume = 0 
         missing = []
	 for type, quantity in self.singridients:
      		needed = db.convert_to_ml(quantity)
	 	available = db.check_inventory_for_type(type)
        	for (m,l) in available:
			vol = db.get_liquor_amount(m,l)
			if vol > volume:
				volume = vol
		if volume < needed:
			missing.append((type,needed - volume))
			volume = 0
		else:
			continue


         return missing
