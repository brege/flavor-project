def set_from_df_col(x):
    X = set()
    for i in x.index:
        if x[i] > 0:
            X.add(i)
    return X

def intersection_of_n_sets(D, v, n):
    L = set_from_df_col(D[v[n-1]])
    if n == 0:
        return L
    else:
        n -= 1
        R = intersection_of_n_sets(D, v, n)
        return L.intersection(R)
