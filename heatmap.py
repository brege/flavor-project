import pandas as pd
import os.path

def set_from_df_col(x):
    X = set()
    for i in x.index:
        try:
            int(x[i])
            if x[i] > 0:
                X.add(i)
        except: continue
    return X

def intersection_of_n_sets(D, v, n):
    L = set_from_df_col(D[v[n-1]])
    if n == 0:
        return L
    else:
        n -= 1
        R = intersection_of_n_sets(D, v, n)
        return L.intersection(R)

def find_triplets(v):
    # provides a list of all triplets for all elements in a slice
    # finds all "m \choose 3" triples in v, m \ge 3
    m = len(v)
    u = []
    for i in range(m):
        for j in range(i+1, m):
            for k in range(i-1, m):
                if k > j and j > i:
                    u.append([v[i], v[j], v[k]])

    return u
 
def affinities_of_slice(D, v):

    # finds the affinities, which are defined as a triplet set A of 
    # a slice v in D, plus the elements x_j found in the intersection 
    # of u_i's in the triplet u

    # list of all triplets u of slice v
    u = find_triplets(v)

    W = []    
    for u_i in u:
        # the triplet u_i, as a set U_i
        U_i = set(u_i)

        # set of all elements w in the total intersection 
        # of triplet U_i 
        w_i = intersection_of_n_sets(D, u_i, len(u_i))

        # determine which elements in the set w are canonical in D,
        # thus determining the canonical set W for each triplet
        # intersection U
        W_i = set(w.upper() for w in w_i if w.upper() in D.T.index)

        W.append(W_i)

    # finally, determine the auxilary set of W for given depth order
    x = set(v)
    for w in W:
        x = x.union(w)

    aux = x.difference(v)

    return list(x)#, list(aux)

def expand_from_affinities(D, v, depth):
    if depth == 0:
        return v
    else:
        depth -= 1
        v = affinities_of_slice(D, v)
        print("==============")
        print("depth:",depth)
        print("slice:",v)

        return expand_from_affinities(D, v, depth)
        

A = pd.read_pickle('.jac_sim_df.pkl')
B = pd.read_pickle('.convert_rank_to_binary_df.pkl')
v = ['BASIL', 'CHEESE, PARMESAN', 'GARLIC', 'OLIVE OIL', 'PINE NUTS']

# [scratch] how to return x-indexed u-rows of A:   print( A[A.index.isin(u)] )
# [scratch] how to return y-indexed u-cols of A:   print( A[u] )
# [Exercise]: find triplets in a set and see if we can generate:
# "Flavor Affinity: basil + garlic + olive oil + <missing piece>"

depth=1

print("==============")
print("depth:", depth)
print("slice:", v)
v = expand_from_affinities(B, v, depth)

print(v)

# [Exercise]: generate a Level 2 heat map using only the auxilary 
# ingredients to v


# PLOTTING:
#
# This will generate a 2D heat map of the canonical ingredients in 
# the slice v, such that every triplet yields an intersecting value
# (canonical in A), the set of which is auxilary and appended to 
# the slice v.  This will, in turn, produce a new slice v', of which 
# its auxilary elements can be used to find new triplet intersects
# (in A), and so on (iterated to a specified depth).
#
# Note that we do not require the auxilary elements to have 
# intersecting sets in the opposite direction for all v^i, just some,
# as /their/ conjugate sets adhere to a criteria that we are building 
# affinities from a seeded slice anyway (the goal is to be able to 
# round out menus and inventory with a tractable flavor metric.
#
# The heatmap for the full set of ~700^2 canonical ingredients is 
# practically meaningless other than to find holes in the parser
# data. Instead, having a way to build out a recipe from a set of
# ingredient keys is much more valuable, and easier to understand
# with a similarity heatmap.

#v.append('COFFEE AND ESPRESSO')
#v.append('BANANAS')
#v.append('BUTTERMILK')

data = (A[v])[A.index.isin(v)]
data = data[sorted(data.columns)]
print(data)
print()
data.to_pickle('.pesto.pkl')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import seaborn as sns

plt.style.use("seaborn")
heat_map = sns.heatmap( data , cmap='viridis', norm=LogNorm(), linewidth = 0 , annot = True )
plt.title("Jaccard Similarity of Pesto")
plt.show() 
