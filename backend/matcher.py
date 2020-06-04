from typing import List
from Configuration.Config import config
from Pipelines.DecidingPipeline import DecidingPipeline
from Pipelines.FilterPipeline import FilterPipeline
from Database.SQLAlchemyController import SQLAlchemyController
from Database.DBController import DBController
from Models.models import Contract, Invoice, PossibleRelation
from Pipelines.SquashPipeline import SquashPipeline
from tqdm import tqdm
import logging


def get_relations(invoice: Invoice, contracts:List[Contract]) -> List[PossibleRelation]:
    relations = []
    if not contracts:
        return relations
    for contract in contracts:
        relations.append(PossibleRelation(invoice=invoice, contract=contract))
    return relations


def refresh_statistics(connection: DBController) -> None:
    print("Creating statistics")
    connection.refresh_statistics()
    print("statistics refreshed")


def create_warnings(connection: DBController) -> None:
    print("Creating warnings")
    connection.create_warnings(10, 100)
    print("Warnings created")

def clear_relations(connection: DBController) -> None:
    print("Clearing relations")
    connection.execute_non_query("""
                                delete from test_result where 1=1;
                                ALTER SEQUENCE test_result_test_result_id_seq RESTART;
                                
                                delete from possible_relation where 1=1;
                                ALTER SEQUENCE possible_relation_possible_relation_id_seq RESTART;
                                """)
    print("Relations cleared")


def start_matching(connection: DBController):
    page = 1
    page_size = 10000

    #get blocked suppliers and create sets with values
    blocked_suppliers = connection.get_blocked_suppliers()
    blocked_icos = set()
    blocked_names = set()
    for x in blocked_suppliers:
        if x.supplier_ico:
            blocked_icos.add(x.supplier_ico)
        if x.supplier_name:
            blocked_names.add(x.supplier_name)

    #create pipelines and prepare them
    filter_pipeline = FilterPipeline()
    filter_pipeline.prepare()
    squash_pipeline = SquashPipeline()
    squash_pipeline.prepare()
    deciding_pipeline = DecidingPipeline()
    deciding_pipeline.prepare()

    while True:
        invoices = connection.get_invoices(page=page, page_size=page_size)
        if not invoices:
            break
        else:
            page = page + 1

        for invoice in tqdm(invoices, desc=f"[{page-1}] Matching invoices"):
            if invoice.supplier_ico in blocked_icos or invoice.supplier_name in blocked_names:
                continue

            contracts = connection.get_contracts_for_invoice(invoice)
            if not contracts:
                continue
            else:
                relations = get_relations(invoice=invoice, contracts=contracts)
                passed_relations, _ = filter_pipeline.process_invoice_relations(relations)
                final_relations, other_relations = deciding_pipeline.process_invoice_relations(passed_relations)
                for relation in final_relations:
                    connection.insert_possible_relation(relation)
                for relation in other_relations:
                    connection.insert_possible_relation(relation)

            matcher_conn.commit()



if __name__ == '__main__':
    matcher_conn = SQLAlchemyController()
    matcher_conf = config("matcherdb")
    logging.debug("Connecting to the database.")
    matcher_conn.connect(host=matcher_conf["host"], database=matcher_conf["database"], user=matcher_conf["user"], password=matcher_conf["password"], port=matcher_conf["port"], echo=False)
    clear_relations(matcher_conn)
    start_matching(matcher_conn)
    logging.debug("Finished matching.")
    logging.debug("Creating warnings.")
    create_warnings(matcher_conn)
    logging.debug("Finished creating warnings.")
    logging.debug("Creating statistics.")
    refresh_statistics(matcher_conn)
    logging.debug("Finished creating statistics.")
    logging.debug("Closing session.")
    matcher_conn.session.commit()
    matcher_conn.session.close()
    logging.debug("Finished.")
