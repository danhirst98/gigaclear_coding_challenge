# Gigaclear Technical Challenge

This is my (Dan Hirst) submission for the Gigaclear technical challenge. This program calculates the total cost of a network given a graph of the infrastructure and a rate card showing the costs of each infrastructure type.

## Quick Start

The only required package is networkx==2.4.


To calculate the cost of a network in the file problem.graphml using a rate card in the file rate_card_a.csv, simply run:

```python main.py -g problem.graphml -r rate_card_a.csv```

## Installation

The only external package required for this program is [networkx](https://pypi.org/project/networkx/#history). You can install it directly or by cloning this repository and running 
```pip install -r requirements.txt```

*Note*: Currently, there is a [bug in networkx](https://github.com/networkx/networkx/issues/4188) that means it does not support the attribute type long from version 2.5. This attribute type is in the provided graph (problem.graphml). To fix this, either install networkx==2.4 (which is automatically done when installing from requirements.txt) or swap any `long` for `int`.

## Running the Program

There are two required arguments to run the program:
* `-g`/`--graph` - the path to the input graph. Must be a .graphml file
* `-r`/`--rate_card` - the path to the rate card. Must be a .csv file

You can therefore run the program as such:

```python main.py -g <graphml> -r <rate_card>```

## Rate Card CSV

There was no standardised format for inputting rate cards, so I created a basic file that the program reads as a rate card. The file is a comma-delimited csv with 2 columns - 'item' and 'cost'. The column names are provided on the first row. 

Below the column titles are the infrastructure types and their associated cost. The item field is just the name of the infrastructure type. I determined that any item with a per meter ("/m") snippet is an edge, and any other items are nodes. 

There are two possible types of cost structures. A flat rate is when you provide only a number in the cost field. In this case, each node will cost this flat rate and each edge will cost this flat rate for each meter in length. 
A variable rate is when the cost of the item is dependent on the distance between the item and another node type (e.g. 20 x trench length (in meters) from Cabinet). This can be inputted as `<cost-multiplier>x<node-type>` in the cost field. For the given example, the cost field will be `20xCabinet`. 

The two rate cards given as part of the problem are provided as `rate_card_a.csv` and `rate_card_b.csv`.

## Features

The program allows the user to calculate cost when  the cost of an item is dependent on the distance to a cabinet and there are multiple cabinets in the graph. In this event, it will find the distance to the nearest cabinet and calculate the cost accordingly.

Furthermore, the user can change the node type that affects the cost of a node. For example, you can calculate the cost of a Pot based on the distance to the nearest Chamber. To do this, simply input `<cost-multiplier>x<node-type>` (e.g. `20xChamber`) in the cost field of the rate card csv.

Finally, the program supports any additional infrastructure types. The code will allow for a new node type to be added to the network and rate card files and will calculate the cost accordingly.

## Improvements

With more time I would swap over all functions using networkx to use networkit. Unlike networkx which is written in Python, networkit is written in C and has [significant speed advantages](https://www.timlrx.com/blog/benchmark-of-popular-graph-network-packages).

Additionally, I would change the delimiter for the variable rate away from `x`. Currently, the code breaks if the node type has an x in its name.

I also would add functionality to read from .dot files. 

