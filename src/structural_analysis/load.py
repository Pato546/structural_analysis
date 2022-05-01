import math
import functools


@functools.total_ordering
class PointLoad:
    def __init__(
            self,
            magnitude: float or None = None,
            x: float or None = None,
            y: float or None = None,
            angle_of_inclination: float = 90.0,
    ) -> None:
        self._angle_of_inclination = angle_of_inclination

        if x:
            if x < 0:
                raise ValueError("x cannot be less than zero")
        if y:
            if y < 0:
                raise ValueError("y cannot be less than zero")

        self._x = x
        self._y = y

        if magnitude:
            self._horizontal_force: float = round(
                magnitude * self._horizontal_component, 4
            )
            self._vertical_force: float = round(magnitude * self._vertical_component)
        else:
            self._horizontal_force = None
            self._vertical_force = None

    def __repr__(self):
        return f"{self.__class__.__name__}(vertical_force={self.vertical_force}, horizontal_force={self.horizontal_force})"

    def __str__(self) -> str:
        return self.__class__.__name__

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (abs(self.vertical_force), abs(self.horizontal_force)) == (
                abs(other.vertical_force),
                abs(other.horizontal_force),
            )
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return (abs(self.vertical_force), abs(self.horizontal_force)) < (
                abs(other.vertical_force),
                abs(other.horizontal_force),
            )
        return NotImplemented

    def __add__(self, other):
        if isinstance(self, self.__class__):
            vertical_force = self.vertical_force + other.vertical_force
            horizontal_force = self.horizontal_force + other.horizontal_force
            cls = self.__class__()
            cls.vertical_force = vertical_force
            cls.horizontal_force = horizontal_force
            return cls

        return NotImplemented

    def __sub__(self, other):
        if isinstance(self, self.__class__):
            vertical_force = self.vertical_force - other.vertical_force
            horizontal_force = self.horizontal_force - other.horizontal_force
            cls = self.__class__()
            cls.vertical_force = vertical_force
            cls.horizontal_force = horizontal_force
            return cls

        return NotImplemented

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
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, val):
        if val < 0:
            raise ValueError("x cannot be less than zero")
        self._x = val

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, val):
        if val < 0:
            raise ValueError("y cannot be less than zero")
        self._y = val

    @property
    def horizontal_force(self) -> float:
        return self._horizontal_force

    @horizontal_force.setter
    def horizontal_force(self, val) -> None:
        if isinstance(val, (int, float)):
            self._horizontal_force = val
        else:
            raise ValueError("horizontal_force must be a number")

    @property
    def vertical_force(self) -> float:
        return self._vertical_force

    @vertical_force.setter
    def vertical_force(self, val):
        if isinstance(val, (int, float)):
            self._vertical_force = val
        else:
            raise ValueError("vertical_force must be a number")


@functools.total_ordering
class UniformlyDistributedLoad:
    def __init__(self, magnitude: float, length: float or None = None, start: float or None = None):
        self._magnitude = magnitude

        if length < 0:
            raise ValueError("length cannot be less than zero")
        self._length = length

        if start:
            if start < 0:
                raise ValueError("start cannot be less than zero")

        self._start = start

    def __repr__(self):
        return f"{self.__class__.__name__}(magnitude={self.magnitude}, start={self.start}, L={self._length})"

    def __str__(self) -> str:
        return self.__class__.__name__

    def __len__(self):
        return self._length

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return abs(self.total_force_of_udl()) == abs(other.total_force_of_udl())
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return abs(self.total_force_of_udl()) < abs(other.total_force_of_udl())
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(magnitude=self.magnitude + other.magnitude)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(magnitude=self.magnitude - other.magnitude)
        return NotImplemented

    @property
    def magnitude(self) -> float:
        return self._magnitude

    @property
    def start(self) -> float:
        return self._start

    @start.setter
    def start(self, val):
        if val < 0:
            raise ValueError("start cannot be less than zero")
        self._start = val

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, val):
        if val < 0:
            raise ValueError("length cannot be less than zero")
        self._length = val

    def centroid_of_udl(self) -> float:
        return len(self) / 2

    def total_force_of_udl(self) -> float:
        return self.magnitude * len(self)


@functools.total_ordering
class PointMoment:
    def __init__(
            self, magnitude: float, x: float or None = None, y: float or None = None
    ):
        self._magnitude = magnitude

        if x:
            if x < 0:
                raise ValueError("x cannot be less than zero")
        if y:
            if y < 0:
                raise ValueError("y cannot be less than zero")

        self._x = x
        self._y = y

    def __repr__(self):
        return f"{self.__class__.__name__}(magnitude={self.magnitude}, x={self.x}, y={self.y})"

    def __str__(self):
        return self.__class__.__name__

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return abs(self.magnitude) == abs(other.magnitude)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return abs(self.magnitude) < abs(other.magnitude)
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(magnitude=self.magnitude + other.magnitude)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(magnitude=self.magnitude - other.magnitude)
        return NotImplemented

    @property
    def magnitude(self):
        return self._magnitude

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        if val < 0:
            raise ValueError("val cannot be less than zero")
        self._x = val

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        if val < 0:
            raise ValueError("val cannot be less than zero")
        self._y = val


if __name__ == "__main__":
    # pl1 = PointLoad(-90)
    # pl2 = PointLoad(-90)
    # print(pl1 >= pl2)
    # m1 = UniformlyDistributedLoad(-50, 4)
    # m2 = UniformlyDistributedLoad(100, 2)
    # print(m1 > m2)
    pm1 = PointMoment(-40)
    pm2 = PointMoment(-50)
    print(pm1 > pm2)
