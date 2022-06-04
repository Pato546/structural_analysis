from typing import Iterable, Any
from types import MappingProxyType

import attrs

from .load import PointLoad, UniformlyDistributedLoad, PointMoment
from .beam_errors import SupportCreationError


# TODO automatically update the beam's length when nodes are added


class FixedSupport:
    NUMBER_OF_RESTRAINTS = 3

    def __init__(
            self,
            moment: float or None = None,
            vertical_force: float or None = None,
            horizontal_force: float or None = None,
            x: float or None = None,
            y: float or None = None,
    ):
        self._moment = moment
        self._vertical_force = vertical_force
        self._horizontal_force = horizontal_force
        self._x = x
        self._y = y

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    # def __str__(self) -> str:
    #     return self.__class__.__name__

    @property
    def moment(self):
        return self._moment

    @moment.setter
    def moment(self, val):
        if isinstance(val, (int, float)):
            self._moment = val
        else:
            raise ValueError("moment can only be int or float")

    @property
    def vertical_force(self):
        return self._vertical_force

    @vertical_force.setter
    def vertical_force(self, val):
        if isinstance(val, (int, float)):
            self._vertical_force = val
        else:
            raise ValueError("vertical force can only be int or float")

    @property
    def horizontal_force(self):
        return self._horizontal_force

    @horizontal_force.setter
    def horizontal_force(self, val):
        if isinstance(val, (int, float)):
            self._horizontal_force = val
        else:
            raise ValueError("horizontal force can only be int or float")

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, val):
        if val < 0:
            raise ValueError("x cannot be negative")
        self._x = val

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, val):
        if val < 0:
            raise ValueError("y cannot be negative")
        self._y = val

    @classmethod
    def get_num_of_restraints(cls):
        return cls.NUMBER_OF_RESTRAINTS

    @staticmethod
    def get_vertical_reaction():
        return 1

    @staticmethod
    def get_horizontal_reaction():
        return 1

    @staticmethod
    def get_moment():
        return 1


class HingeSupport:
    NUMBER_OF_RESTRAINTS = 2

    def __init__(
            self,
            vertical_force: float or None = None,
            horizontal_force: float or None = None,
            x: float or None = None,
            y: float or None = None,
    ):
        self._vertical_force = vertical_force
        self._horizontal_force = horizontal_force
        self._x = x
        self._y = y

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    # def __str__(self) -> str:
    #     return self.__class__.__name__

    @property
    def vertical_force(self):
        return self._vertical_force

    @vertical_force.setter
    def vertical_force(self, val):
        if isinstance(val, (int, float)):
            self._vertical_force = val
        else:
            raise ValueError("vertical force can only be int or float")

    @property
    def horizontal_force(self):
        return self._horizontal_force

    @horizontal_force.setter
    def horizontal_force(self, val):
        if isinstance(val, (int, float)):
            self._horizontal_force = val
        else:
            raise ValueError("horizontal force can only be int or float")

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, val):
        if val < 0:
            raise ValueError("x cannot be negative")
        self._x = val

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, val):
        if val < 0:
            raise ValueError("y cannot be negative")
        self._y = val

    @classmethod
    def get_num_of_restraints(cls):
        return cls.NUMBER_OF_RESTRAINTS

    @staticmethod
    def get_vertical_reaction():
        return 1

    @staticmethod
    def get_horizontal_reaction():
        return 1

    @staticmethod
    def get_moment():
        return 0


class RollerSupport:
    NUMBER_OF_RESTRAINTS = 1

    def __init__(
            self,
            force: float or None = None,
            x: float or None = None,
            y: float or None = None,
            rx: bool or None = None,
            ry: bool or None = None,
    ):
        self._force = force
        self._x = x
        self._y = y
        self.rx = rx
        self.ry = ry

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        return self.__class__.__name__

    @property
    def force(self):
        return self._force

    @force.setter
    def force(self, val):
        if isinstance(val, (int, float)):
            self._force = val
        else:
            raise ValueError("force can only be int or float")

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, val):
        if val < 0:
            raise ValueError("x cannot be negative")
        self._x = val

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, val):
        if val < 0:
            raise ValueError("y cannot be negative")
        self._y = val

    @classmethod
    def get_num_of_restraints(cls):
        return cls.NUMBER_OF_RESTRAINTS

    def get_vertical_reaction(self):
        if self.is_rxn_vertical():
            return 1
        else:
            return 0

    def get_horizontal_reaction(self):
        if self.is_rxn_vertical():
            return 0
        else:
            return 1

    @staticmethod
    def get_moment():
        return 0

    def is_rxn_vertical(self) -> bool:
        try:
            return self.ry
        except AttributeError:
            return self.rx


class InternalHinge:
    pass


class InternalRoller:
    pass


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


def create_supports(restraints: list[dict]):
    return [create_support(**r) for r in restraints]


@attrs.define(slots=True)
class Node:
    name: str = attrs.field(validator=attrs.validators.instance_of(str))
    x: int or float = attrs.field(validator=attrs.validators.ge(0))
    y: int or float = attrs.field(validator=attrs.validators.ge(0))
    next_ = attrs.field(repr=False)
    point_load: PointLoad = attrs.field(default=None, kw_only=True, repr=False)
    distributed_load: UniformlyDistributedLoad = attrs.field(
        default=None, kw_only=True, repr=False
    )
    point_moment: PointMoment = attrs.field(default=None, kw_only=True)
    support: FixedSupport or HingeSupport or RollerSupport = attrs.field(
        default=None, kw_only=True, repr=False
    )

    elements: list = attrs.field(init=False, factory=list)

    def __attrs_post_init__(self):
        if self.point_load:
            self.point_load.x = self.x
            self.point_load.y = self.y

            self.elements.append(self.point_load)

        if self.distributed_load:
            self.distributed_load.start = self.x

            self.elements.append(self.distributed_load)

        if self.point_moment:
            self.point_moment.x = self.x
            self.point_moment.y = self.y

            self.elements.append(self.point_moment)

        if self.support:
            self.support.x = self.x
            self.support.y = self.y

            self.elements.append(self.support)

    @property
    def has_support(self):
        return True if self.support else False


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


@attrs.define(slots=True)
class Beam:
    # total number of equilibrium equations
    NUMBER_OF_EQUILIBRIUM_EQUATIONS: int = 3

    # Material Properties
    MODULUS_OF_ELASTICITY: float = 20e-07
    THERMAL_EXPANSION_ALPHA: float = 1.2e-05

    # Geometric Properties
    CROSS_SECTIONAL_AREA: float = 1.000e-02
    MOMENT_OF_INERTIA: float = 1.000e-04
    L: float = attrs.field(default=None)
    modulus_of_elasticity: float = attrs.field(kw_only=True, repr=False)
    thermal_expansion_alpha: float = attrs.field(kw_only=True, repr=False)
    moment_of_inertia: float = attrs.field(kw_only=True, repr=False)
    cross_sectional_area: float = attrs.field(kw_only=True, repr=False)  # TODO check this again

    head = attrs.field(default=None, repr=False)
    tail = attrs.field(default=None, repr=False)
    size = attrs.field(default=0, repr=False)

    @modulus_of_elasticity.default
    def _modulus_of_elasticity(self):
        return self.MODULUS_OF_ELASTICITY

    @thermal_expansion_alpha.default
    def _thermal_expansion_alpha(self):
        return self.THERMAL_EXPANSION_ALPHA

    @moment_of_inertia.default
    def _moment_of_inertia(self):
        return self.MOMENT_OF_INERTIA

    @cross_sectional_area.default
    def _cross_sectional_area(self):
        return self.CROSS_SECTIONAL_AREA

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        return beam_iterator(self)

    @property
    def is_empty(self) -> bool:
        return self.size == 0

    def reactions(self):
        pass

    @property
    def length(self):
        return self.tail.x - self.head.x

    @property
    def members(self):
        supports = tuple(self.get_supports())

        if len(supports) == 1:
            if supports[0].get_num_of_restraints() == 3:
                return 1

        return len(supports) - 1

    @property
    def joints(self) -> int:
        supports = tuple(self.get_supports())

        if len(supports) == 1:
            if supports[0].get_num_of_restraints() == 3:
                return 1

        return len(supports)

    @property
    def number_of_vertical_reactions(self):
        supports = self.get_supports()
        num_of_vertical_rxn = 0
        for support in supports:
            num_of_vertical_rxn += support.get_vertical_reaction()

        return num_of_vertical_rxn

    @property
    def number_of_horizontal_reactions(self):
        supports = self.get_supports()
        num_of_horizontal_rxn = 0
        for support in supports:
            num_of_horizontal_rxn += support.get_horizontal_reaction()

        return num_of_horizontal_rxn

    @property
    def number_of_moments(self):
        supports = self.get_supports()
        num_of_moment = 0
        for support in supports:
            num_of_moment += support.get_moment()

        return num_of_moment

    def append_node(
            self,
            name: str = '',
            x: float = 0,
            y: float = 0.0,
            *,
            point_load: PointLoad or None = None,
            distributed_load: UniformlyDistributedLoad or None = None,
            point_moment: PointMoment or None = None,
            support: Any or None = None,
            node=None
    ) -> None:

        if node is None:
            node = Node(
                name=name,
                x=x,
                y=y,
                next_=None,
                point_load=point_load,
                distributed_load=distributed_load,
                point_moment=point_moment,
                support=support,
            )
        else:
            node = node

        if self.is_empty:
            self.head = node
        else:
            self.tail.next_ = node

        self.tail = node
        self.size += 1
        self.L = node.x

    def remove_first_node(self):
        if self.is_empty:
            raise Exception

        head = self.head
        self.head = self.head.next_
        self.size -= 1

        if self.is_empty:
            self.tail = None

        return head

    def remove_last_node(self):
        if self.tail is None:
            raise Exception

        previous = None
        head = self.head
        tail = self.tail

        while head.next_ is not None:
            previous = head
            head = head.next_

        previous.next_ = None
        self.tail = previous
        self.size -= 1

        if self.tail is None:
            self.head = self.tail

        return tail

    def is_geometrically_stable(self) -> bool:
        members = self.members
        reactions = self.get_total_support_reactions()
        joints = self.joints
        eqn_on_condition = self.get_eqn_on_conditions()

        ie = 3 * members + reactions - (3 * joints + eqn_on_condition)

        if ie == 0:
            if self.number_of_vertical_reactions == 1:
                return False
            if self.number_of_horizontal_reactions == 0:
                return False
        return True

    def classify_beam(self):
        r = self.get_total_support_reactions()
        eqn_on_condition = self.get_eqn_on_conditions()
        rhs = self.NUMBER_OF_EQUILIBRIUM_EQUATIONS + eqn_on_condition

        if r < rhs:
            return "unstable"
        elif r == rhs:
            return "determinate"
        else:
            return "indeterminate"

    def get_beam_information(self) -> MappingProxyType:
        return MappingProxyType(
            {
                "point_loads": self.get_point_loads(),
                "distributed_loads": self.get_distributed_loads(),
                "point_moments": self.get_point_moments(),
                "supports": self.get_supports(),
            }
        )

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
            if isinstance(support, InternalHinge):
                equations += 1
            elif isinstance(support, InternalRoller):
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
