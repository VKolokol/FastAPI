from abc import ABC, abstractmethod


class CRUDRepository(ABC):

    @abstractmethod
    def get_all(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_object(self, *args, **kwargs):
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def remove(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass
