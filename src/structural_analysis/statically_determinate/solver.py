from . import Beam
from . import StaticallyUnstableExternally, StaticallyIndeterminateExternally


class StaticallyDeterminateSolver:
    def __init__(self, beam: Beam):
        self.beam = beam
        self.beam_type = self.beam.classify_beam()

        if self.beam_type == 'determinate':
            pass
        else:
            if self.beam_type == 'unstable':
                raise StaticallyUnstableExternally('Structure is unstable')
            else:
                raise StaticallyIndeterminateExternally('Structure is indeterminate')

        self.beam_information: dict = self.beam.get_beam_information()
        self.supports = tuple(self.beam_information['supports'])

        if len(self.supports) > 1:
            self.support_a = self.supports[0]
            self.support_b = self.supports[1]
        elif len(self.supports) == 1:
            raise NotImplementedError('Solver does not work for built-in beams')

        self.point_loads = self.beam_information['point_loads']
        self.distributed_loads = self.beam_information['distributed_loads']

    def _reactions_solver_for_point_loads(self) -> tuple[float, float, float]:
        support_a_x = self.support_a.x  # The x coordinate of the first support
        support_b_x = self.support_b.x  # The x coordinate of the second support
        summation_of_vertical_forces = 0
        summation_of_horizontal_forces = 0
        summation_of_moments = 0

        for load in self.point_loads:
            load_x = load.x  # The x coordinate of the load from the origin
            fx = load.horizontal_force() * -1  # The horizontal component of the load
            fy = load.vertical_force() * -1  # The vertical component of the load

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

    def total_rxn_generated_from_loads(self):
        rxn_from_point_loads = self._reactions_solver_for_point_loads()
        rxn_from_udl = self._reactions_solver_for_udl()

        vertical_rxn_at_a, vertical_rxn_at_b, horizontal_rxn = (
            p + u for p, u in zip(rxn_from_point_loads, rxn_from_udl)
        )

        return vertical_rxn_at_a, vertical_rxn_at_b, horizontal_rxn
