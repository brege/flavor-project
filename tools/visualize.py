import argparse
import os
import json
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser(
        prog='visualize.py',
        description='Visualize ingredient network relationships as a colored graph',
        epilog='Example: python visualize.py -n basil -n garlic -n "olive oil"'
    )

    parser.add_argument(
        '-c', '--clean',
        default='output/clean.json',
        metavar='FILE',
        help='input clean data JSON (default: output/clean.json)'
    )
    parser.add_argument(
        '-s', '--similarity',
        default='output/similarity.json',
        metavar='FILE',
        help='input similarity matrix JSON (default: output/similarity.json)'
    )
    parser.add_argument(
        '-n', '--node',
        action='append',
        dest='seed_nodes',
        metavar='NODE',
        help='seed node for visualization (can specify multiple times)'
    )
    parser.add_argument(
        '-o', '--output',
        default='output/img/visualize-graph.png',
        metavar='FILE',
        help='output PNG file (default: output/img/visualize-graph.png)'
    )

    args = parser.parse_args()

    # Load data from JSON
    with open(args.clean) as f:
        clean_data = json.load(f)

    with open(args.similarity) as f:
        sim_data = json.load(f)

    # Extract numeric data from clean
    clean_numeric = {}
    for ingredient, relations in clean_data.items():
        clean_numeric[ingredient] = {k: v for k, v in relations.items()
                                     if isinstance(v, (int, float))}

    # Convert to DataFrames
    df = pd.DataFrame(clean_numeric).fillna(0).astype(float)
    bf = pd.DataFrame(sim_data).fillna(0).astype(float)

    # Set seed nodes
    if args.seed_nodes is None:
        v = ['basil', 'cheese, parmesan', 'garlic', 'olive oil', 'pine nuts']
    else:
        v = [node.lower() for node in args.seed_nodes]

    # Ensure seed nodes exist
    v = [node for node in v if node in df.index]
    if not v:
        print("Error: no valid seed nodes found in data")
        return 1

    a = v[0]

    if len(v) < 2:
        v = []
        n = 11
        print("Generating seed list from top matching ingredients")
        Bf = bf[a].nlargest(n)
        for idx in Bf.index:
            v.append(idx)

    A = df[a].nlargest(10)
    V = df[v].copy().astype(float)

    for idx in V.T.index:
        V.loc[:, idx] = V[idx].nlargest(10)
    A = A.nlargest(10)

    GG = []
    for i in range(len(v)):
        GG.append(nx.Graph())
        if v[i] in V.columns:
            for idx in V.index:
                if V[v[i]][idx] > 0:
                    GG[i].add_edge(v[i], idx)
        GG[i].nodes()

    G = nx.Graph()
    H = nx.Graph()

    for idx in A.index:
        if A[idx] > 0:
            G.add_edge(a, idx, weight=A[idx], width=A[idx]**2)

    G.nodes()
    H.nodes()

    H = nx.compose_all(GG)
    GH = nx.compose(G, H)

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
    ws = np.multiply(list(edge_weights.values()), 2) if edge_weights else [1]

    nx.draw(GH, pos,
            nodelist=GH.nodes(),
            node_color=node_colors,
            edgelist=edge_colors.keys(),
            edge_color=edge_colors.values(),
            node_size=200,
            width=ws,
            alpha=0.5,
            with_labels=True)

    output_dir = os.path.dirname(args.output)
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(args.output)
    plt.show()

    return 0


if __name__ == '__main__':
    exit(main())
