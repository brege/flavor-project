# * if there are m columns of a vector A,
#   there are m sets
# * if the n members of each set have a presence, either [0] or [1],
#   there is an associated weight, values \in [0..real]

# For a justification of this method, see:
#   https://arxiv.org/pdf/1809.04052.pdf

def weighted_jaccard_probability(x, y):
    # input: 2 (two) n*1 vectors x and y
    # does:
    #   From a pair of vectors of length n (columns of an n*m matrix A)
    #   it returns the weighted set overlap of elements within that pair
    # output: number
    sim = 0
    n = len(x)
    for i in range(n):
        nom, den = 1, 0
        if x[i] > 0 and y[i] > 0:
            for j in range(n):
                den += max(x[j]/x[i], y[j]/y[i])
        else: continue
        if den > 0:
            sim += nom/den
        else: continue
    return sim

def jaccard_probability_distribution(A):
    # input: n*m np array A
    # does:
    #   Constructs a similarity matrix of A, whose values are
    #   determined by weighted set overlaps (column compatability) 
    #   of A. To do so, loop through all possible vector pairs of A
    # output: m*m np array J, elements of which are score values
    m = len(A)
    J=[]
    for i in range(m):
        J_i=[]
        for j in range(m):
            #print(i, j, "in", m)
            j_prob = weighted_jaccard_probability(A[i], A[j])
            J_i.append(j_prob)
        J.append(J_i)
        print(J)
    return J

# TESTING different matrices
'''
import pandas as pd
import numpy as np

np.random.seed(0)
df = pd.DataFrame(np.random.binomial(1, 0.5, size=(100, 5)), columns=list('abcde'))
print("Start with:\n", df)

from scipy.spatial.distance import pdist, squareform
print("From jaccard metric, where elements are binary:")
jac_dist = pdist(df.T, metric = "jaccard")
jac_dist = squareform(jac_dist)
jac_dist_df = pd.DataFrame(jac_dist, index=df.columns, columns=df.columns)
# or, put elsewise:
jac_sim = 1 - jac_dist
jac_sim_df = pd.DataFrame(jac_sim, index=df.columns, columns=df.columns)
print(jac_sim_df)
print()

print("Jaccard Probability Distribution Matrix") 
B = [[1, 3, 0], [0, 1, 2], [1, 2, 1], [5,5,1]]
#B = [[1,0,0],[0,1,0],[0,0,1]]
#B = [[1,1,1],[1,1,1],[1,1,1]]
B = [[1,0,0],[1,0,0],[1,0,0]]
#A = [[1, 1, 0], [0, 1, 1], [1, 1, 1], [1,1,1]]
bf = pd.DataFrame(B,columns=list('abc'))
print()
print("Start with:\n",bf)
B = bf.T.to_numpy()
J_p = jaccard_probability_distribution(B)
print()
print("Then J_P is:\n",pd.DataFrame(J_p, columns=bf.columns))

print("Checking to see if J_p of a binary matrix gives\nsame scores as the built in jaccard metric:")

print(df.head(6),'\n..\n',df.tail(2))
print(jac_sim_df)
bf = df
B = bf.T.to_numpy()
J_p = jaccard_probability_distribution(B)
print( pd.DataFrame(J_p, columns=bf.columns) )
'''
