from typing import Iterable
# import math

from load import PointLoad, UniformlyDistributedLoad, PointMoment


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
    # Material Properties
    MODULUS_OF_ELASTICITY = 20e-07
    THERMAL_EXPANSION_ALPHA = 1.2e-05

    # Geometric Properties
    CROSS_SECTIONAL_AREA = 1.000e-02
    MOMENT_OF_INERTIA = 1.000e-04

    class beam_iterator:
        def __init__(self, obj):
            self.head = obj.head

        def __iter__(self):
            return self

        def __next__(self):
            try:
                return self.head
            except AttributeError:
                raise StopIteration
            finally:
                try:
                    self.head = self.head.next_
                except AttributeError:
                    raise StopIteration

    class Node:
        def __init__(
                self,
                name: str,
                x: float,
                y: float,
                next_,
                *,
                point_loads: tuple or None,
                distributed_loads: tuple or None,
                point_moments: tuple or None,
                supports: tuple or None,
        ) -> None:
            self.name = name
            self.next_ = next_
            self.point_loads = point_loads
            self.distributed_loads = distributed_loads
            self.point_moments = point_moments
            self.supports = supports

            if x < 0:
                raise ValueError("x cannot be negative")
            self._x = x

            if y < 0:
                raise ValueError("y cannot be negative")
            self._y = y

            if point_loads:
                for point_load in point_loads:
                    point_load.x = self.x
                    point_load.y = self.y

            if distributed_loads:
                for udl in distributed_loads:
                    udl.start = self.x

            if point_moments:
                for point_moment in point_moments:
                    point_moment.x = self.x
                    point_moment.y = self.y

        def __repr__(self) -> str:
            return (
                f"{self.__class__.__name__}(name={self.name}, x={self._x}, y={self._y})"
            )

        @property
        def x(self):
            return self._x

        @x.setter
        def x(self, val: float or int) -> None:
            if val < 0:
                raise ValueError("x cannot be negative")
            self._x = val

        @property
        def y(self):
            return self._y

        @y.setter
        def y(self, val: float or int):
            if val < 0:
                raise ValueError("y cannot be negative")
            self._y = val

    def __init__(
            self,
            length: float,
            e: float or None = None,
            alpha: float or None = None,
            i: float or None = None,
            cross_section: float or None = None,
    ) -> None:
        self.L = length

        if e is None:
            self.modulus_of_elasticity = self.MODULUS_OF_ELASTICITY
        else:
            self.modulus_of_elasticity = e

        if alpha is None:
            self.thermal_expansion_alpha = self.THERMAL_EXPANSION_ALPHA
        else:
            self.thermal_expansion_alpha = alpha

        if i is None:
            self.moment_of_inertia = self.MOMENT_OF_INERTIA
        else:
            self.moment_of_inertia = i

        if cross_section is None:
            self.cross_sectional_area = self.CROSS_SECTIONAL_AREA
        else:
            self.cross_sectional_area = cross_section

        self.head = None
        self.tail = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        return self.beam_iterator(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(length={self.L})"

    @property
    def is_empty(self) -> int:
        return self._size == 0

    def append_node(
            self,
            name: str,
            x: float,
            y: float,
            *,
            point_loads: tuple or None = None,
            distributed_loads: tuple or None = None,
            point_moments: tuple or None = None,
            supports: tuple or None = None,
    ) -> None:
        node = self.Node(
            name=name,
            x=x,
            y=y,
            next_=None,
            point_loads=point_loads,
            distributed_loads=distributed_loads,
            point_moments=point_moments,
            supports=supports,
        )
        if self.is_empty:
            self.head = node
        else:
            self.tail._next = node

        self.tail = node
        self._size += 1

    def check_degree_of_ext_indeterminacy(self) -> int:
        pass

    def check_geometric_stability(self) -> bool:
        pass

    def classify_beam(self):
        pass

    def get_supports(self) -> Iterable:
        pass

    def get_point_loads(self) -> Iterable:
        return (
            point_load
            for node in self
            if node.point_loads
            for point_load in node.point_loads
        )

    def get_distributed_loads(self) -> Iterable:
        return (
            udl
            for node in self
            if node.distributed_loads
            for udl in node.distributed_loads
        )

    def get_point_moments(self) -> Iterable:
        return (
            point_moment
            for node in self
            if node.point_moments
            for point_moment in node.point_moments
        )

    def get_eqn_on_condition(self):
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

    def get_total_eqn_for_structure(self) -> int:
        # 3 * number of reactions
        pass


if __name__ == "__main__":
    pl = (PointLoad(-40), PointLoad(-20))
    ul = (UniformlyDistributedLoad(-40, 7),)
    pm = (PointMoment(-90),)
    b = Beam(length=12, e=0, i=0)
    b.append_node("A", 0, 0, point_loads=pl)
    b.append_node("B", 4, 0, point_loads=pl, point_moments=pm)
    b.append_node("C", 0, 0, distributed_loads=ul)
    print(len(b))
    print(b.get_point_loads())
    print(b.get_distributed_loads())
    print(b.get_point_moments())
