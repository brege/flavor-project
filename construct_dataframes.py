import pandas as pd
import numpy as np
import os.path
import src.flavor_tools as ft
import test.jaccard_probability_measure as jpd

def simple_jaccard_similarity(A, B):
    nom = A.intersection(B)
    den = A.union(B)
    similarity = len(nom)/len(den)
    return similarity

# right now, these three methods squash subcategorical data in 
# the json tree, which is a huge problem because a lot of 
# wines and cheeses are left out
def convert_rank_to_proximity(n):
    eps = 1e-3
    try:
        m = int(n)
        if n < eps:
            return 0 #makes data enemy-agnostic
        else:
            return 1/n# - (n/5.)**2*np.exp(n/5.)
    except: 
        print("WARN", n)

def convert_rank_to_binary(n):
    eps = 1e-3
    try:
        m = int(n)
        if n <= eps or n >= 4 + eps:
            return 0 #makes data enemy-agnostic
        else:
            return 1
    except:
        print("WARN")

def convert_rank_to_weight(n):
    eps = 1e-3
    try:
        m = int(n)
        if n < -eps:
            return 0 #makes data enemy-agnostic
        elif n > eps:
            return 5-n
        else: return 0 
    except:
        print("WARN")

# working on getting pointers in json file to replace values
# in the dataframe:
# (e.g.)
#  "DANDELION GREENS": {
#    "dandelion greens": 0,
#    "(See Greens, Dandelion)": 1
#  },
# we probably just want to quite these for now, and then use 
# the nat-lang toolkit with these for search queries on the web

def reference_pointers(D):
    refs=[]
    for idy in D.index:
        if "also" in idy:
            continue
        if "(See " in idy:
            refs.append(idy)
    return refs

def drop_sparse_rows(D):
    refs = reference_pointers(D)
    D = D.drop(refs)
    return D

def drop_sparse_cols(D,n):
    i = 0
    print("Removing any rows that might be too sparse")
    for idx in D.T.index:
        col_red = ft.set_from_df_col(D[idx])
        if len(list(col_red)) < n:
            #print("DROPPING:", idx, '=', col_red)
            i += 1
            del D[idx]
    print("Removed", i, "titular entries")

    # determine global-rank population (No. of json 2's, 3's etc)
    for m in range(-1,5):
        print(m, convert_rank_to_weight(m), count_global_ranks(df, m) )

    return D

def count_global_ranks(D,n):
    return np.count_nonzero(D==n)

input_dir = "/home/notroot/Build/flavor-project/"
input_file = "bible.json"
file = os.path.join(input_dir, input_file)
df = pd.read_json(file)  

df0 = df

##
# Create a new dataframe that:
#   1. removes metadata
#   2. replaces NaN with "5"
#   3. normalizes distances [-1:5] to similarities abs(w)<1 
##

df = df[df.index.str.contains("topics")==False]
df = df[df.index.str.contains("affinities")==False]
df = drop_sparse_cols(df,3)

dw = df.fillna(0)
df = df.fillna(5)
dw_w = dw.apply(np.vectorize(convert_rank_to_weight))
dw_w.to_pickle('.convert_rank_to_weight_df.pkl')
print(dw_w)

df = df.apply(np.vectorize(convert_rank_to_binary))
df.to_pickle('.convert_rank_to_binary_df.pkl')

from sklearn.metrics.pairwise import pairwise_distances
print(" From hamming metric:")
ham_sim = 1 - pairwise_distances(df.T, metric = "hamming")
ham_sim_df = pd.DataFrame(ham_sim, index=df.columns, columns=df.columns)
ham_sim_df.to_pickle('.ham_sim_df.pkl')
#print(ham_sim_df)


from scipy.spatial.distance import pdist, squareform
print(" From jaccard metric:")
jac_dist = pdist(df.T, metric = "jaccard")
jac_dist = squareform(jac_dist)
jac_dist_df = pd.DataFrame(jac_dist, index=df.columns, columns=df.columns)
jac_sim = 1 - jac_dist
jac_sim_df = pd.DataFrame(jac_sim, index=df.columns, columns=df.columns)
jac_sim_df.to_pickle('.jac_sim_df.pkl')
#print(jac_sim_df)


#'''
print("=======================================================================")
print("  TESTING                                                              ")
print("=======================================================================")
a = 'BASIL'
b = 'GARLIC'
c = 'TARRAGON'
print()

# This does not give the same results as the 
# next methods, despite what this says:
#   https://stackoverflow.com/questions/37003272/how-to-compute-jaccard-similarity-from-a-pandas-dataframe
print("#0) SciKit Learn - Hamming Metric:")
print(a, b, ham_sim_df[a][b])
print(a, c, ham_sim_df[a][c])
print(b, c, ham_sim_df[b][c])
print() 

# the next three dumps all give the same results:
print("#1) SciPy Spatial - Jaccard Metric:")
print(a, b, jac_sim_df[a][b])
print(a, c, jac_sim_df[a][c])
print(b, c, jac_sim_df[b][c])
print()

from sklearn.metrics import jaccard_score
print("#2) SciKit Learn - Jaccard Score [Direct Elementary Computation]:")
print(a, b, jaccard_score(df[a], df[b]))
print(a, c, jaccard_score(df[a], df[c]))
print(b, c, jaccard_score(df[b], df[c]))
print()

print("#3) Raw Element Calculation - Simple Jaccard Method:")
A = ft.set_from_df_col( df[a] )
B = ft.set_from_df_col( df[b] )
C = ft.set_from_df_col( df[c] )
print(a, b, simple_jaccard_similarity(A, B))
print(a, c, simple_jaccard_similarity(A, C))
print(b, c, simple_jaccard_similarity(B, C))
print()

print("#4 Raw Element Calculation - Weighted Jaccard Method:")

#print(dw_w)
D_a = dw_w[a].T.to_numpy()
D_b = dw_w[b].T.to_numpy()
D_c = dw_w[c].T.to_numpy()

print(a, b, jpd.weighted_jaccard_probability(D_a, D_b))
print(a, c, jpd.weighted_jaccard_probability(D_a, D_c))
print(b, c, jpd.weighted_jaccard_probability(D_b, D_c))

#D = dw_w.T.to_numpy() 
#J_P = jpd.jaccard_probability_distribution(D)
#print(J_P)
#J_P.to_pickle('.jaccard_prob_dist.pkl')
