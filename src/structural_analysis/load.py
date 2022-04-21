import math


class PointLoad:
    def __init__(
        self, magnitude: float, x: float, y: float, angle_of_inclination: float = 90
    ) -> None:
        self._magnitude = magnitude
        self._x = x
        self._y = y
        self._angle_of_inclination = angle_of_inclination

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(magnitude={self.magnitude}, {repr(self.position)})"

    def __str__(self) -> str:
        return self.__class__.__name__

    @property
    def _angle(self) -> float:
        # converts the angle of inclination from degrees to radians
        return (self._angle_of_inclination / 180) * math.pi

    @property
    def _horizontal_component(self) -> float:
        return math.cos(self._angle)

    @property
    def _vertical_component(self) -> float:
        return math.sin(self._angle)

    @property
    def magnitude(self) -> float:
        return self._magnitude

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def horizontal_force(self) -> float:
        load_magnitude: float = self.magnitude * self._horizontal_component

        return (
            0
            if math.isclose(0.0, load_magnitude, rel_tol=0.001, abs_tol=0.001)
            else load_magnitude
        )

    def vertical_force(self) -> float:
        return self.magnitude * self._vertical_component


class UDL:
    def __init__(self, magnitude: float, x1: float, y1: float, x2: float, y2: float):
        self._magnitude = magnitude
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(magnitude={self.magnitude}"

    def __str__(self) -> str:
        return self.__class__.__name__

    @property
    def magnitude(self) -> float:
        return self._magnitude

    @property
    def x1(self) -> float:
        return self._x1

    @property
    def y1(self) -> float:
        return self._y1

    @property
    def x2(self) -> float:
        return self._x2

    @property
    def y2(self) -> float:
        return self._y2


if __name__ == "__main__":
    a = PointLoad(100, Position(0, 4))
    b = UDL(100, Position(3, 4), Position(4, 4))
    print(str(b))
