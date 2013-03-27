"""
Yevgeny Khessin
A39652176
HOMEWORK 3
CSE491
Database functionality for drinkz information.

"""

def convert_to_ml(amount):
    if("ml") in amount: #dont change anything 
        amount = amount.strip('ml') #strips characters
        amount = amount.strip() #strip whitespace
        final = float(amount)
    elif("oz") in amount:
        amount = amount.strip('oz') #strips characters
        amount = amount.strip()#strip whitespace
        final = (float(amount)*29.5735)
    elif("gallon") in amount:
        amount = amount.strip('gallon') #strips characters
        amount = amount.strip() #strip whitespace
        final = (float(amount)*3785.41)
    elif("liter") in amount:
        amount = amount.strip('liter') #strips characters
        amount = amount.strip() #strip whitespace
        final = (float(amount)*1000)
    else:
        assert 0, amount

    return final