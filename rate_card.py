from Edge import Edge
from Node import Node
import csv
import re
from networkx import multi_source_dijkstra_path_length


def get_item_type(item):
    return Edge if "/m" in item else Node



def get_nodes(graph, node_type):
    return [x for x, y in graph.nodes(data=True) if y['type'].lower() == node_type]


def generate_rate_card(rate_card_csv_path, graph) -> tuple:
    rate_card = {}
    min_weights = {}
    with open(rate_card_csv_path) as csvfile:
        rate_card_csv = csv.reader(csvfile, delimiter=',')
        next(rate_card_csv, None)  # skip header of file
        for item, cost in rate_card_csv:
            print(cost)
            if cost.strip().isnumeric():
                cost = float(cost)
            elif 'x' in cost:
                cost = cost
                _, source = cost.split('x')
                min_weights[source] = multi_source_dijkstra_path_length(graph, get_nodes(graph, source), weight='length')
            else:
                raise NotImplementedError("")
            name = re.findall(r'\((.*?)\)', item)[0].lower() if "/m" in item else item.lower()
            rate_card[name] = cost

    return rate_card, min_weights

# def generate_rate_card(rate_card_csv_path) -> dict:
#     rate_card = {}
#     with open(rate_card_csv_path) as csvfile:
#         rate_card_csv = csv.reader(csvfile, delimiter=',')
#         next(rate_card_csv, None)  # skip header of file
#         for item, cost in rate_card_csv:
#             cost = float(cost)
#             if "/m" in item:
#                 name = re.findall(r'\((.*?)\)', item)[0].lower()
#                 rate_card[name] = Edge(name=name, cost_per_meter=cost)
#             else:
#                 node_type = item.lower()
#                 rate_card[node_type] = Node(node_type=node_type, cost=cost)
#     return rate_card


if __name__ == '__main__':
    print(generate_rate_card("rate_card_a.csv"))
