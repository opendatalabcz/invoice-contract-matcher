from typing import Callable, Iterable, Optional, List

from Configuration.Config import config
from Database.PSQLController import PSQLController
from Decorators.Timer import timer
from Models.Contract import Contract
from Models.Invoice import Invoice
from Models.TestResult import TestResult
from Models.PossibleRelation import PossibleRelation
from Providers.ContractProviderRegistr.ContractProviderRegistr import ContractProviderRegistr
from Providers.InoviceProviderOpenData.InvoiceProviderOpenData import InvoiceProviderOpenData
from tqdm import tqdm
from ContractInvoiceTests.ContractInoviceTests import ic_test_amount, ic_test_purpose


@timer
def download_all_contracts_and_push_to_db(connection: PSQLController) -> None:
    links = ContractProviderRegistr.get_available_files()
    for link in links:
        contracts = ContractProviderRegistr.get_contracts_with_link(link, custom_filter=None)
        connection.begin_transaction()
        try:
            for contract in tqdm(contracts, desc="Uploading contracts:"):
                # res = ContractSanitizer.sanitizeContract(contract)
                connection.insert_contract(contract)
            connection.commit()
        except Exception as e:
            print(f"Exception during inserting contract to the database: {e}")
            connection.rollback()
            connection.disconnect()
            raise
    connection.disconnect()

@timer
def download_all_invoices_and_push_to_db(connection: PSQLController) -> None:
    page = 1
    page_size = 100000
    connection = connection

    while True:
        invoices = InvoiceProviderOpenData.get_invoices(config_file="./Database/database.ini", page=page, page_size=page_size)
        if len(invoices) == 0:
            break

        try:
            connection.begin_transaction()
            for invoice in tqdm(invoices, desc="Uploading invoices"):
                # print(f"Inserting {invoice}")
                connection.insert_invoice(invoice)
            connection.commit()
        except Exception as e:
            print(f"[Page: {page}, Page_size: {page_size}] Exception during inserting invoice to the database: {e}")
            connection.rollback()
            connection.disconnect()
            raise
        page += 1
    connection.disconnect()

def match_invoice(connection: PSQLController, invoice: Invoice, tests: Optional[List[Callable[[Invoice, Contract], TestResult]]]) -> None:
    connection = connection
    contracts = connection.get_contracts_for_invoice(invoice)
    if contracts is None:
        return
    relations = []
    print(f"\tFound {len(contracts)} contracts")
    for contract in contracts:
        # print(contract)
        rel = PossibleRelation(None, contract_id=contract.contract_id, invoice_id=invoice.invoice_id, final_score=None, final=False)
        possible_relation_id = connection.insert_possible_relation(relation=rel)
        relations.append(rel)
        print(f"\tRelation inserted: {possible_relation_id}")

        if tests is not None and len(tests) != 0:
            for test in tests:
                test_result = test(invoice, contract)
                test_result.possible_relation_id = possible_relation_id
                test_result_id = connection.insert_test_result(test_result)
                print(f"\tTest result inserted: id: {test_result_id}, result: {test_result.result}")


    if len(relations)==0:
        rel = PossibleRelation(None, contract_id=None, invoice_id=invoice.invoice_id, final_score=0, final=True)
        possible_relation_id = connection.insert_possible_relation(relation=rel)
        print(f"\tEmpty Relation inserted: {possible_relation_id}")


def start_matching(connection: PSQLController):
    page = 1
    page_size = 1000
    while True:
        invoices = connection.get_invoices(page=page, page_size=page_size, custom_filter=None)
        connection.begin_transaction()
        if invoices is None:
            break
        else:
            page = page + 1
        for invoice in tqdm(invoices, desc="Matching invoices"):
            match_invoice(connection=connection, invoice=invoice, tests=[ic_test_amount, ic_test_purpose])
        connection.commit()


conn = PSQLController()
configuration = config("./Database/database.ini", "matcherdb")
conn.connect(host=configuration["host"], database=configuration["database"], user=configuration["user"], password=configuration["password"])
start_matching(conn)

