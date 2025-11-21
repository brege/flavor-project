import re

class isCulinaryGroup:
    
    def __init__(self, name, genre, species):
        self.name = name
        self.genre = genre
        self.species = species

    def orient(name, genre, species):

        # SUFFIX -- remove source, but append after
        # Input:
        #   'vinegar: balsamic, red wine, rice, sherry'
        # Output:
        #   'balsamic vinegar, red wine vinegar, rice vinegar, sherry vinegar'
        # in the dictionary.
        suffix = ['cheese', 'oil', 'oils', 'pepper', 'wine', 
                  'sugar', 'salads', 'squash', 'stocks', 'mushrooms',
                  'salt', 'ham', 'seeds', 'bell peppers', 'ginger',
                  'beans', 'eggs', 'chocolate', 'crust', 'vinegar',
                  'cherries', 'rum', 'liqueurs', 'tea', 'vinaigrette',
                  'fruits', 'fat', 'stock', 'potatoes', 'zest',
                  'vermouth', 'meats', 'liqueur', 'cabbage', 'cheeses',
                  'lettuce', 'sausages', 'sausage', 'peppercorns']

        # PREFIX -- remove source
        # Input:
        #   sauces: béarnaise, beurre blanc, brown butter hollandaise
        # Output:
        #   [béarnaise, beurre blanc, brown butter hollandaise]
        prefix_remove = ['sauce', 'sauces', 'spices', 'berries', 'melon', 
                         'baked goods', 'poultry', 'herbs', 'orange liqueurs', 'cured meats',
                         'seafood']

        # PREFIX PLUS -- include source, and append before
        # Input:
        #   'lime: juice, leaves'
        # Output:
        #   '[lime, lime juice, lime leaves]'
        prefix_before = ['lime', 'orange', 'lemon', 'yuzu', 'sesame', 
                         'chili peppers', 'curry', 'roe', 'grapefruit',
                         'chile peppers', 'coconut', 'game', 'innards', 'nuts',
                         'mangoes', 'raspberries', 'butter', 'paprika',
                         'celery', 'greens', 'beef', 'chicken', 'lamb',
                         'pork', 'veal', 'shellfish', 'mint', 'raisins',
                         'olives', 'bread', 'dill', 'turkey', 'fennel',
                         'pumpkin', 'carrot']

        # PREFIX MINUS -- include source, and append after
        # Input:
        #   'pears: dried, fresh'
        # Output:
        #   '[pears, dried pears, fresh pears]'
        prefix_after = ['pears', 'cranberries', 'peas', 'shrimp', 'fruit',   
                        'basil', 'fish', 'sesame seeds', 'chiles', 'rice',
                        'honey', 'ice cream', 'soups', 'asparagus', 'parsley', 
                        'corn syrup', 'cream', 'port', 'miso', 'onions']

        # case-by-case:
        # Input:
        #   'mustard: Dijon, seeds'
        # Ouput:
        #   ['dijon mustard', 'mustard seeds'] 
        # Use a dict of lists:
        #   {'ingredient: original layout':['ingredient', 'any', 'possible layout']}
        case_by_case = {
            'apples: cider, fruit':
                ['apples', 'apple cider'],
            'apples: cider, juice':
                ['apples', 'apple cider', 'apple juice'],
            'apples: cider, fruit, juice':
                ['apples', 'apple cider', 'apple juice'],
            'APPLES: cider, fruit, juice':
                ['apples', 'apple cider', 'apple juice'],
            'apples: fruit, juice':
                ['apples', 'apple juice'],
            'APPLES: Golden Delicious, Rome, tart':
                ['apples', 'Golden Delicious apples', 'Rome apples', 'tart apples'],
            'APPLES: CIDER, FRUIT, JUICE':
                ['apples', 'apple cider', 'apple juice'],
            'APPLES: cider, fruit, sauce':
                ['apples', 'apple cider', 'apple sauce'],
            '*APPLES: fruit, juice':
                ['apples', 'apple juice'],
            'apple: cider, fruit, juice':
                ['apples', 'apple cider', 'apple juice'],
            'apricots: dried, jam, puree':
                ['apricots', 'dried apricot', 'apricot jam',' apricot puree'],
            'bananas: fruit, liqueur':
                ['bananas', 'banana liqueur'],
            'BASIL: regular, cinnamon':
                ['basil', 'cinnamon basil'],
            'Beefeater: pear': # alcohol brands, and probably kinds,
                ['pear'],      # are going to need further refinement
            'beets: vegetable, juice':
                ['beets', 'beet juice'],
            'bonito: dried, flakes':
                ['bonito', 'dried bonito', 'bonito flakes'],
            'bread crumbs: regular, panko':
                ['bread crumbs', 'panko bread crumbs'],
            'bread, esp. fruit':
                ['bread', 'fruit bread'],
            'bread, fruit':
                ['bread', 'fruit bread'],
            'cheese and cheese dishes: feta, mozzarella, Parmesan':
                ['cheese', 'cheese dishes', 'feta cheese', 
                 'mozzarella cheese', 'Parmesan cheese'],
            'cocktails: mint julep (ingredient), Pimms No. 1 Cup (ingredient)':
                ['cocktails', 'juleps'],
            'currants, black or red: fruit, preserves':
                ['currants', 'black currants', 'red currants', 'currants preserves'],
            'currants, red: fruit, jelly':
                ['currants', 'red currants', 'currant jelly'],
            'figs: dried, fresh':
                ['figs', 'dried figs'],
            'figs: fresh, dried':
                ['figs', 'dried figs'],
            'fish, esp. white: halibut, skate':
                ['fish', 'white fish', 'halibut', 'skate fish'],
            'GARLIC: regular, spring':
                ['GARLIC', 'spring garlic'],
            'Hendrick’s: cucumber, rose petals': #ibid
                ['cucumber', 'rose petals'],
            'lettuces: red oak leaf, red leaf':
                ['lettuce', 'red oak leaf lettuce', 'red leaf lettuce'],
            'mushrooms: cultivated, shiitakes': 
                ['cultivated mushrooms', 'shiitake mushrooms'],
            'mustard: dry, seeds':
                ['mustard', 'dry mustard', 'mustard seeds'],
            'MUSTARD: Dijon, dry':
                ['Dijon mustard', 'dry mustard'],
            'MUSTARD: Dijon, whole grain':
                ['Dijon mustard', 'whole grain mustard'],
            'mustard: Dijon, dry':
                ['Dijon mustard', 'dry mustard'],
            'mustard: Dijon, dry, grainy':
                ['Dijon mustard', 'dry mustard', 'grainy mustard'],
            'mustard: Dijon, seeds':
                ['Dijon mustard', 'mustard seeds'],
            'mustard: Dijon, dry, whole grain':
                ['Dijon mustard', 'dry mustard', 'whole grain mustard'],
            'mustard: Dijon, yellow':
                ['Dijon mustard', 'yellow mustard'],
            'mustard: Dijon, Meaux':
                ['Dijon mustard', 'Meaux mustard'],
            'mustard: Dijon, dry, yellow':
                ['mustard', 'Dijon mustard', 'dry mustard', 'yellow mustard'],
            'mustard: oil, seeds':
                ['mustard', 'mustard oil', 'mustard seeds'],
            'mustard: powder, seeds':
                ['mustard powder', 'mustard seeds'],
            'mustard: country, Dijon, dry (sauce)':
                ['country mustard', 'Dijon mustard', 'dry mustard'],
            'mustard: Dijon, Chinese (ingredient and complement)':
                ['Dijon mustard', 'Chinese mustard'],
            'noodles: angel hair, vermicelli, rice':
                ['angel hair pasta', 'vermicelli noodles', 'rice noodles'],
            'Old Raj: saffron':
                ['saffron'],
            'olives: black, niçoise':
                ['black olive', 'olive niçoise'],
            'oranges: fruit, marmalade':
                ['oranges', 'orange marmalade'],
            'plums: fruit, sauce':
                ['plums', 'plum sauce'],
            'soy sauce: regular, white':
                ['soy sauce', 'white soy sauce'],
            'spirits, white: gin, vodka':
                ['white spirits', 'gin', 'vodka'],
            'stocks and broths: fish, seafood':
                ['fish stock', 'fish broth', 'seafood stock', 'seafood broth'],
            'STOCKS AND BROTHS: chicken, clam, fish, shellfish, veal':
                ['chicken broth', 'chicken stock' 'clam stock', 
                 'fish stock', 'shellfish stock', 'veal stock'],
            'stocks / broths: beef, chicken, vegetable':
                ['beef stock', 'chicken stock', 'vegetable stock',
                 'beef broth', 'chicken broth', 'vegetable broth'],
            'strawberries: fruit, puree':
                ['strawberries', 'strawberry puree'],
            'tomatoes: paste, puree, raw':
                ['tomatoes', 'tomato paste', 'tomato puree'],
            'TOMATOES: cherry, grape, juice, roasted':
                ['TOMATOES', 'cherry tomatoes', 'grape tomatoes', 
                 'tomato juice', 'roasted tomatoes'],
            'TOMATOES: canned, paste, plum, sauce':
                ['TOMATOES', 'canned tomatoes', 
                 'tomato paste', 'plum tomatoes', 'tomato sauce'],
            'TOMATOES: fresh, sun-dried':
                ['TOMATOES', 'sun-dried tomatoes'],
            'TOMATOES: juice, paste, pulp':
                ['TOMATOES', 'tomato juice', 'tomato paste', 'tomato pulp'],
            'tomatoes: flesh, juice':
                ['tomatoes', 'tomato juice'],
            'tomatoes: regular, sun-dried':
                ['tomatoes', 'sun-dried tomatoes'],
            'tomatoes: canned, fresh, paste':
                ['tomatoes', 'canned tomatoes', 'tomato paste'],
            'TOMATOES: canned, fresh, paste':
                ['TOMATOES', 'canned tomatoes', 'tomato paste'],
            'tomatoes: paste, sauce':
                ['tomato paste', 'tomato sauce'],
            'truffles: black, juice':
                ['truffles', 'black truffles', 'truffle juice'],
            'truffles: black, white':
                ['truffles', 'black truffles', 'white truffles'],
            'truffles: oil, shaved, white':
                ['truffles', 'shaved truffels', 'white truffels'],
            'vegetables: fresh, fermented':
                ['vegetables', 'fermented vegetables'],
            'walnuts: nuts, oil':
                ['walnuts', 'walnut oil'],
            'Zuidam Dry: orange peel': #ibid
                ['orange peel'],
            }
        # at this point you wonder if its even worth it to have a dict

        genre_ = genre.lower().strip("*")
        digest = []
        if name in case_by_case:
            digest = case_by_case[name]
        elif genre_ in suffix:
            [ digest.append(k+' '+genre_) for k in species] #.split(',') ]
        elif genre_ in prefix_remove: 
            [ digest.append(genre_) ]
            [ digest.append(k) for k in species] #.split(',') ]
        elif genre_ in prefix_after: 
            [ digest.append(k+' '+genre_) for k in species] #.split(',') ]
        elif genre_ in prefix_before:
            [ digest.append(genre_) ]
            [ digest.append(genre_+' '+k) for k in species] #.split(',') ]
        else:
            print("Warn:", name, "could not be parsed")
            digest.append(name)
            pass

        return digest


