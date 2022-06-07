from abc import ABCMeta, abstractmethod


class Structure(metaclass=ABCMeta):

    @abstractmethod
    def add_node(self, node):
        pass

    @abstractmethod
    def add_member(self, start, end, *args, **kwargs):
        pass

    @abstractmethod
    def get_nodes(self):
        pass

    @abstractmethod
    def get_members(self):
        pass
