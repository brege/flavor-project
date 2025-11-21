#!/usr/bin/env python

"""

Usage: python ./parse.py  

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
-1. AVOID: known to not work well together
   e.g. Basil and Tarragon

So, while 
    basil + garlic + olive oil + Parmesan cheese + pine nuts
is a natural flavor affinity (i.e. pesto), 
    basil + garlic + olive oil + lemon + black pepper + walnut
also has strong flavor affinity and in my experience makes a 
wonderfully fine pesto, too, esp. in grilled chicken wraps.  

It would be good to visualize paths between ingredients that 
one might have on hand, or that might be in season together, 
or explore what's common between two cuisines--e.g. Thai, 
Mexican, and Italian all have paths between each other but we 
don't see their fusions as frequently as we do with Brazilian and 
Japanese or French and Creole which have clear culturally historic 
blending.  Can we predict ingredient pathways between African and 
Chinese cuisines based on nontrivial ingredients the same way, say, 
Indian curries might interface with British cuisine today?   

The overall purpose of this project is to first create a machine 
readable database (from the various book's epub files) of flavor 
compatablities and then create an input system so that a chef 
can either visualize graphs of possible (new) flavor combinations 
given several input ingredients or so, so that she may learn 
and interactively chart a course in recipe creation.

"""

from bs4 import BeautifulSoup
import re
import glob
import os.path
import json
import src.utils.brackets as pb
from src.utils.genres import isCulinaryGroup

##
# Matching Flavors Heuristic (cf. pp 37)
# TODO: Normalize with a power law?
# Note that these ranks can be thought of as the distance from the source
# ingredient.
##


# This only works for singleton ingredients:
def what_rank(x):
    if x.find_all(re.compile("^strong")):
        if "*" in x.text:
            rank = 1
        elif isCap(x.text):
            rank = 2
        else:
            rank = 3
    else:
        rank = 4
    return rank

def rank_subtags(Y, ptag):
    rank = lambda x: 4 - x
    y = [rank(0) for y_i in Y]
    s_tags=ptag.find_all('strong')
    for s_tag in s_tags:
        for j in range(len(Y)):
            Y[j] = Y[j].strip()
            if Y[j] in s_tag.text:
                y[j] = rank(1)
                if Y[j].isupper(): y[j] -= 1
                if "*" in Y[j]: y[j] -= 1
    return Y, y

def isCap(x) : return x.isupper()

# General qualifiers of principal ingredient -- Chef's Almanac
def contains_topics(x, a):
    for i in range(len(x)):
        if x[i] in a:
            return x[i], a.replace(x[i], '').strip()

# Super combos of highly matching ingredients
# Generally: source + supporting ingredient 1 [+...]
def contains_affinity(b):
    if " + " in b:
        return 1

# Incompatable flavors
def contains_avoid(c):
    if "AVOID" in c:
        return 1

# useful for debugging when parsing parens doesn't work:
def remove_parens(a):
    return re.sub(r'\([^)]*\)', '', a).strip()

# TODO: move to config file, there we can handle special cases
#       that we just have to hardcode
topics = ["Season:", 
          "Taste:", 
          "Function:",
          "Weight:", 
          "Volume:", 
          "Techniques:",
          "Tips:",
          "Tip:", 
          "Use ", 
          "Botanical relative:", 
          "Botanical relatives:", 
          "Weather:",
          "Character:"]
          # "Use " has several instances after these cues (cf. Page 37) 
          # in the book that /should/ be caught with "Tips:", although
          # "Tips:" has its own class=ul3, but some other content 
          # falls in that class, too.  [errata] 

# in the beginning..
bible = {}

input_dir = "./input/"
input_files = "FlavorBible_chap-3*.html"

for input_file in glob.glob(os.path.join(input_dir, input_files)):
    with open(input_file) as markup:

        soup = BeautifulSoup(markup, features="html.parser")
        ##
        # In the source files of the book, FlavorBible_chap-3*.html, the source 
        # ingredient is given by .lh1, but sometimes .lh, while the friendly, 
        # enemy, and super-alliance ingredients are captured by .ul and .ul1 
        # within the .lh* bounds (so is some metadata that will be useful later)
        ##
        classes = ["lh","lh1","ul","ul1","ul3"]
        ptags = soup.find_all("p", class_=classes)   

        # build the dictionary from each input html chapter file
        for ptag in ptags:

            ##
            # SOURCES
            ##  determine the titular ingredients

            T = list(ptag.children)

            if ptag['class'] == ['lh'] or ptag['class'] == ['lh1']:
                flag = 0
                dummy_array=[]
                dummy_dict={}
                ###
                # Sometimes, the title tags concatenate mistakenly:
                #
                # <p class="lh">WALNUT OIL <strong>(See Oil, Walnut)</strong>
                #   WALNUTS <strong>(See also Nuts — In General)</strong></p>
                #
                # or just have special references:
                #
                # <p class="lh1">ANISE <strong>(See also Anise, Star, and Fennel)</strong></p>
                #
                # In first case, the initial title (WALNUT OIL) is actually a pointer 
                # to  another entry somewhere else in the book (OIL, WALNUT), as no
                # ingredient line items are present.  On the other hand, the second 
                # title (WALNUTS) should be treated as the real title to the following
                # list of ingredients, and its parens (i.e. Nuts — In General) treated 
                # as rank-1 (holy grail), for now..
                ###
                # TODO: can this routine be used for all titles?
                if len(T) > 1:
                    for i in range(len(T)):
                        if (T[i]).text.isupper():
                            title = T[i].strip()
                            bible[title] = {title.lower():0}
                        else: continue
                        # capture topic that got mistaken with 'lh1':
                        if "Weight:" in ptag.text:
                            topic = "Weight:"
                            title = T[0].strip()
                            matter = T[2].strip()
                            dummy_dict.update( {topic.replace(':',''):matter} )
                            continue
                        if i < len(T)-1:
                            desc = (T[i+1]).text.strip()
                            bible[title][desc] = 1
                            continue
                        else: continue
                    continue
                else:     
                    title = remove_parens(ptag.text) #double check what's going on here
                    bible[title] = {ptag.text.lower():flag}
                    continue
            # [errata] capture titles that got mistaken with 'ul':
            #   <p class="ul">ZUCCHINI BLOSSOMS <strong>(See also Zucchini)</strong></p>
            elif T[0].text.isupper() and ptag.find('strong').previous_sibling:
                flag = 0
                title = T[0].strip()
                bible[title] = {title.lower():flag}
                bible[title][ptag.find_next('strong').text] = 1
                continue

            ##
            # METADATA
            ##  capture affinities as raw list for each titular ingredient dictionary

            if contains_affinity(ptag.text):
                # will be useful for training the flavor model
                dummy_array.append(ptag.text) 
                bible[title]['affinities'] = dummy_array
                continue

            # rule for non-unanimous consensus of flavor nemeses
            if flag == 1:
                qual = "say some"
                if qual in ptag.text:
                    bible[title][remove_parens(ptag.text)] = -flag/2.
                else: 
                    bible[title][remove_parens(ptag.text)] = -flag/1.
                continue
            if contains_avoid(ptag.text):
                flag = 1
                continue

            # topical subtext for the source ingredient
            if contains_topics(topics, ptag.text):
                topic, matter = contains_topics(topics, ptag.text)
                # now to address [errata]:
                if topic == "Use ":
                    matter = topic+matter
                    topic = "Tips:"
                dummy_dict.update( {topic.replace(':',''):matter} )
                bible[title]['topics'] = dummy_dict
                continue

            # when: a: x (peak Y)
            if re.search('peak ', ptag.text) or re.search('peak: ', ptag.text):
                entry = ptag.text.lower()
                entry = remove_parens(entry)
                # print("contains peak", entry, what_rank(ptag))
                bible[title][entry]=what_rank(ptag)
                continue
            # TODO: Keep this data, then parse out in pandas code, but store as a range
            # here because it might be nice to query "October" for the graph, or maybe 
            # it's better to just use a third party seasonal ingredient database that has
            # ag-zone boundaries, since that's how you'd use it. You only see this 
            # heuristic in the book under each of the four seasons.

            ##
            # TARGETS
            ##            
   
            # when: a: x, y, z, [..,]
            # e.g.:
            #
            #   <p class="ul">
            #       <strong>CHEESE: BLUE, Brie, Cabrales,</strong> 
            #       Cambozola, Camembert, Cantal, cheddar, feta, 
            #       <strong>goat, Gorgonzola,</strong> 
            #       Monterey Jack, 
            #       <strong>Parmesan, pecorino,</strong> 
            #       ricotta, Romano, 
            #       <strong>ROQUEFORT, Stilton</strong>
            #   </p>
            #

            # [errata]
            if "When look" in ptag.text: continue
            # [/errata]    

            if re.search(':', ptag.text):
                # this case is much different, because what proceeds the
                # colon ':' is a category (genre) that might either be
                # read after or before or need not be mentioned with the 
                # following matter after the colon (species).  Therefore,
                # in order for the database to reflect natural language, 
                # we must accurately provide the context for that species
                # as close to English as we can.. 

                #if title == 'PEARS': #continue #!Debug
                #    print(ptag)
                rank = lambda x: 4 - x 
                subtitle = ptag.text.split(':')[0]
                subtext = ptag.text.split(':')[1]
                s_tags = ptag.find_all('strong')
        
                # when: a: x (e.g., y), z
                if "(e.g." in subtext:
                    Y = pb.parse_brackets(subtext, r'\(e.g.', r'\)', sep=',')
                else:
                    Y = ptag.text.split(':')[1].strip()
                    Y = Y.split(',')
                

                Y = isCulinaryGroup.orient(ptag.text, subtitle, Y)
                Y, y = rank_subtags(Y, ptag)
                for i in range(len(Y)):
                    subtitle = Y[i].lower().strip('*').strip()
                    bible[title][subtitle] = y[i]

            # when: a (e.g., x, y, [,..])
            elif "(e.g." in ptag.text:
                X = ptag.text
                # [errata: pp. 334]
                if ")" not in X:
                    X+=")"
                # [/errata]
                Y = pb.parse_brackets(X, r'\(e.g.', r'\)', sep=',')
                # [errata pp 151]
                if 'sweet (' in ptag.text:
                    Y = [re.sub(r'sweet \(','', y) for y in Y]
                    Y = [re.sub(r'\)','', y) for y in Y]
                # [/errata]
                Y, y = rank_subtags(Y, ptag)
                for i in range(len(Y)):
                    subtitle = Y[i].lower().strip('*').strip()
                    bible[title][subtitle] = y[i]

            # when: a, b [hopefully]
            else:
                if re.search(',', ptag.text):
                    rank = lambda x: 4 - x
                    X = re.sub('esp. ','',ptag.text)
                    X = re.sub('e.g.,','',X)
                    X = re.sub(' or ','', X) 
                    Y = X.split(',')
                    s_tags = ptag.find_all('strong')

            
                    Y = isCulinaryGroup.orient(X, Y[0], Y[1:])
                    Y, y = rank_subtags(Y, ptag)
                    for i in range(len(Y)):
                        subtitle = Y[i].lower().strip('*').strip()
                        bible[title][subtitle] = y[i]

                # finally, store the ingredients
                subtitle, rank = ptag.text.lower(), what_rank(ptag)
                bible[title][subtitle] = what_rank(ptag)


output_file = open("output/bible.json", "w")
json.dump(bible, output_file, indent = 2)

# TODO: what to do about reference pointers?
# TODO: account for ", esp. [..] or [..]" cases
# TODO: account for ", e.g., [..]" cases
# TODO: account for cuisine [define class?]
