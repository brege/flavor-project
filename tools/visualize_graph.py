# thank you: https://stackoverflow.com/questions/61421491/
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

df = pd.read_pickle('../output/.convert_rank_to_weight_df.pkl')
bf = pd.read_pickle('../output/.jac_sim_df.pkl')

#v = ['BANANAS']
v = ['BASIL', 'CHEESE, PARMESAN', 'GARLIC', 'OLIVE OIL', 'PINE NUTS']
a = v[0]

if len(v) < 2:
    v = []
    n = 11
    print("Generating seed list from top matching ingredients") 
    Bf = bf[a].nlargest(n)
    for idx in Bf.index:
        v.append(idx)

A = df[a].nlargest(25)
V = df[v]

for idx in V.T.index:
    V[idx] = V[idx].nlargest(15)
A = A.nlargest(20)

GG = []
for i in range(len(v)):
    GG.append(nx.Graph())
    for idx in V.index:
        if V[v[i]][idx] > 0:
            GG[i].add_edge(v[i], idx)
    GG[i].nodes()

G=nx.Graph()
H=nx.Graph()

for idx in A.index:
    if A[idx] > 0:
        G.add_edge(a, idx, weight=A[idx], width=A[idx]**2)
#    if B[idx] > 0:
#        H.add_edge(b, idx, weight=B[idx], width=B[idx]**2) 

G.nodes()
H.nodes()

H = nx.compose_all(GG)
GH = nx.compose(G,H)
   
GH.nodes()

# set edge colors
edge_colors = dict()
for edge in GH.edges():
    if G.has_edge(*edge):
        if H.has_edge(*edge):
            edge_colors[edge] = 'green'
            continue
        edge_colors[edge] = 'lightgreen'
    elif H.has_edge(*edge):
        edge_colors[edge] = 'lightblue'

# set node colors
G_nodes = set(G.nodes())
H_nodes = set(H.nodes())
node_colors = []
for node in GH.nodes():
    if node in G_nodes:
        if node in H_nodes:
            node_colors.append('green')
            continue
        node_colors.append('lightgreen')
    if node in H_nodes:
        node_colors.append('lightblue')

pos = nx.spring_layout(GH, scale=20)

edge_weights = nx.get_edge_attributes(GH, 'weight')
ws = np.multiply(list(edge_weights.values()),2)

nx.draw(GH, pos, 
        nodelist=GH.nodes(),
        node_color=node_colors,
        edgelist=edge_colors.keys(), 
        edge_color=edge_colors.values(),
        node_size=200,
        width=ws,
        alpha=0.5,
        with_labels=True)

plt.savefig('../fig/visualize-graph.png')
plt.show()
