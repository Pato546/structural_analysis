from . import Position


class Node:
    def __init__(self, position: Position):
        self._position = position

    @property
    def position(self):
        return self._position


if __name__ == "__main__":
    n = Node(x=0, y=0)
    print(n.is_origin)
