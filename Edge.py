from abc import ABC
from numbers import Number



class Edge:
    def __init__(self, name, cost_per_meter, length=0):
        if not isinstance(name, str):
            raise TypeError(f"Material name must be of type str. Was type {type(name)}")
        if not (isinstance(cost_per_meter, Number) or (isinstance(cost_per_meter, str) and cost_per_meter.isnumeric())):
            raise TypeError(f"Cost must be numerical. Was type {type(cost_per_meter)}")
        elif cost_per_meter < 0:
            raise ValueError(f"Cost per meter of material must be positive. Value was {cost_per_meter}")

        self.name = name
        self.cost_per_meter = float(cost_per_meter)
        self.length = length

    def __repr__(self):
        return f"{self.name}, {self.cost_per_meter}, {self.length}"


    def get_total_cost(self):
        return self.length * self.cost_per_meter


# class Edge(ABC):
#     def __init__(self, material, length):
#         if not isinstance(material, Material):
#             raise TypeError(f"Material must be of type Material. Was type {type(material)}")
#         if not (isinstance(length, Number) or (isinstance(length, str) and length.isnumeric())):
#             raise TypeError(f"Length must be numerical. Was type {type(length)}")
#         elif length < 0:
#             raise ValueError(f"Length of edge must be positive. Value was {length}")
#         self.material = material
#         self.length = float(length)
#
#     def cost(self) -> float:
#         return self.material.cost_per_meter * self.length
