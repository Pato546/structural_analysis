from typing import Iterable, Any

# import math

from .load import PointLoad, UniformlyDistributedLoad, PointMoment
from .beam_errors import SupportCreationError


class FixedSupport:
    NUMBER_OF_RESTRAINTS = 3

    def __init__(self, x: float or None = None, y: float or None = None):
        self._x = x
        self._y = y

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, val):
        if val < 0:
            raise ValueError("val cannot be negative")
        self._x = val

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, val):
        if val < 0:
            raise ValueError("val cannot be negative")
        self._y = val

    @classmethod
    def get_num_of_restraints(cls):
        return cls.NUMBER_OF_RESTRAINTS


class HingeSupport:
    NUMBER_OF_RESTRAINTS = 2

    def __init__(self, x: float or None = None, y: float or None = None):
        self._x = x
        self._y = y

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, val):
        if val < 0:
            raise ValueError("val cannot be negative")
        self._x = val

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, val):
        if val < 0:
            raise ValueError("val cannot be negative")
        self._y = val

    @classmethod
    def get_num_of_restraints(cls):
        return cls.NUMBER_OF_RESTRAINTS


class RollerSupport:
    NUMBER_OF_RESTRAINTS = 1

    def __init__(
            self,
            x: float or None = None,
            y: float or None = None,
            rx: bool or None = None,
            ry: bool or None = None,
    ):
        self._x = x
        self._y = y
        self.rx = rx
        self.ry = ry

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, val):
        if val < 0:
            raise ValueError("val cannot be negative")
        self._x = val

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, val):
        if val < 0:
            raise ValueError("val cannot be negative")
        self._y = val

    @classmethod
    def get_num_of_restraints(cls):
        return cls.NUMBER_OF_RESTRAINTS

    def is_rxn_horizontal(self):
        return self.rx

    def is_rxn_vertical(self):
        return self.ry


def create_support(
        rx: bool or None = None,
        ry: bool or None = None,
        rm: bool or None = None,
):
    if rx and ry and rm:
        return FixedSupport()
    elif rx and ry:
        return HingeSupport()
    elif rx or ry:
        return RollerSupport(rx=rx, ry=ry)

    raise SupportCreationError("Not enough information to create a valid support")


class Beam:
    # total number of equilibrium equations
    NUMBER_OF_EQUILIBRIUM_EQUATIONS = 3

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
                point_load: PointLoad or None = None,
                distributed_load: UniformlyDistributedLoad or None = None,
                point_moment: PointMoment or None = None,
                support: Any or None = None,
        ) -> None:
            self.name = name
            self.next_ = next_
            self.point_load = point_load
            self.distributed_load = distributed_load
            self.point_moment = point_moment
            self.support = support

            if x < 0:
                raise ValueError("x cannot be negative")
            self._x = x

            if y < 0:
                raise ValueError("y cannot be negative")
            self._y = y

            if self.point_load:
                self.point_load.x = self.x
                self.point_load.y = self.y

            if self.distributed_load:
                self.distributed_load.start = self.x

            if self.point_moment:
                self.point_moment.x = self.x
                self.point_moment.y = self.y

            if self.support:
                self.support.x = self.x
                self.support.y = self.y

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
        self.beam_information = {}

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
            point_load: PointLoad or None = None,
            distributed_load: UniformlyDistributedLoad or None = None,
            point_moment: PointMoment or None = None,
            support: Any or None = None,
    ) -> None:
        node = self.Node(
            name=name,
            x=x,
            y=y,
            next_=None,
            point_load=point_load,
            distributed_load=distributed_load,
            point_moment=point_moment,
            support=support,
        )
        if self.is_empty:
            self.head = node
        else:
            self.tail.next_ = node

        self.tail = node
        self._size += 1

    def check_geometric_stability(self) -> bool:
        pass

    def classify_beam(self):
        r = self.get_total_support_reactions()
        eqn_on_condition = self.get_eqn_on_conditions()
        rhs = self.NUMBER_OF_EQUILIBRIUM_EQUATIONS + eqn_on_condition

        if r < rhs:
            return 'unstable'
        elif r == rhs:
            return 'determinate'
        else:
            return 'indeterminate'

    def get_beam_information(self) -> dict:
        return {
            "point_loads": self.get_point_loads(),
            "distributed_loads": self.get_distributed_loads(),
            "point_moments": self.get_point_moments(),
            "supports": self.get_supports(),
        }

    def get_degree_of_ext_indeterminacy(self) -> int:
        r = self.get_total_support_reactions()
        eqn_on_condition = self.get_eqn_on_conditions()
        rhs = self.NUMBER_OF_EQUILIBRIUM_EQUATIONS + eqn_on_condition

        return r - rhs

    def get_supports(self) -> Iterable:
        return (node.support for node in self if node.support)

    def get_point_loads(self) -> Iterable:
        return (node.point_load for node in self if node.point_load)

    def get_distributed_loads(self) -> Iterable:
        return (node.distributed_load for node in self if node.distributed_load)

    def get_point_moments(self) -> Iterable:
        return (node.point_moment for node in self if node.point_moment)

    def get_eqn_on_conditions(self) -> int:
        equations = 0
        supports = self.get_supports()
        for support in supports:
            if str(support) == "InternalHinge":
                equations += 1
            elif str(support) == "InternalRoller":
                equations += 2

        return equations

    def get_total_support_reactions(self) -> int:
        support_rxn = 0
        supports = self.get_supports()
        for support in supports:
            support_rxn += support.get_num_of_restraints()
        return support_rxn


if __name__ == "__main__":
    pl = PointLoad(-40)
    pl2 = PointLoad(-40)
    ul = UniformlyDistributedLoad(-40, 7)
    pm = PointMoment(-90)
    s = create_support(ry=True)
    b = Beam(length=12, e=0, i=0)
    b.append_node("A", 0, 0, point_load=pl)
    b.append_node("B", 4, 0, point_load=pl2, point_moment=pm)
    b.append_node("C", 0, 0, distributed_load=ul, support=s)
    # print(len(b))
    print(list(b.get_point_loads()))
    print(list(b.get_distributed_loads()))
    print(list(b.get_point_moments()))
    print(list(b.get_supports()))
