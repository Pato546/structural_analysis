from . import Position


class FixedSupport:
    def __init__(self, position: Position):
        self._position = Position

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def position(self):
        return self._position

    @staticmethod
    def resist_moment() -> bool:
        return True

    @staticmethod
    def resist_vertical_force() -> bool:
        return True

    @staticmethod
    def resist_horizontal_force() -> bool:
        return True


class HingeSupport:
    def __init__(self, position: Position):
        self._position = position

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def position(self):
        return self._position

    @staticmethod
    def resist_moment() -> bool:
        return False

    @staticmethod
    def resist_vertical_force() -> bool:
        return True

    @staticmethod
    def resist_horizontal_force() -> bool:
        return True


class RollerSupport:
    def __init__(self, position: Position):
        self._position = position

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def position(self):
        return self._position

    @staticmethod
    def resist_moment() -> bool:
        return False

    @staticmethod
    def resist_vertical_force() -> bool:
        # depends on the orientation of the support
        pass

    @staticmethod
    def resist_horizontal_force() -> bool:
        # depends on the orientation of the support
        pass


if __name__ == '__main__':
    pass
