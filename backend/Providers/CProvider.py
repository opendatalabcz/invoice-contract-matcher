from abc import ABC, abstractmethod
from typing import List, Generator

from Models.models import Contract


class CProvider(ABC):
    """
    Abstraktní trída představující interface pro Contract Provider
    """
    @staticmethod
    @abstractmethod
    def get_generator(**kwargs) -> Generator[Contract, None, None]:
        """
        Funkce které vrátí smlouvy z nějakého zdroje.
        :param kwargs: parametry, které mohou být vloženy
        :return: Generator smluv.
        """
        pass