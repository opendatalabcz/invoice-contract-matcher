from abc import ABC, abstractmethod
from typing import List, Generator

from Models.models import Invoice


class IProvider(ABC):
    """
    Abstraktní trída představující interface pro Invoice Provider
    """
    @staticmethod
    @abstractmethod
    def get_generator(**kwargs) -> Generator[Invoice, None, None]:
        """
        Funkce které vrátí faktury z nějakého zdroje.
        :param kwargs: parametry, které mohou být vloženy
        :return: Generator faktur
        """
        pass