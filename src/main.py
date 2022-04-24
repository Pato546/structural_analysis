from structural_analysis import PointLoad, UniformlyDistributedLoad, PointMoment
from structural_analysis.statically_determinate.solver import (
    StaticallyDeterminateSolver,
)
from structural_analysis import Beam, sign_convention
from structural_analysis.beam import create_support, create_supports

if __name__ == "__main__":
    # sign_convention()
    # p1 = PointLoad(40, angle_of_inclination=60)
    # p2 = PointLoad(30, angle_of_inclination=25)
    # p3 = p1 - p2
    # print(p3.horizontal_force)
    # print(p3.vertical_force)
    # exit()
    # Create Beam
    b = Beam(length=8)

    # Create Loads
    # pl = PointLoad(-20)
    # udl = UniformlyDistributedLoad(-5, 3)
    # pm = PointMoment(6)

    # Create Supports
    s1, s2 = create_supports([{'ry': True, 'rx': True}, {'ry': True}])

    b.append_node('A', 0, support=s1)
    b.append_node('B', 4, support=s2)
    # b.append_node('B', 8, support=s3)

    print(b.members)
    print(b.is_geometrically_stable())
    # exit()

    # print(b.get_total_support_reactions())
    # print(b.get_eqn_on_conditions())
    print(b.get_degree_of_ext_indeterminacy())
    print(b.classify_beam())
    solver = StaticallyDeterminateSolver(beam=b)
    # print(solver.total_rxn_generated_from_loads())
    print(solver.solve())
