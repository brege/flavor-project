# see "unique_affixes.txt" for a full list of A's that 
# appear from splitting A:B text in the <p> tags

# SUFFIX
# Input type:
#
#   'vinegar: balsamic, red wine, rice, sherry'
#
# Output:
# 
#   'balsamic vinegar, red wine vinegar, rice vinegar, sherry vinegar'
# in the dictionary.
suffix = ['cheese', 'oil', 'oils', 'pepper', 'wine', 
          'sugar', 'salads', 'squash', 'stocks', 'mushrooms',
          'salt', 'ham', 'seeds', 'bell peppers', 'ginger',
          'beans', 'eggs', 'chocolate', 'crust' ]

# PREFIX
# Input type:
#   sauces: béarnaise, beurre blanc, brown butter hollandaise
#
# Output:
#
#   béarnaise, beurre blanc, brown butter hollandaise
prefix = ['sauce', 'spices', 'berries']

# PREFIX+
# Input type:
#   'lime: juice, leaves'
# 
# Output:
#
#   'lime, lime juice, lime leaves'
prefix_plus = ['lime', 'orange', 'lemon', 'yuzu', 'sesame', 
               'chili peppers', 'curry', 'roe', 'grapefruit',
               'coconut', 'game']

# case-by-case:
case_by_case = ['mushrooms: cultivated, shiitakes',
                    'mustard: Dijon, seeds',
                    'noodles: angel hair, vermicelli, rice',
                    'apples: cider, fruit',
                    'olives: black, niçoise',
                    'TOMATOES: canned, paste, plum, sauce',
                    'innards: turkey heart, liver']
