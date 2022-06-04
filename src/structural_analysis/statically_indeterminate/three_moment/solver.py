from pprint import pprint
import operator
from typing import Sequence
from collections import deque, namedtuple

import attrs

from structural_analysis import (
    UniformlyDistributedLoad,
    PointLoad,
    PointMoment,
    HingeSupport,
    RollerSupport,
    Beam,
)
from structural_analysis.statically_determinate.solver import (
    StaticallyDeterminateSolver,
    display_results,
)

boundary = namedtuple("SupportBoundary", "lower_bound, upper_bound")


def pair_elements(iterables: Sequence, num_of_pairs: int) -> Sequence:
    _iterables = iterables
    iterable_container = []

    for idx, _ in enumerate(_iterables):

        if idx == num_of_pairs:
            break

        iterable_pairs = []

        idx_plus_1 = idx + 1
        x1, x2 = _iterables[idx], _iterables[idx_plus_1]

        iterable_pairs.append(_iterables[idx])
        iterable_pairs.append(_iterables[idx_plus_1])

        iterable_container.append(iterable_pairs)

    return iterable_container


@attrs.define(slots=True)
class ThreeMomentSolver:
    beam: Beam = attrs.field(validator=attrs.validators.instance_of(Beam))
    supports = attrs.field(init=False)
    point_loads = attrs.field(init=False)
    distributed_loads = attrs.field(init=False)
    point_moments = attrs.field(init=False)

    def create_sub_beams(self):
        support_counter: int = 0
        beam = Beam()
        collection_of_sub_beams = []

        for node in self.beam:

            if node.has_support:
                support_counter += 1

            if support_counter == 2:
                # add node to beam
                beam.append_node(
                    name=node.name,
                    x=node.x,
                    y=node.y,
                    point_load=node.point_load,
                    distributed_load=node.distributed_load,
                    point_moment=node.point_moment,
                    support=node.support,
                )

                val = (
                    beam,
                    boundary(*[node.support.x for node in beam if node.has_support]),
                )

                # add beam to collection of sub beams
                collection_of_sub_beams.append(val)

                if self.beam.members == len(collection_of_sub_beams):
                    if node.next_ is not None:
                        overhang_force = node.next_
                        beam.append_node(
                            name=overhang_force.name,
                            x=overhang_force.x,
                            y=overhang_force.y,
                            point_load=overhang_force.point_load,
                            distributed_load=overhang_force.distributed_load,
                            point_moment=overhang_force.point_moment,
                            support=overhang_force.support,
                        )

                # create new Beam
                beam = Beam()

                support_counter = 1

            beam.append_node(
                name=node.name,
                x=node.x,
                y=node.y,
                point_load=node.point_load,
                distributed_load=node.distributed_load,
                point_moment=node.point_moment,
                support=node.support,
            )

        return collection_of_sub_beams

    def three_hinge_support_solver(self):
        sub_beams = self.create_sub_beams()

        beam_info = []
        ma = 0
        mc = 0

        # external_support_moment = (ma, mb)

        for idx, (sub_beam, bound) in enumerate(sub_beams):
            for node in sub_beam:
                for el in node.elements:
                    if isinstance(
                            el, (PointLoad, UniformlyDistributedLoad, PointMoment)
                    ):
                        if isinstance(el, PointLoad):
                            if bound.lower_bound <= el.x < bound.upper_bound:
                                a = el.x - bound.lower_bound
                                b = bound.upper_bound - el.x
                                l = a + b  # span length

                                max_bending_moment = (
                                        -1 * (el.vertical_force * a * b) / l
                                )

                                if idx == 0:
                                    area_from_point_load_mul_centroid = (
                                            1 / 2 * a * max_bending_moment * (2 / 3 * a)
                                            + 1
                                            / 2
                                            * b
                                            * max_bending_moment
                                            * (a + 1 / 3 * b)
                                    )
                                else:
                                    area_from_point_load_mul_centroid = (
                                            1 / 2 * b * max_bending_moment * (2 / 3 * b)
                                            + 1
                                            / 2
                                            * a
                                            * max_bending_moment
                                            * (b + 1 / 3 * a)
                                    )
                                beam_info.append((area_from_point_load_mul_centroid, l))

                        elif isinstance(el, UniformlyDistributedLoad):
                            if bound.lower_bound <= el.start < bound.upper_bound:
                                end_node = (
                                        el.start + el.length
                                )  # coordinate of the end node of udl
                                print((end_node, bound.upper_bound))
                                if end_node == bound.upper_bound:
                                    l = bound.upper_bound - bound.lower_bound
                                    centroid = (1 / 2) * l

                                    area_from_udl = (
                                            2
                                            / 3
                                            * l
                                            * ((-1 * el.magnitude * pow(l, 2)) / 8)
                                    )

                                    area_from_udl_mul_centroid = (
                                            area_from_udl * centroid
                                    )

                                    beam_info.append((area_from_udl_mul_centroid, l))

                        # Overhang
                        # TODO check UDL overhang
                        if isinstance(el, (PointLoad, PointMoment)):
                            if idx == 0:
                                if el.x < bound.lower_bound:
                                    if isinstance(el, PointLoad):
                                        moment_arm = bound.lower_bound - el.x
                                        ma = el.vertical_force * moment_arm
                                    elif isinstance(el, PointMoment):
                                        ma = (
                                            el.magnitude
                                            if el.direction == -1
                                            else el.magnitude * -1
                                        )
                            else:
                                if el.x > bound.upper_bound:
                                    if isinstance(el, PointLoad):
                                        moment_arm = el.x - bound.upper_bound
                                        mc = el.vertical_force * moment_arm
                                    elif isinstance(el, PointMoment):
                                        mc = (
                                            el.magnitude * -1
                                            if el.direction == -1
                                            else el.magnitude * -1
                                        )

        (area1, l1), (area2, l2) = beam_info

        total_length = l1 + l2
        lhs = -1 * (ma * l1 + mc * l2)
        rhs = -6 * (operator.truediv(area1, l1) + operator.truediv(area2, l2))

        mb = (rhs + lhs) / (2 * total_length)
        print(mb)

        beams = [b for b, *_ in sub_beams]
        moments = pair_elements((ma, mb, -1 * mc), 2)

        for idx, (beam, _moments) in enumerate(zip(beams, moments)):
            counter = 0
            for node in beam:
                if node.has_support:
                    if idx == 0:
                        if counter == 1:
                            m = _moments[counter] * -1
                            pm = PointMoment(magnitude=m)
                            pm.x = node.x
                            pm.y = node.y
                            node.point_moment = pm
                            continue
                    pm = PointMoment(magnitude=_moments[counter])
                    pm.x = node.x
                    pm.y = node.y
                    node.point_moment = pm
                    counter += 1
            if idx == 0:
                if not beam.head.has_support:
                    beam.remove_first_node()
            if idx == 1:
                if not beam.tail.has_support:
                    beam.remove_last_node()
        for b in beams:
            for n in b:
                print(n)
            print('=========================================')
            # b = StaticallyDeterminateSolver(beam=b, check_determinacy=False).solve()
            # display_results(b)
