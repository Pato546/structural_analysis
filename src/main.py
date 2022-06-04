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
    b = Beam()
    #
    pl1 = PointLoad(-10)
    pl2 = PointLoad(-40)
    pl3 = PointLoad(-20)

    pm = PointMoment(20)
    # print(pl1)
    # pl2 = PointLoad(-8)
    udl1 = UniformlyDistributedLoad(-10, 5)
    udl2 = UniformlyDistributedLoad(-2.3, 3)
    # #
    s1, s2, s3, s4 = create_supports(
        [
            {"rx": True, "ry": True},
            {'rx': True, 'ry': True},
            {"rx": True, "ry": True},
            {"rx": True, "ry": True},
        ]
    )

    b.append_node('A', 0, support=s1)
    b.append_node('B', 3, point_load=pl1)
    b.append_node('C', 5, support=s2, distributed_load=udl1)
    b.append_node('D', 10, support=s3)
    # b.append_node('E', 11, point_moment=pm)
    # b.append_node('F', 11, point_load=pl3)
    # b.append_node('E', 9, support=s3)
    # b.append_node('F', 11, point_load=pl3)
    # print(b.remove_first_node())
    # print(b.remove_last_node())
    # # exit()
    # print('===================================')
    # for n in b:
    #     print(n)
    #
    # exit()

    m = ThreeMomentSolver(b)
    print(m.three_hinge_support_solver())

    # for val in m.create_sub_beams():
    #     # print(f'Length = {beam.length}')
    #     for node in val[0]:
    #         print(node)
    #     print('----------------------------------------------------------')

    # b.append_node('A', 0, support=s1, distributed_load=udl1)
    # b.append_node('B', 3, point_load=pl2, distributed_load=udl2)
    # b.append_node('C', 6, support=s2)
    # #
    # b_s = StaticallyDeterminateSolver(b, check_determinacy=False).solve()
    # display_results(b_s)

    # #
    # b_c = BendingShearCalculator(b)
    # print(b_c.calculate_bending())
    # print("")
    # print(b_c.calculate_shear())

    # udl = UniformlyDistributedLoad(-5, 3)
    # pm = PointMoment(6)
    #
    # b.append_node('A', 0, distributed_load=udl, support=s1)
    # b.append_node('B', 3, point_moment=pm, point_load=pl1)
