import csv
import re
from networkx import multi_source_dijkstra_path_length


def get_nodes(graph, node_type) -> list:
    """
    Returns list of node names that are of node type

    :param graph: weighted graph we are looking at
    :type graph: networkx.Graph
    :param node_type: node type we are looking for
    :type node_type: str
    :return: list of node names that are of type node_type
    :rtype: list
    """
    return [x for x, y in graph.nodes(data=True) if y['type'].lower() == node_type]


def generate_rate_card(rate_card_csv_path, graph) -> tuple:
    """
    Convert rate card csv into hash table that gives the costs of different infrastructure types. For variable cost
    structures, returns a min_weights dict that gives the minimum distances between certain infrastructure types to
    all other nodes

    :param rate_card_csv_path: path to rate card csv file
    :type rate_card_csv_path: str, Path
    :param graph: full graph of nodes and edges
    :type graph: networkx.Graph
    :return: rate_card, min_weights
    :rtype: tuple
    """
    # initialise rate_card and min_weights hash tables
    rate_card = {}
    min_weights = {}
    # open rate card
    with open(rate_card_csv_path) as csvfile:
        rate_card_csv = csv.reader(csvfile, delimiter=',')
        # skip header of file
        next(rate_card_csv, None)
        # iterate through rate card items
        for item, cost in rate_card_csv:
            # strip whitespace from cost
            cost = cost.strip()
            # check if cost is based on multiplier
            if 'x' in cost:
                # find the source to find the min distance from
                _, source = cost.split('x')
                # use djikstras algorithm to find minimum weights between nodes of type source and all other nodes
                # save in hash table for fast look up and so we don't have to calculate again
                source = source.lower()
                if source not in min_weights.keys():
                    min_weights[source] = multi_source_dijkstra_path_length(graph,
                                                                            get_nodes(graph, source),
                                                                            weight='length')

            # raise error if cost is not a number
            elif not cost.isnumeric():
                raise NotImplementedError(f"Rate card gave a cost in an unknown format. Must be a number or a string "
                                          f"in the form<number>x<node_type>. Given cost was: {cost}")
            # find the name of item (the text inside the parentheses if an edge, otherwise just the item)
            name = re.findall(r'\((.*?)\)', item)[0].lower() if "/m" in item else item.lower()
            # add item to rate card
            rate_card[name] = cost

    return rate_card, min_weights
