from typing import Any

from .config_base import ConfigBase


class ConfigDict(ConfigBase):
    def __init__(self, data):
        # type: (dict) -> None
        self.__conf = data

    def get(self, key):
        # type: (str) -> Any
        return self.__conf.get(key)
