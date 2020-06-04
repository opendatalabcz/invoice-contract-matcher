from typing import List, Tuple

from ContractInvoiceTests.CIStaticTest import CIStaticTest
from Database.DBController import DBController
from Models.models import PossibleRelation, Invoice, Contract
from Pipelines.Pipeline import Pipeline


class FilterPipeline(Pipeline):
    """
    Pipeline sloužící k vyfiltrování spojení, které můžeme ignorovat, protože porušují pravidla, která musí platit
    """

    def prepare(self):
        """
        Příprava potřebných dat.
        :return: None
        """
        pass

    def process_invoice_relations(self, relations: List[PossibleRelation]) -> Tuple[List[PossibleRelation], List[PossibleRelation]]:
        """
        Funkce pro otestování spojení. Tato funkce spustí povinné testy, které kontrolují pravidla které musí platit
        mezi fakturou a smlouvou.
        :param relations: List spojení, které chceme otestovat
        :return: Tuple, kde první List obsahuje spojení, pro které pravidla platí a druhý List obsahuje spojení, pro
        které jedno nebo více pravidel neplatí
        """
        passed_relations = []
        failed_relations = []

        for relation in relations:
            test_result = CIStaticTest.ci_test_invoice_contract_dates(relation.contract, relation.invoice)
            # relation.test_results.append(test_result)

            if test_result.result == 0:
                failed_relations.append(relation)
            else:
                passed_relations.append(relation)

        return (passed_relations, failed_relations)