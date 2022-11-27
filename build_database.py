#!/usr/bin/env python

"""

Usage: python3 ./build_database.py 1> ./database.csV

The purpose of this code is to create a database with an assumed seven 
rankings in "The Flavor Bible" and related literature for the strengths
of flavor combinations:

0. The source ingredient
1. *BOLD CAPS (with asterisk): "Holy Grail" flavor combination
   e.g. Basil and Garlic
2. BOLD CAPS: highly recommended
   e.g. Basil and Olive Oil
3. bold: frequently recommended
   e.g. Basil and Lemon
4. normal: known to work well together
   e.g. Basil and Black Pepper
5. not mentioned
   e.g. Basil and Walnuts
6. AVOID: known to not work well together
   e.g. Basil and Tarragon

So, while 
 basil + garlic + olive oil + Parmesan cheese + pine nuts
is a natural flavor affinity (i.e. pesto), 
 basil + garlic + olive oil + lemon + black pepper + walnut
also has strong flavor affinity and in my experience makes a 
wonderfully fine pesto, too.

The overall purpose of this project is to first create a machine 
readable database (from the various book's epub files) of flavor 
affinities and then creat an input system so that a chef can either 
visualize graphs of possible flavor combinations given several input
ingredients or so that she may learn interactively a new approach to 
recipe creation.

"""

import pandas as pd
from bs4 import BeautifulSoup
import re

def isCap(x) : return x.isupper()

def what_rank(x):
    if x.find_all(re.compile("^strong")):
        if "*" in x.text :
            rank = "1"
        elif isCap(x.text):
            rank = "2"
        else:
            rank = "3"
    else:
        rank="4"

    return rank


markup = open("./input/basil-2.html")
soup = BeautifulSoup(markup, features="lxml")

entry_tag = soup.select(".lh1")
print(entry_tag[0].text, "0")

first_hit = soup.select(".ul")
print(first_hit[0].text, what_rank(first_hit[0]))
    
avoid_hits=""
for tag in first_hit[0].find_next_siblings(re.compile("p"), class_="ul"):
    if avoid_hits=="AVOID" and str("+") in tag.next_sibling.next_sibling.text:
        break
    if tag.text=="AVOID":
        avoid_hits=str("AVOID")
        continue
    elif avoid_hits=="AVOID":
        print(tag.text, "6")
        continue
    print(tag.text, what_rank(tag))


