import abc


class ConfigBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, key: str):
        pass
