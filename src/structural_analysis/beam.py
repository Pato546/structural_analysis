from typing import Iterable
import math


class FixedSupport:
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y


class HingeSupport:
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y


class RollerSupport:
    def __init__(self, x: float, y: float, rx, ry):
        self._x = x
        self._y = y
        self.rx = rx
        self.ry = ry

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def is_rxn_horizontal(self):
        return self.rx

    def is_rxn_vertical(self):
        return self.ry


def support(
        x,
        y: float = 0.0,
        rx: bool or None = None,
        ry: bool or None = None,
        rm: bool or None = None,
):
    if rx and ry and rm:
        return FixedSupport(x=x, y=y)
    elif rx and ry:
        return HingeSupport(x=x, y=y)
    elif rx or ry:
        return RollerSupport(x=x, y=y, rx=rx, ry=ry)


class Beam:
    class Node:
        def __init__(self, name: str, x: float, y: float) -> None:
            self.name = name

            if x < 0:
                raise ValueError('x cannot be negative')
            self._x = x

            if y < 0:
                raise ValueError('y cannot be negative')
            self._y = y

            self.point_loads = []
            self.distributed_loads = []
            self.point_moments = []
            self.supports = []

        def __repr__(self) -> str:
            return f'{self.__class__.__name__}({self.name}, x={self._x}, y={self._y})'

        @property
        def x(self):
            return self._x

        @x.setter
        def x(self, val: float or int) -> None:
            if val < 0:
                raise ValueError('x cannot be negative')
            self._x = val

        @property
        def y(self):
            return self._y

        @y.setter
        def y(self, val: float or int):
            if val < 0:
                raise ValueError('y cannot be negative')
            self._y = val

        def add_point_load(self, pl):
            self.point_loads.append(pl)

        def add_distributed_loads(self, dl):
            self.distributed_loads.append(dl)

        def add_point_moments(self, pm):
            self.point_moments.append(pm)

        def support_support(self, s):
            self.supports.append(s)

        class Span:
            # TODO check loads again
            def __init__(self, node1, node2, loads):
                self._node1 = node1
                self._node2 = node2
                self._loads = loads

            def __len__(self) -> int:
                return int(
                    math.sqrt(
                        (self.node1.x - self.node2.x) ** 2 + (self.node1.y - self.node2.y) ** 2
                    )
                )

            @property
            def node1(self):
                return self._node1

            @property
            def node2(self):
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

    def __init__(self, l: float, e: float, i=None, cross_section=None) -> None:
        self.L = l
        self.e = e

        # TODO work on i and cross_section

    def add_node(self, n: Node) -> None:
        pass

    def check_degree_of_ext_indeterminacy(self) -> int:
        pass

    def check_geometric_stability(self) -> bool:
        pass

    def classify_beam(self):
        pass

    def get_supports(self) -> Iterable:
        pass

    def get_point_loads(self) -> Iterable:
        pass

    def get_distributed_loads(self) -> Iterable:
        pass

    def get_point_moments(self) -> Iterable:
        pass

    def get_eqns_on_condition(self):
        pass

    def get_total_support_reactions(self) -> int:
        pass

    def get_total_internal_forces(self) -> int:
        pass

    def get_total_unknowns(self) -> int:
        pass

    def get_rigid_members(self) -> int:
        # TODO write a decorator satisfy_eqn
        # TODO to whether rigid members satisfy the
        # TODO equilibrium equations
        pass

    def get_total_eqns_for_structure(self) -> int:
        # 3 * number of reactions
        pass


if __name__ == "__main__":
    f1 = support(0, rx=True, ry=True, rm=True)
    print(f1)
    h1 = support(4, rx=True, ry=True)
    print(h1)
    r1 = support(8, rx=True)
    print(f"Vy={r1.is_rxn_vertical()}")
    print(f"Vx={r1.is_rxn_horizontal()}")
