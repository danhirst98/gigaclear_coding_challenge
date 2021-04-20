from numbers import Number


class Node:
    """
    This class stores the node type, cost, and number of this node within a graph
    """
    def __init__(self, node_type, cost, count=0):
        if not isinstance(node_type, str):
            raise TypeError(f"Node type name must be of type str. Was type {type(node_type)}")
        if not isinstance(cost, Number) and not (isinstance(cost, str) and cost.isnumeric()):
            raise TypeError(f"Cost must be numerical. Was type {type(cost)}")
        elif cost < 0:
            raise ValueError(f"Cost of node must be positive. Value was {cost}")

        self.type = node_type
        self.cost = float(cost)
        self.count = count

    def __repr__(self):
        return f"node type: {self.type}, cost: £{self.cost}, number of occurrences: {self.count}"

    def get_total_cost(self):
        return self.cost * self.count


