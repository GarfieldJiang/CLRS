from abc import ABC, abstractmethod


class Map(ABC):
    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __getitem__(self, k):
        pass

    @abstractmethod
    def __setitem__(self, k, v):
        pass

    @abstractmethod
    def __contains__(self, k):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def pop(self, k):
        pass

    @abstractmethod
    def keys(self):
        pass

    @abstractmethod
    def values(self):
        pass
