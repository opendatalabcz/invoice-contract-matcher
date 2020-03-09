from typing import Callable, Optional, List

from Models.Contract import Contract
from Models.Invoice import Invoice
from Models.PossibleRelation import PossibleRelation
from Models.TestResult import TestResult


class DBController:

    def connect(self, host: str, database: str, user: str, password=str):
        pass

    def disconnect(self):
        pass

    def begin_transaction(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def insert_contract(self, contract: Contract) -> Optional[int]:
        pass

    def update_contract(self, contract: Contract):
        pass

    def remove_contract(self, contract: Contract):
        pass

    def get_contract(self, contract: Contract):
        pass

    def insert_invoice(self, invoice: Invoice) -> Optional[int]:
        pass

    def insert_possible_relation(self, relation: PossibleRelation) -> Optional[int]:
        pass

    def insert_test_result(self, testResult: TestResult) -> Optional[int]:
        pass

    def update_invoice(self, invoice: Invoice):
        pass

    def remove_invoice(self, invoice: Invoice):
        pass

    def get_invoice(self, invoice: Invoice):
        pass

    def get_invoices(self, page: int = None, page_size: int = None, custom_filter: Callable[[Invoice], bool] = None) -> \
    Optional[List[Invoice]]:
        pass

    def get_contracts(self, custom_filter: Callable[[Contract], bool] = None) -> Optional[List[Contract]]:
        pass

    def execute_query(self, command: str, params: List = None) -> Optional[List]:
        pass

    def execute_non_query(self, command: str, params: List = None) -> None:
        pass

    def get_contracts_for_invoice(self, invoice: Invoice) -> Optional[List[Contract]]:
        pass