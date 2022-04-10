class Position:
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(x={self.x}, y={self.y})'

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @x.setter
    def x(self, val: float):
        self._x = val

    @y.setter
    def y(self, val: float):
        self._y = val
