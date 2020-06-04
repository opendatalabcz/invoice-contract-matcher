from typing import List, Tuple

from Configuration.Config import config
from ContractInvoiceTests.CIStaticTest import CIStaticTest
from ContractInvoiceTests.MultipleContractsInvoiceTest import MCIStaticTest
from Models.models import PossibleRelation
from Pipelines.Pipeline import Pipeline

class DecidingPipeline(Pipeline):
    """
    Pipeline sloužící k otestování spojení a rozhodnutí, které je nepravdepodobnější a ostatní vyřadit.
    """
    def prepare(self):
        """
        Příprava potřebných dat. Načtení limitů.
        :return: None
        """
        self.conf = config('deciding_pipeline')
        self.minimal_score = self.conf.getint("minimal_score")
        self.invoice_count_limit = self.conf.getint("invoice_count_limit")
        self.amount_test_weight = self.conf.getfloat("amount_test")
        self.greater_amount_weight = self.conf.getfloat("greater_amount")
        self.purpose_weight = self.conf.getfloat("purpose")
        self.contract_num_weight = self.conf.getfloat("contract_num")
        self.clean_contract_num_weight = self.conf.getfloat("clean_contract_num")
        pass

    def process_invoice_relations(self, relations: List[PossibleRelation]) -> Tuple[List[PossibleRelation], List[PossibleRelation]]:
        """
        Funkce pro zpracování spojení. Cílem je vybrat jedno spojení, které bude považováno za to reálné.
        :param relations:
        :return:
        """
        num_of_relations = len(relations)

        rel_results = []

        for relation in relations:
            rel_copy = relation
            score = 0
            test_dict = {}

            test_dict["amount"] = CIStaticTest.ci_test_amount(relation.contract, relation.invoice)
            test_dict["greater_amount"] = CIStaticTest.ci_test_amount_not_greater_than_contract(relation.contract, relation.invoice)
            #purpose
            test_dict["purpose"] = CIStaticTest.ci_test_purpose(relation.contract, relation.invoice)
            test_dict["clean_contract_num"] = CIStaticTest.ci_test_clean_contract_num_in_invoice_purpose(relation.contract, relation.invoice)
            test_dict["contract_num"] = CIStaticTest.ci_test_contract_num_in_invoice_purpose(relation.contract, relation.invoice)
            #dates
            test_dict["days_after"] = CIStaticTest.ci_test_days_invoice_agreed_from_contract(relation.contract, relation.invoice)
            #other
            test_dict["valid"] = CIStaticTest.ci_test_contract_is_valid(relation.contract, relation.invoice)
            test_dict["linked"] = CIStaticTest.ci_test_contract_is_linked(relation.contract, relation.invoice)


            if test_dict["amount"].result is not None and test_dict["amount"].result > 0.9 and test_dict["amount"].result < 0.9:
                score = score + self.amount_test_weight

            if test_dict["greater_amount"].result is not None and test_dict["greater_amount"].result == 0:
                score = score + self.greater_amount_weight

            if test_dict["purpose"].result is not None and test_dict["purpose"].result >= 0.5:
                score = score + self.purpose_weight

            if test_dict["contract_num"].result is not None and test_dict["contract_num"].result == 1:
                score = score + self.contract_num_weight

            if test_dict["clean_contract_num"].result is not None and test_dict["clean_contract_num"].result == 1:
                score = score + self.clean_contract_num_weight

            rel_copy.score = score
            for test in test_dict.values():
                relation.test_results.append(test)
            rel_results.append(rel_copy)

        if not rel_results:
            return [], []

        rel_results.sort(key=lambda x: x.score, reverse=True)
        max_score = rel_results[0].score
        filtered_results = list(filter(lambda x: x.score == max_score, rel_results))

        filtered_results.sort(key=lambda x: CIStaticTest.ci_test_days_invoice_agreed_from_contract(x.contract, x.invoice).result)

        final_relation = filtered_results[0]

        if len(filtered_results) < self.invoice_count_limit:
            filtered_results.extend(rel_results[len(filtered_results):self.invoice_count_limit])

        if final_relation.score >= self.minimal_score:
            final_relation.real = True
            rest_relations = filtered_results[1:]
            for r in rest_relations:
                r.real = False
            return [final_relation], rest_relations
        else:
            return [], filtered_results















