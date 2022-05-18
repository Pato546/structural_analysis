class ThreeMomentSolver:
    def __init__(self, beam):
        self.beam = beam
        self.beam_information: dict = beam.get_beam_information()
        self.supports = tuple(self.beam_information["supports"])
        self.point_loads = list(self.beam_information["point_loads"])
        self.distributed_loads = list(self.beam_information["distributed_loads"])
        self.point_moments = list(self.beam_information["point_moments"])

    # def __repr__(self):
    #     return f"{self.__class__.__name__}({repr(self.solve())})"

    def create_sub_beams(self):
        pass

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
                if str(load) == "UniformlyDistributedLoad":
                    if supports[0].x <= load.start < supports[1].x:
                        supports.append(load)
                else:
                    if supports[0].x <= load.x < supports[1].x:
                        supports.append(load)

        for elem in support_container:
            elem.sort(
                key=lambda e: e.start if str(e) == "UniformlyDistributedLoad" else e.x
            )

        return support_container
