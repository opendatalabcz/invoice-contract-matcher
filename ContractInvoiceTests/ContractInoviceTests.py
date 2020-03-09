from typing import Optional

from Models.Invoice import Invoice
from Models.Contract import Contract
from Models.TestResult import TestResult


def ic_test_amount(invoice: Invoice, contract: Contract) -> TestResult:
    test_name = "Amount of money"
    result = None
    results = []
    if invoice.amount is not None and contract.amount_with_dph is not None:
        max_value = max(invoice.amount, contract.amount_with_dph)
        min_value = min(invoice.amount, contract.amount_with_dph)
        results.append(min_value/max_value)

    if invoice.amount_without_tax is not None and contract.amount_without_dph is not None:
        max_value = max(invoice.amount_without_tax, contract.amount_without_dph)
        min_value = min(invoice.amount_without_tax, contract.amount_without_dph)
        results.append(min_value/max_value)

    if invoice.amount_in_diff_currency is not None and contract.amount_different_currency is not None:
        max_value = max(invoice.amount_in_diff_currency, contract.amount_different_currency)
        min_value = min(invoice.amount_in_diff_currency, contract.amount_different_currency)
        results.append(min_value/max_value)
    if len(results) != 0:
        result = sum(results) / len(results)
    return TestResult(test_result_id=None, possible_relation_id=None, result=result, test_name=test_name)


def ic_test_purpose(invoice: Invoice, contract: Contract) -> TestResult:
    test_name = "Same words in purpose"
    if invoice.purpose is not None and contract.purpose is not None:
        parts = invoice.purpose.split(" ")
        num_of_chars = len(contract.purpose.replace(" ", ""))
        num_of_matched = 0
        for part in parts:
            if part in contract.purpose:
                num_of_matched = num_of_matched + len(part)
        res = num_of_matched/num_of_chars
        return TestResult(test_result_id=None, possible_relation_id=None, result=res, test_name=test_name)
    else:
        return TestResult(test_result_id=None, possible_relation_id=None, result=None, test_name=test_name)

