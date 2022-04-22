import math
import functools


# TODO Write the codes for comparing loads using total ordering


class PointLoad:
    def __init__(
            self,
            magnitude: float,
            x: float or None = None,
            y: float or None = None,
            angle_of_inclination: float = 90.0,
    ) -> None:
        self._magnitude = magnitude
        self._x = x
        self._y = y
        self._angle_of_inclination = angle_of_inclination

    def __repr__(self):
        return f"{self.__class__.__name__}(magnitude={self.magnitude}, x={self.x}, y={self.y})"

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

    @x.setter
    def x(self, val):
        self._x = val

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, val):
        self._y = val

    def horizontal_force(self) -> float:
        load_magnitude: float = self.magnitude * self._horizontal_component

        return (
            0
            if math.isclose(0.0, load_magnitude, rel_tol=0.001, abs_tol=0.001)
            else load_magnitude
        )

    def vertical_force(self) -> float:
        return self.magnitude * self._vertical_component


class UniformlyDistributedLoad:
    def __init__(self, magnitude: float, length: float, start: float or None = None):
        self._magnitude = magnitude
        self._length = length
        self._start = start

    def __repr__(self):
        return f"{self.__class__.__name__}({self.magnitude})"

    def __str__(self) -> str:
        return self.__class__.__name__

    def __len__(self):
        return self._length

    @property
    def magnitude(self) -> float:
        return self._magnitude

    @property
    def start(self) -> float:
        return self.start

    @start.setter
    def start(self, val):
        self._start = val

    def centroid_of_udl(self) -> float:
        return len(self) / 2

    def total_force_of_udl(self) -> float:
        return self.magnitude * len(self)


class PointMoment:
    def __init__(self, magnitude: float, x: float or None = None, y: float or None = None):
        self._magnitude = magnitude
        self._x = x
        self._y = y

    def __repr__(self):
        return f"{self.__class__.__name__}(magnitude={self.magnitude}, x={self.x}, y={self.y})"

    @property
    def magnitude(self):
        return self._magnitude

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        self._y = val


if __name__ == "__main__":
    pm = PointMoment(-40, 9, 0)
    print(pm)
