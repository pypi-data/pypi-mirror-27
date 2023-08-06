import abc

from typing import Any


class ConfigBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get(self, key):
        # type: (str) -> Any
        pass
