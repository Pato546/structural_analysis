from structural_analysis import PointLoad, UniformlyDistributedLoad, PointMoment
from structural_analysis.statically_determinate.solver import (
    StaticallyDeterminateSolver,
)
from structural_analysis import Beam, FixedSupport, HingeSupport, RollerSupport
from structural_analysis.beam import create_supports
from structural_analysis.bending_shear import BendingShearCalculator
from structural_analysis.statically_indeterminate.three_moment.solver import (
    ThreeMomentSolver,
)

from pprint import pprint

if __name__ == "__main__":

    def display_results(solved_beam: Beam):
        # TODO check RollerSupport direction

        for node in solved_beam:
            if node.support:
                if isinstance(node.support, HingeSupport):
                    if node.support.vertical_force < 0:
                        print(
                            f"{node.name}y = {abs(node.support.vertical_force):.2f} \u2193"
                        )
                    else:
                        print(
                            f"{node.name}y = {node.support.vertical_force:.2f} \u2191"
                        )

                    if node.support.horizontal_force < 0:
                        print(
                            f"{node.name}x = {abs(node.support.horizontal_force):.2f} \u2190"
                        )
                    else:
                        print(
                            f"{node.name}x = {node.support.horizontal_force:.2f} \u2192"
                        )

                elif isinstance(node.support, RollerSupport):
                    if node.support.force < 0:
                        print(f"{node.name}y = {abs(node.support.force):.2f} \u2193")
                    else:
                        print(f"{node.name}y = {node.support.force:.2f} \u2191")

                else:
                    if node.support.moment < 0:
                        print(f"{node.name}m = {abs(node.support.moment):.2f} \u21BA")
                    else:
                        print(f"{node.name}m = {node.support.moment:.2f} \u21BB")

                    if node.support.vertical_force < 0:
                        print(
                            f"{node.name}y = {abs(node.support.vertical_force):.2f} \u2193"
                        )
                    else:
                        print(
                            f"{node.name}y = {node.support.vertical_force:.2f} \u2191"
                        )

                    if node.support.horizontal_force < 0:
                        print(
                            f"{node.name}x = {abs(node.support.horizontal_force):.2f} \u2190"
                        )
                    else:
                        print(
                            f"{node.name}x = {node.support.horizontal_force:.2f} \u2192"
                        )


    b = Beam(8)
    #
    pl1 = PointLoad(-10, angle_of_inclination=60)
    print(pl1)
    # pl2 = PointLoad(-8)
    # udl = UniformlyDistributedLoad(-10, 5)
    # #
    s1, s2, s3, s4 = create_supports(
        [
            {"rx": True, "ry": True, 'rm': True},
            {'rx': True, 'ry': True},
            {"rx": True, "ry": True},
            {"rx": True, "ry": True},
        ]
    )
    #
    # b.append_node('A', 0, support=s1)
    # b.append_node('B', 3, point_load=pl1)
    # b.append_node('C', 5, support=s2, distributed_load=udl)
    # b.append_node('D', 10, support=s3)
    # # b.append_node('E', 11, support=s3)
    #
    # m = ThreeMomentSolver(b)
    # # pprint(m.get_sub_beams())
    # pprint(m.area_mul_centroid())

    # b.append_node('A', 0, support=s1)
    # b.append_node('B', 4, point_load=pl1)
    # b.append_node('C', 8, support=s2)
    #
    # b_s = StaticallyDeterminateSolver(b).solve()
    # display_results(b_s)
    #
    # b_c = BendingShearCalculator(b)
    # print(b_c.calculate_bending())
    # print("\n\n")
    # print(b_c.calculate_shear())

    udl = UniformlyDistributedLoad(-5, 3)
    pm = PointMoment(6)

    b.append_node('A', 0, distributed_load=udl, support=s1)
    b.append_node('B', 3, point_moment=pm, point_load=pl1)

    b_s = StaticallyDeterminateSolver(b).solve()
    display_results(b_s)

    b_c = BendingShearCalculator(b)
    print(b_c.calculate_bending())
    print(b_c.calculate_shear())
