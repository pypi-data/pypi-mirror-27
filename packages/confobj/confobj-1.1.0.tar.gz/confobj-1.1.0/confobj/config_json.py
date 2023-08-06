import json

from typing import Any

from .config_base import ConfigBase


class ConfigJson(ConfigBase):
    def __init__(self, path):
        # type: (str) -> None
        self.__conf = json.load(path)

    def get(self, key):
        # type: (str) -> Any
        return self.__conf.get(key)
