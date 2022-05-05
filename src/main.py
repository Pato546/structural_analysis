from structural_analysis import PointLoad, UniformlyDistributedLoad, PointMoment
from structural_analysis.statically_determinate.solver import (
    StaticallyDeterminateSolver,
)
from structural_analysis import Beam
from structural_analysis.beam import create_supports
from structural_analysis.bending_shear import BendingShearCalculator

if __name__ == "__main__":
    # p1 = PointLoad(40, angle_of_inclination=60)
    # p2 = PointLoad(30, angle_of_inclination=25)
    # p3 = p1 - p2
    # print(p3.horizontal_force)
    # print(p3.vertical_force)
    # exit()
    # Create Beam
    b = Beam(length=12)

    # Create Loads
    pl = PointLoad(-20)
    udl1 = UniformlyDistributedLoad(-10, 5)
    # udl2 = UniformlyDistributedLoad(-10, 3)
    # udl3 = UniformlyDistributedLoad(-10, 1)
    pm1 = PointMoment(-6.21)
    pm2 = PointMoment(10)

    # Create Supports
    s1, s2, s3 = create_supports(
        [{'ry': True, 'rx': True, 'rm': True}, {'ry': True, 'rx': True}, {'ry': True, 'rx': True}])
    s1.moment = -6.21
    s1.vertical_force = 5
    # s1.horizontal_force = 0

    s2.vertical_force = 42.23
    s3.vertical_force = 22.77

    b.append_node('A', 0, support=s1)
    b.append_node('B', 3, point_load=pl)
    b.append_node('C', 5, support=s2, distributed_load=udl1)
    b.append_node('D', 10, support=s3)
    b.append_node('E', 12, point_load=pm2)

    # print(b.members)
    # print(b.is_geometrically_stable())
    # exit()

    # print(b.get_total_support_reactions())
    # print(b.get_eqn_on_conditions())
    # print(b.get_degree_of_ext_indeterminacy())
    # print(b.classify_beam())
    # solver = StaticallyDeterminateSolver(beam=b)
    # print(solver.total_rxn_generated_from_loads())
    # b_s = solver.solve()
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
    b_c = BendingShearCalculator(b)
    print(b_c.calculate_bending())
    print(b_c.calculate_shear())
    # print(b_c.shear_force_equations)
