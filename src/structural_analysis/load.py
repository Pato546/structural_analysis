import math

import attrs


@attrs.define(slots=True)
class PointLoad:
    magnitude: int or float = attrs.field(
        default=0.0, validator=attrs.validators.instance_of((int, float))
    )
    x: int or float = attrs.field(init=False, validator=attrs.validators.ge(0))
    y: int or float = attrs.field(init=False, validator=attrs.validators.ge(0))
    angle_of_inclination: float = attrs.field(
        default=90.0,
        validator=attrs.validators.instance_of(float),
        converter=math.radians,
        repr=False
    )
    horizontal_force: int or float = attrs.field(
        init=False,
        validator=attrs.validators.instance_of((int, float)),
        repr=False
    )
    vertical_force: int or float = attrs.field(
        init=False,
        validator=attrs.validators.instance_of((int, float)),
        repr=False
    )

    @horizontal_force.default
    def h(self):
        return (
            0.0
            if math.isclose(
                round(self.magnitude * math.cos(self.angle_of_inclination), 4), 0
            )
            else round(self.magnitude * math.cos(self.angle_of_inclination))
        )

    @vertical_force.default
    def v(self):
        return round(self.magnitude * math.sin(self.angle_of_inclination), 4)


@attrs.define(slots=True, order=True)
class UniformlyDistributedLoad:
    magnitude: int or float = attrs.field(
        validator=attrs.validators.instance_of((int, float)), order=abs
    )
    length: int or float = attrs.field(validator=attrs.validators.ge(0), order=False)
    start: int or float = attrs.field(
        init=False, validator=attrs.validators.ge(0), order=False
    )

    def centroid_of_udl(self) -> float:
        return self.length / 2

    def total_force_of_udl(self) -> float:
        return self.magnitude * self.length


class TriangularLoad:
    pass


class TrapezoidalLoad:
    pass


# @functools.total_ordering
@attrs.define(slots=True, order=True)
class PointMoment:
    magnitude: int or float = attrs.field(
        validator=attrs.validators.instance_of((int, float)), order=abs
    )
    x: int or float = attrs.field(
        init=False, validator=attrs.validators.ge(0), order=False
    )
    y: int or float = attrs.field(
        init=False, validator=attrs.validators.ge(0), order=False
    )


if __name__ == "__main__":
    # pl1 = PointLoad(-90)
    # pl2 = PointLoad(-90)
    # print(pl1 >= pl2)
    # m1 = UniformlyDistributedLoad(-50, 4)
    # m2 = UniformlyDistributedLoad(100, 2)
    # print(m1 > m2)
    pm1 = PointMoment(40)
    pm2 = PointMoment(-50)
    print(pm1 < pm2)
