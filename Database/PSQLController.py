from typing import Callable, Union, Iterable

from Database.DBController import DBController
from Models.Contract import Contract
from Models.Invoice import Invoice
from Configuration.Config import config
import psycopg2

from Models.PossibleRelation import PossibleRelation
from Sanitizers.ContractSanitizer import ContractSanitizer


class PSQLController(DBController):

    def __init__(self):
        self.cur = None

    def connect(self, config_file:str):
        params = config(config_file, section="matcherdb")
        print('Connecting to the database...')
        conn = psycopg2.connect(**params)
        self.cur = conn.cursor()
        print('Connected')

    def disconnect(self):
        if self.cur is not None:
            self.cur.close()
        else:
            pass

    def beginTransaction(self):
        print("Starting transaction...")
        self.executeNonQuery("BEGIN")
        print("Transaction started")

    def commit(self):
        print("Committing changes...")
        self.executeNonQuery("COMMIT")
        print("Changes committed")

    def rollback(self):
        print("Rollbacking changes...")
        self.executeNonQuery("BEGIN")
        print("Changes discarded")

    def insertContract(self, contract: Contract) -> None:
        command = '''INSERT INTO public.contract(external_id, version_id, link, date_published, ministry_name, 
        ministry_data_box, ministry_ico, ministry_address, ministry_department, ministry_payer_flag, supplier_name, 
        supplier_date_box, supplier_ico, supplier_address, supplier_department, supplier_receiver_flag, purpose, 
        date_agreed, contract_number, approved, amount_without_dph, amount_with_dph, amount_different_currency, 
        currency, hash_value, link_pdf, valid, linked_record) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s);'''

        params = (contract.external_id, contract.version_id, contract.link, contract.date_published, contract.ministry_name, contract.ministry_data_box, contract.ministry_ico,
            contract.ministry_address, contract.ministry_department, contract.ministry_payer_flag, contract.supplier_name, contract.supplier_date_box, contract.supplier_ico,
            contract.supplier_address, contract.supplier_department, contract.supplier_receiver_flag, contract.purpose, contract.date_agreed, contract.contract_number,
            contract.approved, contract.amount_without_dph, contract.amount_with_dph, contract.amount_different_currency, contract.currency, contract.hash_value, contract.link_pdf, contract.valid, contract.linked_record)
        # print(f"Executing insert query...: {contract}")
        self.executeNonQuery(command, params)
        # print(f"Executed.")

    def updateContract(self, contract: Contract):
        pass

    def removeContract(self, contract: Contract):
        pass

    def getContract(self, contract: Contract):
        pass

    def insertInvoice(self, invoice: Invoice):
        command = '''INSERT INTO public.invoice(ministry_ico, ministry_name, supplier_ico, supplier_name, amount, 
        currency, purpose, supplier_invoice_identifier, document_label, document_number, variable_symbol, date_acceptance, 
        date_payment, date_due, date_issue, budget_item_code, budget_item_name, contract_identifier, amount_per_item, 
        amount_without_tax, amount_in_diff_currency) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

        params = (invoice.ministry_ico, invoice.ministry_name, invoice.supplier_ico, invoice.supplier_name,
                  invoice.amount, invoice.currency, invoice.purpose, invoice.supplier_invoice_identifier,
                  invoice.document_label, invoice.document_number, invoice.variable_symbol, invoice.date_acceptance,
                  invoice.date_payment, invoice.date_due, invoice.date_issue, invoice.budget_item_code,
                  invoice.budget_item_name, invoice.contract_identifier, invoice.amount_per_item,
                  invoice.amount_without_tax, invoice.amount_in_diff_currency)

        # print(f"Executing insert query...: {invoice}")
        self.executeNonQuery(command, params)
        # print(f"Executed.")

    def updateInvoice(self, invoice: Invoice):
        pass

    def removeInvoice(self, invoice: Invoice):
        pass

    def getInvoice(self, invoice: Invoice):
        pass

    def getAllInvoices(self, custom_filter: Callable[[Invoice], bool] = None) -> Union[Iterable[Invoice], None]:
        command = """select 
                        invoice_id, ministry_ico, ministry_name, supplier_ico, supplier_name, amount, currency, 
                        purpose, supplier_invoice_identifier, document_label, document_number, variable_symbol, date_acceptance, 
                        date_payment, date_due, date_issue, budget_item_code, budget_item_name, contract_identifier, amount_per_item,
                        amount_without_tax, amount_in_diff_currency 
                     from invoice"""

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

    def getAllContracts(self, custom_filter: Callable[[Contract], bool] = None) -> Union[Iterable[Contract], None]:
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

    def executeQuery(self, command: str, params: tuple = None) -> Union[Iterable, None]:
        if self.cur is None:
            raise Exception(f"Not connected to the database. Cursor is None.")
        if params is None:
            self.cur.execute(command)
        else:
            self.cur.execute(command, params)
        results = self.cur.fetchall()
        return results

    def executeNonQuery(self, command: str, params: tuple = None) -> None:
        if self.cur is None:
            raise Exception(f"Not connected to the database. Cursor is None.")
        if params is None:
            self.cur.execute(command)
        else:
            self.cur.execute(command, params)

    def insertPossibleRelation(self, relation: PossibleRelation):
        command = '''INSERT INTO public.possible_relation(contract_id, invoice_id, final_score, final) 
                VALUES (%s, %s, %s, %s);'''
        params = (relation.contract_id, relation.invoice_id, relation.final_score, relation.final)
        self.executeNonQuery(command, params)


