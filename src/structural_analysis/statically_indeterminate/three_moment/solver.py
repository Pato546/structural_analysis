from pprint import pprint

from structural_analysis import UniformlyDistributedLoad, PointLoad, PointMoment


class ThreeMomentSolver:
    def __init__(self, beam):
        self.beam = beam
        self.beam_information: dict = beam.get_beam_information()
        self.supports = tuple(self.beam_information["supports"])
        self.point_loads = list(self.beam_information["point_loads"])
        self.distributed_loads = list(self.beam_information["distributed_loads"])
        self.point_moments = list(self.beam_information["point_moments"])

        self.spans = self.get_sub_beams()

    # def __repr__(self):
    #     return f"{self.__class__.__name__}({repr(self.solve())})"

    def create_sub_beams(self):

        sub_beams_container = []

        for idx in range(len(self.spans)):
            if idx == len(self.spans) - 1:
                break
            sub_beams_pair = []
            idx_plus_1 = idx + 1
            sub_beams_pair.append(self.spans[idx])
            sub_beams_pair.append(self.spans[idx_plus_1])
            sub_beams_container.append(sub_beams_pair)

        return sub_beams_container

    def get_sub_beams(self):
        num_of_supports = len(self.supports)
        num_of_spans = num_of_supports - 1
        loads = self.point_loads + self.distributed_loads + self.point_moments

        support_container = []

        for idx in range(num_of_supports):
            if idx == num_of_spans:
                break
            support_pairs = []
            idx_plus_1 = idx + 1
            support_pairs.append(self.supports[idx])
            support_pairs.append(self.supports[idx_plus_1])

            support_container.append(support_pairs)

        for load in loads:
            for supports in support_container:
                if isinstance(load, UniformlyDistributedLoad):
                    if supports[0].x <= load.start < supports[1].x:
                        supports.append(load)
                else:
                    if supports[0].x <= load.x < supports[1].x:
                        supports.append(load)

        for elem in support_container:
            elem.sort(
                key=lambda e: e.start
                if isinstance(e, UniformlyDistributedLoad)
                else e.x
            )

        return support_container

    def area_mul_centroid(self):
        sub_beams = self.create_sub_beams()[0]
        pprint(sub_beams)
        areas_mul_centroid = []
        length_of_spans = []

        for idx, sub_beam in enumerate(sub_beams):
            span = sub_beam

            for el in span:
                if isinstance(el, (PointLoad, UniformlyDistributedLoad, PointMoment)):

                    if isinstance(el, PointLoad):
                        a = span[0].x + el.x
                        b = span[-1].x - el.x
                        l = a + b  # span length

                        length_of_spans.append(l)

                        max_bending_moment = -1 * (el.vertical_force * a * b) / l

                        if idx == 0:
                            area_from_point_load_mul_centroid = (
                                    1 / 2 * a * max_bending_moment * (2 / 3 * a)
                                    + 1 / 2 * b * max_bending_moment * (a + 1 / 3 * b)
                            )
                        else:
                            area_from_point_load_mul_centroid = (
                                    1 / 2 * b * max_bending_moment * (2 / 3 * b)
                                    + 1 / 2 * a * max_bending_moment * (b + 1 / 3 * a)
                            )

                        areas_mul_centroid.append(
                            (area_from_point_load_mul_centroid, l)
                        )

                    elif isinstance(el, UniformlyDistributedLoad):
                        end_node = (
                                el.start + el.length
                        )  # coordinate of the end node of udl
                        if span[-1].x == end_node:
                            l = span[-1].x - span[0].x
                            length_of_spans.append(l)
                            centroid = (1 / 2) * l

                            area_from_udl = (
                                    2 / 3 * l * ((-1 * el.magnitude * pow(l, 2)) / 8)
                            )

                            area_from_udl_mul_centroid = area_from_udl * centroid
                            areas_mul_centroid.append((area_from_udl_mul_centroid, l))

        print(areas_mul_centroid)
        print(length_of_spans)

        # Right-hand side of the three moment equation
        rhs = -6 * sum(area_mul_centroid / l for area_mul_centroid, l in areas_mul_centroid)

        r_moment = rhs / (2 * sum(length_of_spans))

        return r_moment
