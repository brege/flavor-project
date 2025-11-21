"""Create nodes and edges from cleaned data.

Usage:
    graph.py <input_file> <output_file_edges> <output_file_nodes>

Options:
    -h --help     Show this screen.

This script creates a file with the edges and a file with the nodes from the cleaned
data (output of clean.py). The output files are used as input for the
create_graph.py script.

Both the input and output files are assumed to be json files.

nodes.json (a list of dicts of key-value pairs):

[
  {
    "id": "garlic",
    "label": "garlic"
    "influence": 234,
  },
  {   
    "id": "basil",
    "label": "basil"
    "influence": 123,
  },
  { /* ... */ }
]

edges.json (a list of dicts of source and target nodes):
[
  {
    "from": "basil",
    "to": "garlic"
    "weight": 4
  },
  {
    "from": "basil",
    "to": "olive oil"
    "weight": 4
  },
  { /* ... */ }
]

cleaned_data.json (a dict of dicts of key-value pairs):
{
  "garlic": {
    "affinities": [
      "garlic + basil + olive oil",
      /* ... */
    ],
    "basil": 4,
    "chicken": 3,
    "olive oil": 4,
    /* ... */
  },
  "basil": {
    /* ... */
  },
  /* ... */
}
"""

import json
from docopt import docopt
import pandas as pd

def show_stats(nodes, edges):
    print('Number of nodes: {}'.format(len(nodes)))
    print('Number of edges: {}'.format(len(edges)))

    # most influential nodes
    print('Most influential nodes:')
    df_nodes = pd.DataFrame(nodes)
    df_nodes = df_nodes.sort_values(by='influence', ascending=False)
    # only show label and influence
    df_nodes = df_nodes[['label', 'influence']]
    print(df_nodes.head(5))

    # there are {} nodes with only 1 or 2 edges:
    print('There are {} nodes with only one edge.'.format(len(df_nodes[df_nodes['influence'] == 1])))
    print('There are {} nodes with only two edges.'.format(len(df_nodes[df_nodes['influence'] == 2])))

    percent_active = len(df_nodes[df_nodes['influence'] > 10]) / len(df_nodes) * 100
    # use two decimal places for the percentage
    percent_active = round(percent_active, 2)
    # the percentage of nodes with more than 10 edges is {}:
    print('The percentage of nodes with more than 10 edges is {} percent.'.format(percent_active))

def main():
    args = docopt(__doc__)

    input_file = args['<input_file>']
    output_file_edges = args['<output_file_edges>']
    output_file_nodes = args['<output_file_nodes>']

    if input_file == output_file_edges or input_file == output_file_nodes:
        raise ValueError('input and output files cannot be the same')
    
    # Read the data from the input file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Create a list of nodes, and don't use 'topics' as a node
    # or 'affinities' as a node
    nodes = []
    for key, value in data.items():
        for k, v in value.items():
            if k not in ['topics', 'affinities']:
                nodes.append(k)

    # Remove duplicates from the list of nodes
    nodes = list(set(nodes))
    print('Number of nodes after removing duplicates: {}'.format(len(nodes)))

    # Create a list of edges
    edges = []
    for key, value in data.items():
        for k, v in value.items():
            if k not in ['topics', 'affinities']:
                edges.append((key, k, v))

    # Create a dataframe from the list of edges
    df = pd.DataFrame(edges, columns=['from', 'to', 'weight'])

    # Create a dataframe with the number of times each node
    #  appears as a source or target node
    df_nodes = pd.DataFrame(df.groupby('from').size(), columns=['influence'])
    # Concatenate: 
    df_nodes = pd.concat([df_nodes, pd.DataFrame(df.groupby('to').size(), columns=['influence'])])
    df_nodes = df_nodes.groupby(df_nodes.index).sum()

    # Create a list of dicts of nodes
    nodes = []
    for index, row in df_nodes.iterrows():
        nodes.append({'id': index, 'label': index, 'influence': row['influence']})

    # Create a sorted list of dicts of edges 
    edges = []
    for index, row in df.iterrows():
        edges.append({'from': row['from'], 'to': row['to'], 'weight': row['weight']})

    # Write the nodes and edges to files
    with open(output_file_nodes, 'w') as f:
        json.dump(nodes, f, indent=2, sort_keys=True, default=lambda o: o.tolist())
    with open(output_file_edges, 'w') as f:
        json.dump(edges, f, indent=2, sort_keys=True, default=lambda o: o.tolist())

    # Show some stats
    show_stats(nodes, edges)

if __name__ == '__main__':
    main()

# Path: create_graph.py