

class PossibleRelation:
    def __init__(self, possible_relation_id: int = None, contract_id: int = None, invoice_id: str = None,
                       final_score: float = None, final: bool = False):
        self.possible_relation_id = possible_relation_id
        self.contract_id = contract_id
        self.invoice_id = invoice_id
        self.final_score = final_score
        self.final = final

    def __str__(self):
        return f"PossibleRelation [{self.possible_relation_id}]: contract_id: {self.contract_id}, invoice_id: {self.invoice_id}, " \
               f"final_score: {self.final_score}, final: {self.final}"
