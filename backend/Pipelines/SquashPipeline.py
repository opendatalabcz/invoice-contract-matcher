from typing import List, Tuple

from Models.models import PossibleRelation
from Pipelines.Pipeline import Pipeline


class SquashPipeline(Pipeline):
    """
    Pipeline, která slouží k vyloučení spojení, které se opakují a nebo se jedná o stejnou fakturu, ale o více verzí.
    """
    def prepare(self):
        return

    def process_invoice_relations(self, relations: List[PossibleRelation]) -> Tuple[List[PossibleRelation], List[PossibleRelation]]:
        """
        Funkce, která zjistí, zda množina relací obsahuje smlouvy, které reprezentují jednu smlouvu.
        :param relations: Relace spojené s jednou fakturou.
        :return: Tuple, kde první List obsahuje relace, které testy prošli a druhý List obsahuje relace, které jsou
        druhou verzí nebo dodatky smluv v prvním listu.
        """
        passed_relations = []
        failed_relations = []

        external_id_dict = {}
        for relation in relations:
            if relation.contract.contract_id not in external_id_dict.keys():
                external_id_dict[relation.contract.contract_id] = [relation.contract]
            else:
                contracts = external_id_dict[relation.contract.contract_id]
                contracts.append(relation.contract)
                external_id_dict[relation.contract.contract_id] = contracts

        for _, contracts in external_id_dict.items():
            contracts.sort(key=lambda x: x.date_published, reverse=True)
            passed_relations.append(contracts[0])
            if contracts[1:]:
                failed_relations.append(contracts[1:])

        return (passed_relations, failed_relations)