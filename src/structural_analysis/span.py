import math

from . import Node


class Span:
    # TODO check loads again
    def __init__(self, node1: Node, node2: Node, loads=[]):
        self._node1: Node = node1
        self._node2: Node = node2
        self._loads = loads

    def __len__(self) -> int:
        return int(
            math.sqrt(
                (self.node1.x - self.node2.x) ** 2 + (self.node1.y - self.node2.y) ** 2
            )
        )

    @property
    def node1(self) -> Node:
        return self._node1

    @property
    def node2(self) -> Node:
        return self._node2

    @property
    def is_overhang(self) -> bool:
        return self._node2 is None

    def area(self) -> float:
        pass

    def span_rigidity(self):
        pass

    def type_of_loads(self):
        pass

    def bending_moment_diagram(self):
        pass

    def shear_force_diagram(self):
        pass


if __name__ == "__main__":
    s = Span(Node(x=14, y=0), Node(x=12, y=0))
    print(len(s))
