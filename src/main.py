from structural_analysis import PointLoad, UniformlyDistributedLoad
from structural_analysis.statically_determinate.solver import (
    StaticallyDeterminateSolver,
)
from structural_analysis import Beam
from structural_analysis.beam import create_support

if __name__ == "__main__":
    b = Beam(length=7)
    s = create_support(rx=True, ry=True, rm=True)
    udl = UniformlyDistributedLoad(-5, 5)
    b.append_node('A', 0, 0, distributed_load=udl, support=s)
    s2 = create_support(ry=True)
    b.append_node('B', 5, 0, support=s2)
    p = PointLoad(-10)
    b.append_node('C', 7, 0, point_load=p)

    # print(b.get_total_support_reactions())
    # print(b.get_eqn_on_conditions())
    print(b.get_degree_of_ext_indeterminacy())
    print(b.classify_beam())
    solver = StaticallyDeterminateSolver(beam=b)
    print(solver.total_rxn_generated_from_loads())
