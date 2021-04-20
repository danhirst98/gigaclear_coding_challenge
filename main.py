from networkx import read_graphml
from rate_card import generate_rate_card
import argparse


def main(rate_card_path, graph_path) -> float:
    """
    Calculates total cost of graph based on a graphml file and a rate card csv

    :param rate_card_path: path to rate card csv
    :type rate_card_path: str, Path
    :param graph_path: path to graphml file
    :type graph_path: str, Path
    :return: total cost of all infrastructure in graph
    :rtype: float
    """
    # Initialise total cost
    total_cost = 0

    # read graphml file into networkx graph
    with open(graph_path) as file:
        graph = read_graphml(file)

    # generate rate_card and minimum distances between nodes
    rate_card, min_weights = generate_rate_card(rate_card_path, graph)

    # iterate through all nodes
    for node_name, node_type in graph.nodes(data="type"):
        # find cost structure from rate card
        cost = rate_card[node_type.lower()]
        # if cost is a flat rate, add it to total cost
        if cost.isnumeric():
            total_cost += float(cost)
        # if cost is based on minimum distance between node and another node of certain type (e.g. cabinet)
        # lookup minimum distance from min_weights and calculate cost
        elif 'x' in cost:
            multiplier, source = cost.split('x')
            total_cost += float(multiplier) * min_weights[source.lower()][node_name]
        else:
            raise NotImplementedError("")

    # iterate through edges
    for edge in graph.edges(data=True):
        # get material and length from graph data
        material = edge[2]['material']
        length = float(edge[2]['length'])
        # add cost to material based on multiplier * length
        total_cost += float(rate_card[material]) * length

    return total_cost


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This program takes a given graph and rate card and calculates the "
                                                 "total cost of the network")
    parser.add_argument("-r", "--rate_card", help="path to rate card csv", required=True)
    parser.add_argument("-g", "--graph", help="path to graph .graphml file", required=True)

    args = parser.parse_args()
    rate_card_path_arg = args.rate_card
    graph_path_arg = args.graph

    if not graph_path_arg:
        raise ValueError("Must provide path to graph .graphml file")
    if not rate_card_path_arg:
        raise ValueError("Must provide path to rate card .csv file")
    # check that rate_card is a csv
    if not rate_card_path_arg.endswith('.csv'):
        raise TypeError("Rate Card must be a csv file")

    # check that graph is a .graphml file
    if not graph_path_arg.endswith('.graphml'):
        raise TypeError("Graph must be a .graphml file")

    print(main(rate_card_path_arg, graph_path_arg))
