from structural_analysis import PointLoad, UniformlyDistributedLoad, PointMoment
from structural_analysis.statically_determinate.solver import (
    StaticallyDeterminateSolver,
)
from structural_analysis import Beam, sign_convention
from structural_analysis.beam import create_supports, RollerSupport
from structural_analysis.bending_shear import BendingShearCalculator

if __name__ == "__main__":
    # sign_convention()
    # p1 = PointLoad(40, angle_of_inclination=60)
    # p2 = PointLoad(30, angle_of_inclination=25)
    # p3 = p1 - p2
    # print(p3.horizontal_force)
    # print(p3.vertical_force)
    # exit()
    # Create Beam
    b = Beam(length=3)

    # Create Loads
    # pl = PointLoad(-10)
    udl1 = UniformlyDistributedLoad(-5, 3)
    # udl2 = UniformlyDistributedLoad(-10, 3)
    # udl3 = UniformlyDistributedLoad(-10, 1)
    pm = PointMoment(6)

    # Create Supports
    s1, s2 = create_supports([{'ry': True, 'rx': True, 'rm': True}, {'ry': True}])

    b.append_node('A', 0, distributed_load=udl1, support=s1)
    b.append_node('B', 3, point_moment=pm)
    # b.append_node('C', 7, point_load=pl)
    # b.append_node('D', 6)
    # b.append_node('D', 6)
    # b.append_node('B', 8, support=s3)

    # print(b.members)
    # print(b.is_geometrically_stable())
    # exit()

    # print(b.get_total_support_reactions())
    # print(b.get_eqn_on_conditions())
    # print(b.get_degree_of_ext_indeterminacy())
    # print(b.classify_beam())
    solver = StaticallyDeterminateSolver(beam=b)
    # print(solver.total_rxn_generated_from_loads())
    b_s = solver.solve()
    # for node in b_s:
    #     if node.support:
    #         if str(node.support) == 'HingeSupport':
    #             print(node.support.vertical_force)
    #             print(node.support.horizontal_force)
    #
    #         elif str(node.support) == 'RollerSupport':
    #             print(node.support.force)
    #
    #         else:
    #             print(node.support.moment)
    #             print(node.support.vertical_force)
    #             print(node.support.horizontal_force)
    b_c = BendingShearCalculator(b_s)
    b_c.calculate_bending_and_shear()
