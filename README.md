### Flavor Metrics/Gastronomical Map Project

Building a way to visualize The Flavor Bible, and develop flavor metrics to aid in recipe creation, menu development, and crop cycles.  

The primary purpose of this tool is to help chefs discover and experiment with 
flavor combinations where their mistakes are cheap.  This tool also has purpose 
in that looking at food through the flavor lense specifically, where cliques form 
and concepts converge, can help assist a wide range of users:
* *farmers* and *growers*
* *baristas* and *bartenders*
* *stores* and *distributers*
* *chefs* and *homecooks*
* *brewers* and *vitners*

0. [buy the ebook](https://karenandandrew.com/books/the-flavor-bible/) and read it

1. parse the epub files from the book into json format
``` bash
python ./parse_html.py
```
which generates `bible.json`.  The numbers in the json represent 
an integral distance rank of an ingredients importance to its 
source, and is based on the different typefaces used in the book.

We assume these html chapter files live in ./input/.

2. clean up the json, which outputs a better weighted `clean.json`
``` bash
python clean_data.py bible.json clean.json
```

3. compute the similarity matrix in the jaccard metric, which makes 
   a larger `similarity.json` 
``` bash
python compute_similarities.py clean.json similarity.json
```

4. create the network graph date:
``` bash
create_nodes_and_edges.py clean.json edges.json nodes.json
```

5. slice the graph:
``` bash
python slice_network.py -i nodes.json -e edges.json -n 'basil' -n 'garlic' -n 'olive oil'
```

6. visualize a similarity heatmap from a list of input ingredients
``` bash
python viz_heatmap.py -i similarity.json -o samples.txt -d 5 -n 'basil' -n 'garlic' -n 'olive oil'
```

7. visualize similarity graph (networkx) from a list of input 
ingredients[*]
``` bash
#python visualize_graph.py
```

[*] these are going to change, and we'll add some histograms to check
centrality
