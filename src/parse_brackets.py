import re

def parse_brackets(X, bra, ket, sep):

    '''
    Assumes X is a string containing "abc, bra asdfghjklket"
    Input: 
        X = 'Leiflft, \[LB.A 1.0, B 1.0RB\], C, D \[LB E,FRB\]'
    Config::
        sep = ',' 
        bra = '\[LB.'
        ket = 'RB\]'
    Output::
        Y =['Left', 'A 1.0', 'B 1.0', 'C', 'D', 'E']
    NB: This does not iterate, and regex wizards know better than I how to
        do this succinctly, this approach is familiar to me since you do
        it a lot in finite element methods.
    '''

    # Strategy:
    #
    #   X:  ---------[*,*,*,*]-----[*,*]----,---[*]-----
    #   0:  [---L---][---P---][-----------R------------]
    #   1:  .........[q,q,q,q][-L-][-P-][------R-------]
    #   2:  .......................[q,q][---L--][P][-R-]          
    #   3:  ....................................[q][-L-]
    #   Y:  ............................................
    #
    # N.B. this won't work on nested paren's

    # determine P blocks
    pattern = bra+'.*?'+ket
    print(pattern)
    P = re.findall(pattern, X)
    print(P)
        

         
    # then index the content of the P blocks with Q:
    Q = []
    for i in range(len(P)):
        p = P[i]
        q = re.sub(bra, '', p).strip()
        q = re.sub(ket, '', q).strip()
        Q.append(q)

    # P has context, while Q is a list of strings q_k seperated by, say, ',': 
    #   " P = (e.g., q_0,[.k.,]q_i]) "
    # 1. step through X using P's to separate a L-side and a R-side (i),
    # 2. then, step through the strings l in L and record them with Y (j)
    # 3. repeat using L and R of next P block, but let's record inside 
    #   of previous P block and subdivide it into q's in k-space

    Y = []
    for i in range(len(P)):
        L = X.split(P[i])[0]
        R = X.split(P[i])[1]
        l = L.split(sep)
        for j in range(len(l)):
            Y.append(l[j].strip())
        q = Q[i].split(sep)
        for k in range(len(q)):
            Y.append(q[k].strip())
        # set the next starting place, just right of previous P-block
        X = R

    # maybe there's entries after the last P-block too
    l = R.split(sep)
    for j in range(len(l)): 
        Y.append(l[j].strip())

    # finally, we can remove any empty entries from the list: 
    Y = [y for y in Y if y != '' and y != ' ']

    return Y

'''
# Testing examples:
bra = '\(e.g.,'
ket = '\)'

X = ["strong red (e.g., Cabernet Sauvignon, Zinfandel), dry white (e.g., Riesling), sparkling (e.g., Champagne), sweet (e.g., ice wine)",  "fresh, dried, red, green (e.g., jalapeño)", "seafood (e.g., shrimp)"]
print("input:", X)
 
Y=[]
for x in X:
    y = parse_brackets(x, bra, ket, ',')
    print(y)
    Y.append(y)
'''
