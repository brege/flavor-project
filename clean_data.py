"""
Convert primitive `bible.json` to a better structures `bible_clean.json`

Usage:
    bible_clean.py <input> <output>

Options:
    -h --help   Show this screen.

`bible.json` is structurd like this:
    {
        "INGREDIENT 1": {
            "ingredient 1": 0,
            "ingredient 2": j1,
            /* ... */
            "ingredient n": k1
        },
        "INGREDIENT 2": {/* ... */},
        /* ... */
        "INGREDIENT n": {
            "ingredient n": 0,
            "ingredient 1": jn,
            /* ... */
            "ingredient n-1": kn-1
        }
    }

and we want to convert it to this:
    {
        "ingredient 1": {
            "ingredient 1": 0,
            "ingredient 2": j1,
            /* ... */
            "ingredient n": k1
        },
        "ingredient 2": {/* ... */},
        },
        /* ... */
        "ingredient n": {
            "ingredient n": 0,
            "ingredient 1": jn,
            /* ... */
            "ingredient n-1": kn-1
        }
    }

1. sometimes, the ingredient name is not the same as 
    the key, so we need to convert it to the same name.
    - e.g., `INGREDIENT 1 \u2014 IN GENERAL`, to: `INGREDIENT 1`

2. sometimes we have alias/pointer enries like this:
    "ASIAN CUISINE": {
        "asian cuisine": 0,
        "(See Chinese, Japanese, Vietnamese, etc. Cuisines)": 1
    },
    so we need to just remove the entry (for now)

3. remove the source ingredient, it's superfluous

4. remove entries only mentioned a few times

5. convert all the keys to lower case

6. remove asterisks

"""

import os
import json
import re
import sys
import pandas as pd

def remove_alias(bible):
    """Remove alias"""
    for key in list(bible.keys()):
        if len(bible[key]) < 3:
            #print("Removing alias entry: {}".format(key))   
            del bible[key]

# [scares me]
def strip_asterisks(bible):
    """Strip asterisks"""
    for key in list(bible.keys()):
        if '*' in key:
            bible[key.replace('*', '')] = bible[key]
            #print("Renaming key: {} to {}".format(key, key.replace('*', '')))
            del bible[key]
        for entry in list(bible[key].keys()):
            if '*' in entry:
                bible[key][entry.replace('*', '')] = bible[key][entry]
                #print("Renaming entry: {} to {}".format(entry, entry.replace('*', '')))
                del bible[key][entry]

def remove_general(bible):
    """Remove general"""
    for key in list(bible.keys()):
        # the epub uses a different dash sometimes: '-' vs '\u2014'
        if '\u2014 IN GENERAL' in key or '- IN GENERAL' in key:
            bible[key.replace('\u2014 IN GENERAL', '').replace('- IN GENERAL', '')] = bible[key]
            #print("Renaming key: {} to {}".format(key, key.replace('\u2014 IN GENERAL', '').replace('- IN GENERAL', '')))
            del bible[key]

def remove_first_entry(bible):
    """Remove first entry"""
    for key in list(bible.keys()):
        if list(bible[key].values())[0] == 0:
            del bible[key][list(bible[key].keys())[0]]

def remove_see_also(bible):
    """Remove see also"""
    for key in list(bible.keys()):
        for entry in list(bible[key].keys()):
            if '(See' in entry:
                #print("Removing entry: {}".format(entry))
                del bible[key][entry]

# TODO: these last four functions are all the same logic, 
#       so we should combine them into one function

#def remove_parentheses(bible): return bible
#def fixKEY(bible): return bible

def convert_to_lower_case(bible):
    """Convert to lower case"""
    for key in list(bible.keys()):
        if key.lower() != key:
            bible[key.lower()] = bible[key]
            del bible[key]

def remove_empty_keys(bible, n):
    """Get total count"""

    # convert to dataframe to sort, then convert
    # back to dict (annoying)
    df = pd.DataFrame.from_dict(bible, orient='index')
    df = df.sum(axis=1, numeric_only=True)
    df = df.sort_values(ascending=False)
    df = df.to_dict()

    entry_keys = []
    entry_dict = {}
    for key in list(bible.keys()):
        for entry in list(bible[key].items()):
            entry_key = entry[0]
            # we need to make a running list of all the 
            # entry keys so we can determine how many times
            # an entry is mentioned anywhere in the bible
            if entry_key not in entry_keys:
                entry_keys.append(entry_key)
                entry_dict[entry_key] = 1
            else:
                entry_dict[entry_key] += 1

    # sort the entry_dict by the number of times it appears
    df = pd.DataFrame.from_dict(entry_dict, orient='index')
    df = df.sort_values(0, ascending=False)
    df = df.to_dict()

    # now reconstruct df to only include key entries 
    # that have more than 2 appearances
    df = pd.DataFrame.from_dict({key: value for key, value in df[0].items() if value > n}, orient='index')  
    df = df.sort_values(0, ascending=False)
    df = df.to_dict()

    # loop through all the keys and remove entries
    # that are not in the dataframe
    for key in list(bible.keys()):
        for entry in list(bible[key].items()):
            if entry[0] not in df[0].keys():
                del bible[key][entry[0]]

    return df

def is_bible_modified(old_bible, new_bible):
    """Is bible modified"""
    if old_bible != new_bible:
        # this checks:
        # 1. if the number of keys is different
        # 2. if the number of entries is different
        # a more robust check would be to compare the
        # to do a deep comparison of the dictionaries..
        print("Bible has been modified")
    else:
        print("Bible has not been modified")

# clean the bible
def clean_bible(bible):
    """Clean bible"""
    remove_alias(bible)
    remove_general(bible)
    remove_first_entry(bible)
    strip_asterisks(bible)
    convert_to_lower_case(bible)
    remove_see_also(bible)
    # get the total count of appearances for each
    # entry in the bible, and remove entries that
    # only appear less than n times
    remove_empty_keys(bible, n=2)

# write the bible
def write_bible(bible, output):
    """Write bible"""
    # if arg1 and arg2 are the same, then make a copy
    # of arg1 and write to that
    if input == output:
        output = input + '.copy'
    # write the new file
    with open(output, 'w') as file:
        json.dump(bible, file, indent=2, sort_keys=True)

class convertRank:
    """Convert rank"""
    def __init__(self, n):
        self.n = n
    def to_weight(n):
        """To weight"""
        eps = 1e-6
        try: m = int(n)
        except: pass
        if n < -eps: return 0
        elif n > eps: return 5-n
        else: return 0
    def to_binary(n):
        """To binary"""
        eps = 1e-6
        try: m = int(n)
        except: pass
        if n < eps: return 0
        elif n > eps: return 1
        else: return 0

def apply_weight(bible):
    """Apply weight"""
    for key, value in bible.items():
        for entry, rank in value.items():
            if entry == 'topics' or entry == 'affinities':
                continue
            bible[key][entry] = convertRank.to_weight(rank)

def main():
    """Main"""
    # get the input and output files
    input = sys.argv[1]
    output = sys.argv[2]
    # read the file
    with open(input) as file:
        bible = json.load(file)
    # clean the bible
    clean_bible(bible)
    # apply weight
    apply_weight(bible)
    # write the bible
    write_bible(bible, output)

if __name__ == '__main__':
    main()

# Path: clean_bible.py