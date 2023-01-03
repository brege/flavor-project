"""
Usage:
    compute_similarities.py input_json_file output_json_file

The input json file should the file that was output by
the clean_data.py script, whereas the output json file 
from this script will be the similarity matrix, but only 
for the canonically title ingrdients.
"""

import pandas as pd
import numpy as np
import os.path
import json
import sys
from sklearn.metrics.pairwise import pairwise_distances

def set_from_df_col(df, col):
    # get the set of non-zero entries
    return set(df[col][df[col] > 0].index.values)

def simple_jaccard_similarity(A, B):
    # A and B are sets
    if len(A.union(B)) == 0 or len(A.intersection(B)) == 0:
        return 0
    else:
        return len(A.intersection(B))/len(A.union(B))

def jaccard_similarity(df):
    cols = df.columns.values
    sim_matrix = np.zeros((len(cols), len(cols)))
    for i in range(len(cols)):
        for j in range(i+1, len(cols)):
            # construct the sets
            A = set_from_df_col(df, cols[i])
            B = set_from_df_col(df, cols[j])
            sim = simple_jaccard_similarity(A, B)
            sim_matrix[i,j] = sim
            sim_matrix[j,i] = sim
    # convert to a dataframe
    sim_matrix = pd.DataFrame(sim_matrix, index=df.columns, columns=df.columns) 
    return sim_matrix

def similarity_from_metric(df, metric):
    # of interst:
    #  'cosine', 'hamming', 'jaccard'
    # you need to pass the datframe values, not the 
    # dataframe itself (p. for 'jaccard')
    metric_dist = pairwise_distances(df.T.values, metric = metric, n_jobs=-1) 

    sim_matrix = 1 - metric_dist
    sim_matrix = pd.DataFrame(sim_matrix, index=df.columns, columns=df.columns)

    return sim_matrix
        
   

# this is the test function
def test():
    """Usage: test()"""

    # use this preformatted sparse matrix
    print('using preformatted sparse matrix')
    df = pd.DataFrame(np.random.binomial(1, 0.2, size=(100, 5)), columns=list('ABCDE'))
    print(df.head(5).tail(3))

    print('checking metrics...')

    # test the (metric) jaccard similarity
    print('jaccard')
    print(similarity_from_metric(df, 'jaccard'))

    # test the cosine similarity
    print('cosine')
    print(similarity_from_metric(df, 'cosine'))

    # test the hamming similarity
    print('hamming')
    print(similarity_from_metric(df, 'hamming'))

    # test the simple jaccard similarity
    print('jaccard - simple')
    print(jaccard_similarity(df))

    # test the set_from_df_col function
    print('check ing two sets...')
    print('set_from_df_col')
    print(set_from_df_col(df, 'A'))
    print(set_from_df_col(df, 'B'))

    # test the simple_jaccard_similarity function
    print('simple_jaccard_similarity')
    print(simple_jaccard_similarity(set_from_df_col(df, 'A'), set_from_df_col(df, 'B')))

# this is the main function
def main():

    #test the functions:
    #test()

    # get the input and output files
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # construct dataframes from the json files
    df = pd.read_json(input_file)
    df = df[df.index.str.contains("topics")==False]
    df = df[df.index.str.contains("affinities")==False]
    df = df.fillna(0)

    # compute the similarity matrix
    '''see notes'''
    sim_matrix = similarity_from_metric(df, 'jaccard')
    
    # make it so it's in three decimal places
    sim_matrix = sim_matrix.round(3)

    # save the similarity matrix, but make sure  
    # it's formatted so humans can read it 
    sim_matrix.to_json(output_file, orient='index', indent=2)   
    # this writes the similarity matrix to a json file.
    # it's only for canonical key nodes, not every node

if __name__ == "__main__":
    main()

"""Notes:

    Unfortunately, the jaccard similarity converts the weights to
    binary values, so we need to convert them back to weights

    This is actually a pretty non-trivial problem:
    - https://arxiv.org/pdf/1809.04052.pdf
    and there is no weighted algorithm for jaccard metrics with 
    pairwise_distances in sklearn at this time.
     
    I have an unvectorized implementation of this in the
    'jaccard_probability_measure.py' file, but it's not
    fast enough to be used in this context (it isn't so bad
    with the text() function, but it will take all night for
    the full dataset...)

    I did run the script on a randomized slice of the dataset,
    and the results were very marginally different from the
    binary jaccard similarity.

    However, when it comes to the network graphing, there might
    be some tricks to marry the weighted and binary jaccard
    similarity measures.  I'll have to think about this more.
"""

