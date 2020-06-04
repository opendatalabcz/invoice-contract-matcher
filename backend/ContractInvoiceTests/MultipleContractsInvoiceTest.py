from typing import List
import re
from Models.models import Invoice, Contract, TestResult

class MCIStaticTest:

    @staticmethod
    def mci_test_count(contracts: List[Contract], invoice: Invoice) -> TestResult:
        """
        Test pro zjištění, kolik smluv vebeme v úvahu pro jednu fakturu
        :param contracts: List[Contract], kde smlouvy mohou být navázány na fakturu
        :param invoice: faktura, ke které patří smlouvy
        :return:
        """
        test_name = "Test počtu smluv"
        return TestResult(test_name=test_name, result=len(contracts))
