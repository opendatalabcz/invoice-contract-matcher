from typing import Optional


class TestResult:

    def __init__(self, test_result_id: object, possible_relation_id: object, test_name: object, result: object):
        self.test_result_id = test_result_id
        self.possible_relation_id = possible_relation_id
        self.test_name = test_name
        self.result = result
