from abc import ABC, abstractmethod
from typing import List, Tuple
from Models.models import PossibleRelation


class Pipeline(ABC):
    """
    Třída, která má za cíl provést testy nad množinou spojení a vrátit spojení, které test vyloučil a které testy
    prošli úspěšně
    """

    @abstractmethod
    def prepare(self, *args, **kwargs) -> None:
        """
        Funkce, která slouží k připravení potřebných dat a spojení. V této funkci je žádoucí provést přípravu, která
        může být časově náročná a není nutné ji opakovat při každém testování
        :return: None
        """
        pass

    @abstractmethod
    def process_invoice_relations(self, relations: List[PossibleRelation]) -> Tuple[List[PossibleRelation], List[PossibleRelation]]:
        """
        Funkce, které slouží k otestování možných spojení.
        :param relations: List spojení, které chceme otestovat
        :return: Tuple, který obsajuje dva Listy, kde první List obsahuje spojení, které testy prošli a druhý List
        obsahuje spojení, které testy neprošli a již nemusí být v budoucnu testovány
        """
        pass
