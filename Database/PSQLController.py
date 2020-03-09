from typing import Callable, List, Optional

from Database.DBController import DBController
from Models.TestResult import TestResult
from Models.Contract import Contract
from Models.Invoice import Invoice
from Configuration.Config import config
import psycopg2
from Models.PossibleRelation import PossibleRelation


class PSQLController(DBController):

    def __init__(self):
        self.cur = None

    def connect(self, host: str, database: str, user: str, password=str):
        # print('Connecting to the database...')
        conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        self.cur = conn.cursor()
        # print('Connected')

    def disconnect(self):
        if self.cur is not None:
            self.cur.close()
        else:
            pass

    def begin_transaction(self):
        # print("Starting transaction...")
        self.execute_non_query("BEGIN")
        # print("Transaction started")

    def commit(self):
        # print("Committing changes...")
        self.execute_non_query("COMMIT")
        # print("Changes committed")

    def rollback(self):
        # print("Rollbacking changes...")
        self.execute_non_query("BEGIN")
        # print("Changes discarded")

    def insert_contract(self, contract: Contract) -> Optional[int]:
        command = '''INSERT INTO public.contract(external_id, version_id, link, date_published, ministry_name, 
        ministry_data_box, ministry_ico, ministry_address, ministry_department, ministry_payer_flag, supplier_name, 
        supplier_date_box, supplier_ico, supplier_address, supplier_department, supplier_receiver_flag, purpose, 
        date_agreed, contract_number, approved, amount_without_dph, amount_with_dph, amount_different_currency, 
        currency, hash_value, link_pdf, valid, linked_record) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s) RETURNING contract_id;'''

        params = [contract.external_id, contract.version_id, contract.link, contract.date_published,
                  contract.ministry_name, contract.ministry_data_box, contract.ministry_ico,
                  contract.ministry_address, contract.ministry_department, contract.ministry_payer_flag,
                  contract.supplier_name, contract.supplier_date_box, contract.supplier_ico,
                  contract.supplier_address, contract.supplier_department, contract.supplier_receiver_flag,
                  contract.purpose, contract.date_agreed, contract.contract_number,
                  contract.approved, contract.amount_without_dph, contract.amount_with_dph,
                  contract.amount_different_currency, contract.currency, contract.hash_value, contract.link_pdf,
                  contract.valid, contract.linked_record]
        # print(f"Executing insert query...: {contract}")
        res = self.execute_query(command, params)
        if res is None:
            return None
        else:
            return res[0]
        # print(f"Executed.")

    def update_contract(self, contract: Contract):
        pass

    def remove_contract(self, contract: Contract):
        pass

    def get_contract(self, contract: Contract):
        pass

    def insert_invoice(self, invoice: Invoice) -> Optional[int]:
        command = '''INSERT INTO public.invoice(ministry_ico, ministry_name, supplier_ico, supplier_name, amount, 
        currency, purpose, supplier_invoice_identifier, document_label, document_number, variable_symbol, date_acceptance, 
        date_payment, date_due, date_issue, budget_item_code, budget_item_name, contract_identifier, amount_per_item, 
        amount_without_tax, amount_in_diff_currency) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING invoice_id;'''

        params = [invoice.ministry_ico, invoice.ministry_name, invoice.supplier_ico, invoice.supplier_name,
                  invoice.amount, invoice.currency, invoice.purpose, invoice.supplier_invoice_identifier,
                  invoice.document_label, invoice.document_number, invoice.variable_symbol, invoice.date_acceptance,
                  invoice.date_payment, invoice.date_due, invoice.date_issue, invoice.budget_item_code,
                  invoice.budget_item_name, invoice.contract_identifier, invoice.amount_per_item,
                  invoice.amount_without_tax, invoice.amount_in_diff_currency]

        res = self.execute_query(command, params)
        if res is None:
            return None
        else:
            return res[0]

    def insert_possible_relation(self, relation: PossibleRelation) -> Optional[int]:
        command = '''INSERT INTO public.possible_relation(contract_id, invoice_id, final_score, final) 
                VALUES (%s, %s, %s, %s) RETURNING possible_relation_id;'''
        params = [relation.contract_id, relation.invoice_id, relation.final_score, relation.final]
        res = self.execute_query(command, params)
        if res is None:
            return None
        else:
            return res[0]

    def insert_test_result(self, testResult: TestResult) -> Optional[int]:
        command = '''INSERT INTO public.test_result(possible_relation_id, test_name, result) 
                VALUES (%s, %s, %s) RETURNING  test_result_id;'''
        params = [testResult.possible_relation_id, testResult.test_name, testResult.result]
        res = self.execute_query(command, params)
        if res is None:
            return None
        else:
            return res[0]

    def update_invoice(self, invoice: Invoice):
        pass

    def remove_invoice(self, invoice: Invoice):
        pass

    def get_invoice(self, invoice: Invoice):
        pass

    def get_invoices(self, page: int = None, page_size: int = None, custom_filter: Callable[[Invoice], bool] = None) -> \
    Optional[List[Invoice]]:
        command_without_pages = """select 
                        invoice_id, ministry_ico, ministry_name, supplier_ico, supplier_name, amount, currency, 
                        purpose, supplier_invoice_identifier, document_label, document_number, variable_symbol, date_acceptance, 
                        date_payment, date_due, date_issue, budget_item_code, budget_item_name, contract_identifier, amount_per_item,
                        amount_without_tax, amount_in_diff_currency 
                     from invoice"""
        command_with_pages = """
            select 
                invoice_id, ministry_ico, ministry_name, supplier_ico, supplier_name, amount, currency, 
                purpose, supplier_invoice_identifier, document_label, document_number, variable_symbol, date_acceptance, 
                date_payment, date_due, date_issue, budget_item_code, budget_item_name, contract_identifier, amount_per_item,
                amount_without_tax, amount_in_diff_currency 
            from (
                select 
                    inv.*
                    , row_number() over (order by invoice_id) as rn
                 from invoice inv
            ) inv 
            where rn between %s and %s 
                 """

        if page is not None and page_size is not None:
            row_start = (page_size * page) - page_size + 1
            row_end = page * page_size

            command = command_with_pages
            self.cur.execute(command, (row_start, row_end))
        else:
            command = command_without_pages
            self.cur.execute(command)

        res = []
        for line in self.cur:
            invoice = Invoice(*line)
            if custom_filter is None or custom_filter(invoice):
                res.append(invoice)

        if len(res) == 0:
            return None
        else:
            return res

    def get_contracts(self, custom_filter: Callable[[Contract], bool] = None) -> Optional[List[Contract]]:
        command = """select contract_id, external_id, version_id, link, date_published, ministry_name, ministry_data_box, 
                     ministry_ico, ministry_address, ministry_department, ministry_payer_flag, supplier_name, 
                     supplier_date_box, supplier_ico, supplier_address, supplier_department, supplier_receiver_flag, 
                     purpose, date_agreed, contract_number, approved, amount_without_dph, amount_with_dph, 
                     amount_different_currency, currency, hash_value, link_pdf, valid, linked_record from contract"""

        self.cur.execute(command)
        res = []
        for line in self.cur:
            contract = Contract(*line)
            if custom_filter is None or custom_filter(contract):
                res.append(contract)

        if len(res) == 0:
            return None
        else:
            return res

    def execute_query(self, command: str, params: List = None) -> Optional[List]:
        if self.cur is None:
            raise Exception(f"Not connected to the database. Cursor is None.")
        if params is None:
            self.cur.execute(command)
        else:
            self.cur.execute(command, params)
        results = self.cur.fetchall()
        return results

    def execute_non_query(self, command: str, params: List = None) -> None:
        if self.cur is None:
            raise Exception(f"Not connected to the database. Cursor is None.")
        if params is None:
            self.cur.execute(command)
        else:
            self.cur.execute(command, params)

    def get_contracts_for_invoice(self, invoice: Invoice) -> Optional[List[Contract]]:
        command = '''
        select distinct co.contract_id, co.external_id, co.version_id, co.link, co.date_published, co.ministry_name, co.ministry_data_box, 
        co.ministry_ico, co.ministry_address, co.ministry_department, co.ministry_payer_flag, co.supplier_name, 
        co.supplier_date_box, co.supplier_ico, co.supplier_address, co.supplier_department, co.supplier_receiver_flag, 
        co.purpose, co.date_agreed, co.contract_number, co.approved, co.amount_without_dph, co.amount_with_dph, 
        co.amount_different_currency, co.currency, co.hash_value, co.link_pdf, co.valid, co.linked_record
        --, row_number() over (order by co.contract_id, inv.invoice_id) as rn
        from contract co
        join invoice inv on inv.ministry_ico = co.ministry_ico and
                            inv.supplier_ico = co.supplier_ico
        where 
            invoice_id = %s
        '''
        params = [invoice.invoice_id]
        query_res = self.execute_query(command, params)
        res = []
        if query_res is not None:
            for line in query_res:
                res.append(Contract(*line))
            return res
        else:
            return None
