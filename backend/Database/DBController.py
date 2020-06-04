from abc import abstractmethod, ABC
from typing import Callable, Optional, List, Dict
from Models.models import Contract, Invoice, PossibleRelation, TestResult, BlockedSupplier


class DBController(ABC):

    @abstractmethod
    def connect(self, host: str, database: str, user: str, password: str, port: int, echo: bool = False):
        """
        Funkce pro připojení k databázi
        :param host: adresa host databáze
        :param database: jméno databáze
        :param user: jméno uživatele
        :param password: heslo pro přihlášení
        :param port: port
        :param echo: Boolean hodnota určující, zda má mají být logovány informace z databáze
        :return: None
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """
        Funkce pro odpojení od databáze.
        :return: None
        """
        pass

    @abstractmethod
    def begin_transaction(self) -> None:
        """
        Funkce pro spuštění nové transakce.
        :return: None
        """
        pass

    @abstractmethod
    def commit(self) -> None:
        """
        Funkce pro potvrzení změn.
        :return: None
        """
        pass

    @abstractmethod
    def rollback(self) -> None:
        """
        Funkce pro vrácení změn poslední transakce.
        :return:
        """
        pass

    # contract
    @abstractmethod
    def get_contract(self, contract_id: int) -> Optional[Contract]:
        """
        Funkce pro získání smlouvy z databáze pomocí id.
        :param contract_id: ID smlouvy v databázi.
        :return: Contract, s odpovídajícím id, pokud existuje.
                 None, pokud neexistuje.
        """
        pass

    @abstractmethod
    def insert_contract(self, contract: Contract) -> None:
        """
        Funkce pro vložení smlouvy do databáze.
        :param contract: Contract, který chceme vložit.
        :return: None
        """
        pass

    @abstractmethod
    def update_contract(self, contract: Contract) -> None:
        """
        Funkce pro aktualizaci smlouvy v databázi.
        :param contract: Contract, kde contract_id musí odpovídat smlouvě v databázi.
        :return: None
        """
        pass

    @abstractmethod
    def remove_contract(self, contract: Contract) -> None:
        """
        Funkce pro odstranění smlouvy z databáze.
        :param contract: Contract, který chceme odstranit.
        :return: None
        """
        pass

    @abstractmethod
    def get_contracts(self, custom_filter: Callable[[Contract], bool] = None) -> Optional[List[Contract]]:
        """
        Funkce pro získání více smluv.
        :param custom_filter: Nepovinný filtr, který bude aplikován na každou smlouvu.
        :return: List[Contract] pokud smlouvy existují
                 None, pokud nejsou dostupné žádné smlouvy
        """
        pass

    # invoice
    @abstractmethod
    def get_invoice(self, invoice_id: int) -> Optional[Invoice]:
        """
        Funkce pro získání faktury z databáze pomocí id.
        :param invoice_id: ID faktury v databázi.
        :return: Invoice, s odpovídajícím id, pokud existuje.
                 None, pokud neexistuje.
        """
        pass

    @abstractmethod
    def insert_invoice(self, invoice: Invoice) -> None:
        """
        Funkce pro vložení faktury do databáze.
        :param invoice: Invoice, který chceme vložit.
        :return: None
        """
        pass

    @abstractmethod
    def update_invoice(self, invoice: Invoice) -> None:
        """
        Funkce pro aktualizaci faktury v databázi.
        :param invoice: Invoice, kde invoice_id musí odpovídat faktuře v databázi.
        :return: None
        """
        pass

    @abstractmethod
    def remove_invoice(self, invoice: Invoice) -> None:
        """
        Funkce pro odstranění faktury z databáze.
        :param invoice: Invoice, který chceme odstranit.
        :return: None
        """
        pass

    @abstractmethod
    def get_invoices(self, page: int = None, page_size: int = None, custom_filter: Callable[[Invoice], bool] = None) -> \
            Optional[List[Invoice]]:
        """
        Funkce pro získání více faktur.
        :param page: číslo stránky, kterou chceme získat.
        :param page_size: Velikost stránky
        :param custom_filter: Filtr, který bude použit pro filtrování faktur.
        :return: List[Invoice] pokud smlouvy existují.
                 None, pokud nejsou dostupné žádné smlouvy.
        """
        pass

    # possible_relation
    @abstractmethod
    def get_possible_relation(self, possible_relation_id: int) -> Optional[PossibleRelation]:
        """
        Funkce pro získání spojení z databáze pomocí id.
        :param possible_relation_id: ID spojení v databázi.
        :return: PossibleRelation, s odpovídajícím id, pokud existuje.
                 None, pokud neexistuje.
        """
        pass

    @abstractmethod
    def insert_possible_relation(self, relation: PossibleRelation) -> None:
        """
        Funkce pro vložení spojení do databáze.
        :param relation: PossibleRelation, který chceme vložit.
        :return: None
        """
        pass

    @abstractmethod
    def update_possible_relation(self, possible_relation: PossibleRelation) -> None:
        """
        Funkce pro aktualizaci spojení v databázi.
        :param possible_relation: PossibleRelation, kde possible_relation_id musí odpovídat spojení v databázi.
        :return: None
        """
        pass

    @abstractmethod
    def remove_possible_relation(self, possible_relation: PossibleRelation) -> None:
        """
        Funkce pro odstranění spojení z databáze.
        :param possible_relation: PossibleRelation, který chceme odstranit.
        :return: None
        """
        pass

    # test_result
    @abstractmethod
    def get_test_result(self, test_result_id: int) -> Optional[TestResult]:
        """
        Funkce pro získání výsledku testu z databáze pomocí id.
        :param test_result_id: ID výsledku testu v databázi.
        :return: TestResult, s odpovídajícím id, pokud existuje.
                 None, pokud neexistuje.
        """
        pass

    @abstractmethod
    def insert_test_result(self, test_result: TestResult) -> None:
        """
        Funkce pro vložení výsledku testu do databáze.
        :param test_result: TestResult, který chceme vložit.
        :return: None
        """
        pass

    @abstractmethod
    def update_test_result(self, test_result: TestResult) -> None:
        """
        Funkce pro aktualizaci výsledku testu v databázi.
        :param test_result: TestResult, kde possible_relation_id musí odpovídat spojení v databázi.
        :return: None
        """
        pass

    @abstractmethod
    def remove_test_result(self, test_result: TestResult) -> None:
        """
        Funkce pro odstranění výsledku testu z databáze.
        :param test_result: TestResult, který chceme odstranit.
        :return: None
        """
        pass

    # blocked supplier
    @abstractmethod
    def get_blocked_supplier(self, blocked_supplier_id: int) -> Optional[BlockedSupplier]:
        """
        Funkce pro získání záznamu o blokovaném dodavateli z databáze pomocí id.
        :param blocked_supplier_id: ID výsledku testu v databázi.
        :return: BlockedSupplier, s odpovídajícím id, pokud existuje.
                 None, pokud neexistuje.
        """
        pass

    @abstractmethod
    def insert_blocked_supplier(self, blocked_supplier: BlockedSupplier) -> None:
        """
        Funkce pro vložení záznamu o blokovaném dodavateli do databáze.
        :param blocked_supplier: BlockedSupplier, který chceme vložit.
        :return: None
        """
        pass

    @abstractmethod
    def update_blocked_supplier(self, blocked_supplier: BlockedSupplier) -> None:
        """
        Funkce pro aktualizaci záznamu o blokovaném dodavateli testu v databázi.
        :param blocked_supplier: BlockedSupplier, kde possible_relation_id musí odpovídat spojení v databázi.
        :return: None
        """
        pass

    @abstractmethod
    def remove_blocked_supplier(self, blocked_supplier: BlockedSupplier) -> None:
        """
        Funkce pro odstranění záznamu o blokovaném dodavateli z databáze.
        :param blocked_supplier: BlockedSupplier, který chceme odstranit.
        :return: None
        """
        pass

    @abstractmethod
    def get_blocked_suppliers(self) -> Optional[List[BlockedSupplier]]:
        """
        Funkce pro získání všech záznamů o blokovaných dodavatelích.
        :return: List[BlockedSupplier] pokud zázanmy existují
                 None, pokud nejsou dostupné žádné záznamy
        """
        pass

    # other
    @abstractmethod
    def execute_query(self, command: str, params: Dict = None) -> Optional[List]:
        """
        Funkce pro vykonání SQL příkazu nad databází, u kterého očekáváme výstup.
        :param command: SQL příkaz
        :param params: parametry ve formě slovníku, kde klíč je jméno parametru a value je hodnota
        :return: List s výsledky, pokud jsou dostupné
                 None, pokud nejsou vráceny žádné výsledky
        """
        pass

    @abstractmethod
    def execute_non_query(self, command: str, params: Dict = None) -> None:
        """
        Funkce pro vykonání SQL příkazu, u kterého neočekáváme výslup.
        :param command: SQL příkaz
        :param params: parametry ve formě slovníku, kde klíč je jméno parametru a value je hodnota
        :return: None
        """
        pass

    @abstractmethod
    def get_contracts_for_invoice(self, invoice: Invoice) -> Optional[List[Contract]]:
        """
        Funkce pro získání smluv, které mohou být napárovány na fakturu podle IČO ministerstva a dodavatele.
        :param invoice: Invoice, pro kterou chceme vrátit navázané faktury.
        :return: List[Contract] pokud takové smlouvy existují.
                 None, pokud takové smlouvy neexistují.
        """
        pass

    @abstractmethod
    def create_warnings(self, minimal_percentage_diff: float, maximal_percentage_diff: float) -> None:
        """
        Funkce pro vytvoření záznamu o podezřelé zákázce na základě hodnoty smlouvy a součtu hodnot faktur.
        :param minimal_percentage_diff: minimální procentuelní přírustek oproti hodnotě smlouvy.
        :param maximal_percentage_diff: maximální procentuelní přírustek oproti hodnotě smlouvy.
        :return: None
        """
        pass

    @abstractmethod
    def refresh_statistics(self) -> None:
        """
        Funkce pro vytvoření statistik na základě dat, které jsou dostupné v databázi.
        :return: None
        """
        pass