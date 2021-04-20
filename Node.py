from numbers import Number


class Node:
    def __init__(self, node_type, cost, number=0):
        if not isinstance(node_type, str):
            raise TypeError(f"Node type name must be of type str. Was type {type(node_type)}")
        if not isinstance(cost, Number) and not (isinstance(cost, str) and cost.isnumeric()):
            raise TypeError(f"Cost must be numerical. Was type {type(cost)}")
        elif cost < 0:
            raise ValueError(f"Cost of node must be positive. Value was {cost}")

        self.type = node_type
        self.cost = float(cost)
        self.number = number

    def __repr__(self):
        return f"{self.type}, {self.cost}, {self.number}"

    def add_number(self, number=1):
        self.number += number

    def get_total_cost(self):
        return self.cost * self.number


