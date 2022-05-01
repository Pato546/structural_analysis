from sympy import sympify, solve, pprint


class Load:
    def __init__(self, magnitude, length, type_):
        self.magnitude = magnitude
        self.length = length
        self.type = type_


class BendingShearCalculator:
    def __init__(self, beam):
        self.beam = beam
        self.cache: list = []

    def calculate_bending_and_shear(self):
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
                if load.type == "UniformlyDistributedLoad":
                    eqn += f"+{load.magnitude * load.length} * ({load.length / 2} + x)"
                    load.length = load.length + upper_bound

                elif load.type == "PointMoment":
                    eqn += f"+ {load.magnitude}"

                else:
                    eqn += f"+{load.magnitude} * ({load.length} + x)"
                    load.length = load.length + upper_bound

            if node.support:
                if str(node.support) == "HingeSupport":
                    eqn += f"+{node.support.vertical_force} * x"
                    self.cache.append(
                        Load(
                            magnitude=node.support.vertical_force,
                            length=upper_bound,
                            type_=str(node.support),
                        )
                    )
                elif str(node.support) == "RollerSupport":
                    eqn += f"+{node.support.force} * x"
                    self.cache.append(
                        Load(
                            magnitude=node.support.force,
                            length=upper_bound,
                            type_=str(node.support),
                        )
                    )
                else:
                    eqn += f"+{node.support.vertical_force} * x + {node.support.moment}"
                    self.cache.extend(
                        [
                            Load(
                                magnitude=node.support.vertical_force,
                                length=upper_bound,
                                type_="HingeSupport",
                            ),
                            Load(
                                magnitude=node.support.moment,
                                length=upper_bound,
                                type_="PointMoment",
                            ),
                        ]
                    )

            if node.point_load:
                eqn += f"+{node.point_load.vertical_force} * x"
                self.cache.append(
                    Load(
                        magnitude=node.point_load.vertical_force,
                        length=upper_bound,
                        type_=str(node.point_load),
                    )
                )

            if node.distributed_load:
                eqn += f"+{node.distributed_load.magnitude} * x * x / 2"
                self.cache.append(
                    Load(
                        magnitude=node.distributed_load.magnitude,
                        length=upper_bound,
                        type_=str(node.distributed_load),
                    )
                )

            if node.point_moment:
                eqn += f"+{node.point_moment.magnitude}"
                self.cache.append(
                    Load(
                        magnitude=node.point_moment.magnitude,
                        length=upper_bound,
                        type_=str(node.point_moment),
                    )
                )

            # print(eqn)

            pprint(sympify(eqn))
