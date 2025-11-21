import argparse
import json
import sys
import os

def main():
    parser = argparse.ArgumentParser(
        prog='slice.py',
        description='Extract a subgraph from a network graph based on seed nodes',
        epilog='Example: python slice.py -i nodes.json -e edges.json -n garlic -n basil -n "olive oil"'
    )

    parser.add_argument(
        '-i', '--nodes',
        default='output/nodes.json',
        metavar='FILE',
        help='input nodes (default: output/nodes.json)'
    )
    parser.add_argument(
        '-e', '--edges',
        default='output/edges.json',
        metavar='FILE',
        help='input edges (default: output/edges.json)'
    )
    parser.add_argument(
        '-n', '--node',
        action='append',
        dest='nodes_to_slice',
        metavar='NODE',
        required=True,
        help='seed node (can specify multiple times)'
    )

    args = parser.parse_args()

    input_nodes_file = args.nodes
    input_edges_file = args.edges
    nodes = args.nodes_to_slice

    # check the input files exist
    if not os.path.isfile(input_nodes_file):
        parser.error(f'nodes file does not exist: {input_nodes_file}')
    if not os.path.isfile(input_edges_file):
        parser.error(f'edges file does not exist: {input_edges_file}')

    # create the output files
    output_nodes_file = input_nodes_file.replace('.json', '_sliced.json')
    output_edges_file = input_edges_file.replace('.json', '_sliced.json')
  
    # read the input files
    with open(input_nodes_file, 'r') as f:
        input_nodes = json.load(f)
    with open(input_edges_file, 'r') as f:
        input_edges = json.load(f)

    # find every edge that has a node matching an input node
    sliced_nodes = []
    sliced_edges = []
    for edge in input_edges:
        if edge['from'] in nodes or edge['to'] in nodes:
            sliced_edges.append(edge)
            if edge['from'] not in sliced_nodes:
                sliced_nodes.append(edge['from'])
            if edge['to'] not in sliced_nodes:
                sliced_nodes.append(edge['to'])

    # add the node attributes to the sliced nodes
    for node in input_nodes:
        if node['id'] in sliced_nodes:
            sliced_nodes[sliced_nodes.index(node['id'])] = node

    print('\nFrom nodes: {}\n'.format(nodes))
    print('Sliced nodes: {}'.format(len(sliced_nodes)))
    print('Sliced edges: {}'.format(len(sliced_edges)))
    print('')
    print('As you can see, the number of nodes and edges is still')
    print('quite large.  This is why we need to use the Jaccard')
    print('similarity to reduce the number of nodes.')
    print('')
    print('The next step is to run `similarity.py`')
    print('to reduce the number of nodes.')
    print('')

    # graph the output files
    #print('Graphing the output files')
    #os.system('python <graph.py> -n {} -e {}'.format(<output_nodes_file>, <output_edges_file>))

    # write the output files
    with open(output_nodes_file, 'w') as f:
        json.dump(sliced_nodes, f, indent=2)
    with open(output_edges_file, 'w') as f:
        json.dump(sliced_edges, f, indent=2)


if __name__ == '__main__':
    main()
