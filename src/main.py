from structural_analysis import PointLoad, UniformlyDistributedLoad, PointMoment
from structural_analysis.statically_determinate.solver import (
    StaticallyDeterminateSolver,
)
from structural_analysis import Beam, sign_convention
from structural_analysis.beam import create_support, create_supports

if __name__ == "__main__":
    sign_convention()
    exit()
    # Create Beam
    b = Beam(length=8)

    # Create Loads
    # pl = PointLoad(-10)
    udl = UniformlyDistributedLoad(-6, 3)
    pm = PointMoment(-120)

    # Create Supports
    s1, *_ = create_supports([{'rx': True, 'ry': True, 'rm': True}])

    b.append_node('A', 0, support=s1)
    b.append_node('B', 2, point_moment=pm)
    b.append_node('C', 4, distributed_load=udl)
    b.append_node('D', 7)
    b.append_node('E', 8)

    # print(b.get_total_support_reactions())
    # print(b.get_eqn_on_conditions())
    print(b.get_degree_of_ext_indeterminacy())
    print(b.classify_beam())
    solver = StaticallyDeterminateSolver(beam=b)
    # print(solver.total_rxn_generated_from_loads())
    print(solver.solve())
