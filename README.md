Demo for History-Tree Calculation and Visualizaion for IBM ALM Rtc Component-Baselines. 

# Quick-start

Run the run_demo.bat script.
This will:

- setup & activate a venv with pythin 3.14 using py.exe
- install the python modules from requirements.txt via pip
- execute the main.py for the component "MyComponent"
- starts a simple python http server on port 8080 rendering the index.html

# Overview

## main.py

Orchestation to call functions of the other modules to:

1. get baseline and changeset data from ALM Rtc (with local caching)
2. calculate config nodes and edges from the baselines about the contained changesets as config nodes and edges
3. remove transitive edges
4. calculate predecessor nodes
5. compute the mainline (longest path of nodes)
6. export the graph as json

Parameters:

1. --component: ALM Rtc component name (mandatory)
2. --output: json file name (optional, default: "baseline_history.json")

## lscm_utils.py

Helper functions to download json files of baselines and changesets from ALM Rtc via lscm tool.
Downloaded files are cached in folder "cache".

The changesets are downloaded in yearly postions to cope better with huge amount of changesets.

The "cache" folder is already pre-populated with sample data for testing generated via generate_samples.py.

## config_nodes.py

Helper to build an internal config node data-structures from the sorted list of the changesets for each baselines.
The sorting of the changesets handles merges (delivers/accepts) of older changesets into a stream which contains already newer changesets to ensure other baselines with an exact sub-set of these changesets are can be detected as predecessors.
Multiple baselines with the exact same set of changesets are merged into the same node.
Each nodes gets an unique id calculated as sha1 hash over the changeset ids it relates to.

## dag_utils.py

Helper to build DAG (Directed Acyclic Graph) between the config nodes.
A node is a predecessor of an other node if it contains an exact sub-set of (sorted) changesets.

Postprocessing steps:

1. transitive edges are removed
2. config nodes get a list of predecesors (in case of "merges" there can be multiple predecessors)
3. compute mainline (longest path)

## export_graph.py

Helper to write the config nodes to a single json file.

## generate_samples.py

Helper to generate some sample/test json inputs in the "cache" folder.
This is only for testing/demonstration. In the productive workflow the data is fetched via lscm_utils.py only.

## index.html

HTML file with an embedded dynamically gernated graphical representaion of the exported config nodes json file.
The d3 library is used to generate a zoom- and pan-able svg.

To view this correctly in a webbrowser a small http server is necessary e.g. via command:

    python -m http.server 8080

