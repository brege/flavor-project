import argparse
import pandas as pd
import numpy as np
import os.path


def main():
    parser = argparse.ArgumentParser(
        prog='heatmap.py',
        description='Generate a heatmap of ingredient similarities and suggest complementary ingredients',
        epilog='Example: python heatmap.py -i output/similarity.json -o heatmap.csv -d 5 -n garlic -n basil -n "olive oil"'
    )

    parser.add_argument(
        '-i', '--input',
        default='output/similarity.json',
        metavar='FILE',
        help='input similarity matrix (default: output/similarity.json)'
    )
    parser.add_argument(
        '-o', '--output',
        default='output/heatmap.csv',
        metavar='FILE',
        help='output heatmap CSV (default: output/heatmap.csv)'
    )
    parser.add_argument(
        '-d', '--depth',
        type=int,
        default=5,
        metavar='N',
        help='number of suggestions (default: 5)'
    )
    parser.add_argument(
        '-n', '--ingredients',
        action='append',
        dest='ingredients',
        metavar='INGREDIENT',
        help='seed ingredient (can specify multiple times)'
    )

    args = parser.parse_args()

    # check the input file exists
    if not os.path.isfile(args.input):
        parser.error(f'input file does not exist: {args.input}')

    # set defaults for ingredients if not provided
    if args.ingredients is None:
        ingredients = ['garlic', 'basil', 'olive oil']
    else:
        ingredients = args.ingredients

    input_file = args.input
    output_file = args.output
    depth = args.depth

    # read the input file
    sim_matrix = pd.read_json(input_file)
    print(sim_matrix)

    # now we sort the similarity matrix by the ingredients
    # and then get the top depth=n ingredients
    suggested_ingredients = []
    for i in range(depth):
        # get the top n ingredients
        top_n = sim_matrix[ingredients].mean(axis=1).sort_values(ascending=False)
        top_n = top_n.drop(ingredients)
        suggested_ingredients.append(top_n.index.values[0])
        ingredients.append(top_n.index.values[0])

    print(suggested_ingredients)
    print(ingredients)
    # append the input ingredients to the suggested ingredients

    # print the suggested ingredients as a slice of the
    # similarity matrix, in both columns and rows
    suggested_sim_matrix = sim_matrix[ingredients]
    suggested_sim_matrix = suggested_sim_matrix.loc[ingredients]
    # sort the suggested ingredients as an adjacency matrix:
    suggested_sim_matrix = suggested_sim_matrix.sort_index(axis=0)
    suggested_sim_matrix = suggested_sim_matrix.sort_index(axis=1)
    print(suggested_sim_matrix)

    """plotting"""
    import seaborn as sns
    import matplotlib.pyplot as plt
    sns.set()
    sns.set_style("ticks")
    sns.set_palette("viridis")
    plt.figure(figsize=(10,10))
    #use a log scale
    sns.heatmap(suggested_sim_matrix, cmap='viridis', annot=True, fmt='.3f', cbar=False, square=True, mask=np.eye(len(suggested_sim_matrix), dtype=bool))
    plt.savefig('heatmap.png', dpi=300)

    # print this to the output file in csv format,
    # and make sure entries are rounded to 3 decimal places
    suggested_sim_matrix.to_csv(output_file, float_format='%.3f')

if __name__ == '__main__':
    main()