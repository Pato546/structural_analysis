from . import Beam
from . import (
    StaticallyUnstableExternally,
    StaticallyIndeterminateExternally,
    GeometricallyUnstableExternally,
)


class StaticallyDeterminateSolver:
    def __init__(self, beam: Beam):
        self.hinge_roller: bool = False
        self.fixed_end: bool = False
        self.beam = beam

        if self.beam.classify_beam() == "determinate":
            if self.beam.is_geometrically_stable():
                print("\u2713 Structure is determinate and Geometrically stable")
            else:
                raise GeometricallyUnstableExternally(
                    "Structure is geometrically unstable"
                )
        else:
            if self.beam.classify_beam() == "unstable":
                raise StaticallyUnstableExternally("Structure is unstable")
            else:
                raise StaticallyIndeterminateExternally("Structure is indeterminate")

        self.beam_information: dict = self.beam.get_beam_information()
        self.supports = tuple(self.beam_information["supports"])

        if len(self.supports) > 1:
            self.support_a = self.supports[0]
            self.support_b = self.supports[1]
            self.hinge_roller = True
        elif len(self.supports) == 1:
            self.support = self.supports[0]
            self.fixed_end = True

        self.point_loads = tuple(self.beam_information["point_loads"])
        self.distributed_loads = tuple(self.beam_information["distributed_loads"])
        self.point_moments = tuple(self.beam_information["point_moments"])

    def _reactions_solver_for_point_loads(self) -> tuple[float, float, float]:
        support_a_x = self.support_a.x  # The x coordinate of the first support
        support_b_x = self.support_b.x  # The x coordinate of the second support
        summation_of_vertical_forces = 0
        summation_of_horizontal_forces = 0
        summation_of_moments = 0

        for load in self.point_loads:
            load_x = load.x  # The x coordinate of the load from the origin
            fx = load.horizontal_force * -1  # The horizontal component of the load
            fy = load.vertical_force * -1  # The vertical component of the load

            moment_arm_of_load = load_x - support_a_x

            summation_of_vertical_forces += fy
            summation_of_horizontal_forces += fx
            summation_of_moments += fy * moment_arm_of_load

        moment_arm_of_vertical_rxn_at_b = support_b_x - support_a_x

        vertical_rxn_at_b = summation_of_moments / moment_arm_of_vertical_rxn_at_b
        vertical_rxn_at_a = summation_of_vertical_forces - vertical_rxn_at_b
        horizontal_rxn = summation_of_horizontal_forces

        return vertical_rxn_at_a, vertical_rxn_at_b, horizontal_rxn

    def _reactions_solver_for_udl(self) -> tuple[float, float, float]:
        support_a_x = self.support_a.x
        support_b_x = self.support_b.x
        summation_of_vertical_forces = 0
        summation_of_moments = 0

        for load in self.distributed_loads:
            start_of_udl = load.start
            centroid_of_udl = load.centroid_of_udl()
            moment_arm_of_udl = centroid_of_udl + (start_of_udl - support_a_x)

            total_force_of_udl = -1 * load.total_force_of_udl()

            summation_of_vertical_forces += total_force_of_udl
            summation_of_moments += total_force_of_udl * moment_arm_of_udl

        moment_arm_of_vertical_rxn_at_b = support_b_x - support_a_x

        vertical_rxn_at_b = summation_of_moments / moment_arm_of_vertical_rxn_at_b
        vertical_rxn_at_a = summation_of_vertical_forces - vertical_rxn_at_b

        return vertical_rxn_at_a, vertical_rxn_at_b, 0

    def _reaction_solver_point_moment(self):
        support_a_x = self.support_a.x
        support_b_x = self.support_b.x
        summation_of_moments = 0
        summation_of_vertical_forces = 0

        for point_moment in self.point_moments:
            summation_of_moments += point_moment.magnitude

        moment_arm_of_vertical_rxn_at_b = support_b_x - support_a_x
        vertical_rxn_at_b = summation_of_moments / moment_arm_of_vertical_rxn_at_b
        vertical_rxn_at_a = summation_of_vertical_forces - vertical_rxn_at_b

        return vertical_rxn_at_a, vertical_rxn_at_b, 0

    def _hinge_roller_solver(self):
        rxn_from_point_loads = self._reactions_solver_for_point_loads()
        rxn_from_distributed_loads = self._reactions_solver_for_udl()
        rxn_from_point_moments = self._reaction_solver_point_moment()

        vertical_rxn_at_a, vertical_rxn_at_b, horizontal_rxn = (
            p + u + pm
            for p, u, pm in zip(
            rxn_from_point_loads, rxn_from_distributed_loads, rxn_from_point_moments
        )
        )

        return vertical_rxn_at_a, vertical_rxn_at_b, horizontal_rxn

    def _fixed_end_solver(self):
        # TODO work on horizontal reaction

        summation_of_point_loads = sum(-1 * load.magnitude for load in self.point_loads)
        summation_of_distributed_loads = sum(
            -1 * load.total_force_of_udl() for load in self.distributed_loads
        )
        vertical_reaction_at_support = (
                summation_of_point_loads + summation_of_distributed_loads
        )

        summation_of_moments_from_point_loads = sum(
            load.vertical_force * (load.x - self.support.x) for load in self.point_loads
        )

        summation_of_moments_from_distributed_loads = sum(
            load.total_force_of_udl()
            * (load.centroid_of_udl() + (load.start - self.support.x))
            for load in self.distributed_loads
        )

        summation_of_moments_from_point_moments = sum(
            -1 * load.magnitude for load in self.point_moments
        )

        moment_at_support = (
                summation_of_moments_from_point_loads
                + summation_of_moments_from_distributed_loads
                + summation_of_moments_from_point_moments
        )

        horizontal_reaction_at_support = 0

        return (
            moment_at_support,
            vertical_reaction_at_support,
            horizontal_reaction_at_support,
        )

    def solve(self):
        if self.hinge_roller:
            return self._hinge_roller_solver()
        return self._fixed_end_solver()
