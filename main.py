from networkx import read_graphml
from rate_card import generate_rate_card
from numbers import Number
import argparse


def main(rate_card_path, graph_path):
    total_cost = 0
    rate_card, min_weights = generate_rate_card(rate_card_path)
    with open(graph_path) as file:
        graph = read_graphml(file)
    print()

    for node_name, node_type in graph.nodes(data="type"):
        cost = rate_card[node_type]
        if isinstance(cost, Number):
            total_cost += cost
        elif isinstance(cost, str):
            multiplier, source = cost.split('x')
            total_cost += multiplier * min_weights[source][node_name]

    for edge in graph.edges(data=True):
        material = edge[2]['material']
        length = float(edge[2]['length'])
        total_cost += rate_card[material] * length

    total_cost = sum(map(lambda x: x.get_total_cost(), rate_card.values()))
    return total_cost


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This program takes a given graph and rate card and calculates the total cost of the network")
    parser.add_argument("-r", "--rate_card", help="path to rate card csv")
    parser.add_argument("-g", "--graph", help="path to graph file")

    args = parser.parse_args()
    rate_card_path = args.rate_card
    graph_path = args.graph

    if not rate_card_path.endswith('.csv'):
        raise TypeError("Rate Card must be a csv file")

    if not graph_path.endswith('.graphml'):
        raise TypeError("Graph must be a .graphml file")

    print(main(rate_card_path, graph_path))
