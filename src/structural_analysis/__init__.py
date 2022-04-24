from .load import PointLoad, UniformlyDistributedLoad, PointMoment
from .beam import Beam
from .beam_errors import (
    GeometricallyUnstableExternally,
    StaticallyUnstableExternally,
    SupportCreationError,
    StaticallyIndeterminateExternally,
)

__version__ = "1.0.0a"


def sign_convention():
    print("- \u2193   + \u2191")
    print("- \u2190   + \u2192")
    print("- \u21BA   + \u21BB")
