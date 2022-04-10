from structural_analysis import PointLoad, UDL
from structural_analysis import FixedSupport, HingeSupport, RollerSupport
from structural_analysis import Position
from structural_analysis.statically_determinate.solver import (
    StaticallyDeterminateSolver,
)


if __name__ == "__main__":
    loads = [
        UDL(-10, Position(0, 0), Position(2, 0)),
        UDL(-10, Position(2, 0), Position(6, 0)),
    ]
    support_a = HingeSupport(Position(2, 0))
    support_b = RollerSupport(Position(5, 0))
    s = StaticallyDeterminateSolver(loads, support_a, support_b)
    rxn = s.total_rxn_generated_from_loads()
    print(rxn)
