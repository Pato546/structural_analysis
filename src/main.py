from structural_analysis import PointLoad, UDL
from structural_analysis import FixedSupport, HingeSupport, RollerSupport
from structural_analysis.statically_determinate.solver import (
    StaticallyDeterminateSolver,
)


if __name__ == "__main__":
    loads = [PointLoad(-5, 5, 0), UDL(-10, 0, 0, 2, 0)]
    support_a = HingeSupport(0, 0)
    support_b = RollerSupport(4, 0)
    s = StaticallyDeterminateSolver(loads, support_a, support_b)
    rxn = s.total_rxn_generated_from_loads()
    print(rxn)
