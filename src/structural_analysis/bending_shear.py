from sympy import sympify, Derivative
from sympy.core.numbers import Float, Integer
import attrs

from . import (
    HingeSupport,
    RollerSupport,
    PointMoment,
    UniformlyDistributedLoad,
    PointLoad,
)


class NotSolvedError(Exception):
    pass


@attrs.define(slots=True)
class ULoad:
    magnitude: int or float = attrs.field(validator=attrs.validators.instance_of((int, float)))
    type: str = attrs.field(validator=attrs.validators.instance_of(UniformlyDistributedLoad))
    length: list = attrs.field(factory=list)


@attrs.define()
class Load:
    magnitude: int or float = attrs.field(validator=attrs.validators.instance_of((int, float)))
    length: int or float = attrs.field(validator=attrs.validators.instance_of((int, float)))
    type = attrs.field()


@attrs.define(frozen=True, slots=True)
class Boundary:
    lower_bound: int or float = attrs.field(
        validator=attrs.validators.instance_of((int, float))
    )
    upper_bound: int or float = attrs.field(
        validator=attrs.validators.instance_of((int, float))
    )


@attrs.define(frozen=True, slots=True)
class Equation:
    eqn: str = attrs.field()
    boundary: Boundary = attrs.field(validator=attrs.validators.instance_of(Boundary))


@attrs.define(frozen=True, slots=True)
class Result:
    lower_bound: int or float = attrs.field(
        validator=attrs.validators.instance_of((int, float))
    )
    upper_bound: int or float = attrs.field(
        validator=attrs.validators.instance_of((int, float))
    )
    lower_bound_val: Integer or Float = attrs.field(
        validator=attrs.validators.instance_of((Integer, Float))
    )
    upper_bound_val: Integer or Float = attrs.field(
        validator=attrs.validators.instance_of((Integer, Float))
    )
    eqn: str = attrs.field()


class BendingShearCalculator:
    def __init__(self, beam):
        self.beam = beam
        self._bending_moments_equations = []
        self._shear_force_equations = []
        self.cache: list = []
        self.points = []
        self.solved = False

    @property
    def bending_moments_equations(self) -> list:
        if self.solved:
            return self._bending_moments_equations
        raise NotSolvedError("Bending and Shear has not been calculated yet")

    @property
    def shear_force_equations(self) -> list:
        if self.solved:
            return self._shear_force_equations
        raise NotSolvedError("Bending and Shear has not been calculated yet")

    def _calculate_bending_and_shear(self):
        lower_bound: int = 0

        for node in self.beam:
            eqn: str = ""
            x_coordinate_of_node = node.x
            try:
                x_coordinate_of_next_node = node.next_.x
            except AttributeError:
                break
            upper_bound: int = x_coordinate_of_next_node - x_coordinate_of_node

            for load in self.cache:
                if isinstance(load.type, UniformlyDistributedLoad):
                    if len(load.length) > 1:
                        eqn += f" + {load.magnitude * load.length[0]} * ({load.length[0] / 2} + {sum(load.length[1:])} + x)"
                        load.length.append(upper_bound)
                    else:
                        eqn += f" + {load.magnitude * load.length[0]} * ({load.length[0] / 2} + x)"
                        load.length.append(upper_bound)

                elif isinstance(load.type, PointMoment):
                    eqn += f" + {load.magnitude}"

                else:
                    eqn += f" + {load.magnitude} * ({load.length} + x)"
                    load.length = load.length + upper_bound

            if node.support:
                if isinstance(node.support, HingeSupport):
                    eqn += f" + {node.support.vertical_force} * x"
                    self.cache.append(
                        Load(
                            magnitude=node.support.vertical_force,
                            length=upper_bound,
                            type=node.support,
                        )
                    )
                elif isinstance(node.support, RollerSupport):
                    eqn += f" + {node.support.force} * x"
                    self.cache.append(
                        Load(
                            magnitude=node.support.force,
                            length=upper_bound,
                            type=node.support,
                        )
                    )
                else:
                    eqn += (
                        f" + {node.support.vertical_force} * x + {node.support.moment}"
                    )
                    self.cache.extend(
                        [
                            Load(
                                magnitude=node.support.vertical_force,
                                length=upper_bound,
                                type=HingeSupport(),
                            ),
                            Load(
                                magnitude=node.support.moment,
                                length=upper_bound,
                                type=PointMoment(magnitude=node.support.moment),
                            ),
                        ]
                    )

            if node.point_load:
                eqn += f" + {node.point_load.vertical_force} * x"
                self.cache.append(
                    Load(
                        magnitude=node.point_load.vertical_force,
                        length=upper_bound,
                        type=node.point_load,
                    )
                )

            if node.distributed_load:
                eqn += f" + {node.distributed_load.magnitude} * x * x / 2"
                self.cache.append(
                    ULoad(
                        magnitude=node.distributed_load.magnitude,
                        length=[upper_bound],
                        type=node.distributed_load,
                    )
                )

            if node.point_moment:
                eqn += f" + {node.point_moment.magnitude}"
                self.cache.append(
                    Load(
                        magnitude=node.point_moment.magnitude,
                        length=upper_bound,
                        type=node.point_moment,
                    )
                )

            bending_moment_equation = sympify(eqn)
            shear_force_equation = Derivative(
                bending_moment_equation, "x", evaluate=True
            )
            boundary = Boundary(lower_bound=lower_bound, upper_bound=upper_bound)
            b = Equation(eqn=bending_moment_equation, boundary=boundary)
            s = Equation(eqn=shear_force_equation, boundary=boundary)

            self._bending_moments_equations.append(b)
            self._shear_force_equations.append(s)
            self.points.append((lower_bound, upper_bound))

        self.solved = True

    def calculate_bending(self):

        if not self.solved:
            self._calculate_bending_and_shear()

        p = self._convert_points(self.points)
        b = []

        for idx, eqn in enumerate(self.bending_moments_equations):
            lower_bound_val = round(eqn.eqn.subs({"x": eqn.boundary.lower_bound}), 2)
            upper_bound_val = round(eqn.eqn.subs({"x": eqn.boundary.upper_bound}), 2)
            v = (lower_bound_val, upper_bound_val, p[idx][0], p[idx][1])
            v = Result(
                lower_bound=p[idx][0],
                upper_bound=p[idx][1],
                lower_bound_val=lower_bound_val,
                upper_bound_val=upper_bound_val,
                eqn=eqn.eqn,
            )

            b.append(v)

        return b

    def calculate_shear(self):

        if not self.solved:
            self._calculate_bending_and_shear()

        p = self._convert_points(self.points)
        s = []

        for idx, eqn in enumerate(self.shear_force_equations):
            lower_bound_val = round(eqn.eqn.subs({"x": eqn.boundary.lower_bound}), 2)
            upper_bound_val = round(eqn.eqn.subs({"x": eqn.boundary.upper_bound}), 2)
            # v = (lower_bound_val, upper_bound_val, p[idx][0], p[idx][1])

            v = Result(
                lower_bound=p[idx][0],
                upper_bound=p[idx][1],
                lower_bound_val=lower_bound_val,
                upper_bound_val=upper_bound_val,
                eqn=eqn.eqn,
            )

            s.append(v)

        return s

    def draw_bending_moment_diagram(self):
        pass

    def draw_shear_force_diagram(self):
        pass

    @staticmethod
    def _convert_points(points: list):

        n = []

        for idx, vals in enumerate(points):
            l, u = vals

            if idx == 0:
                n.append(vals)
                continue

            n.append((n[idx - 1][1] + l, n[idx - 1][1] + u))

        return n
