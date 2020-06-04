import datetime
from unittest import TestCase
from ContractInvoiceTests.CIStaticTest import CIStaticTest
from Models.models import Contract, Invoice

class TestIC_tests(TestCase):
    def test_ci_test_amount(self):
        tester = CIStaticTest()
        contract = Contract(amount_different_currency=1000, amount_with_dph=2000, amount_without_dph=3000)

        invoice = Invoice(amount_different_currency=1000, amount_with_dph=2000, amount_without_dph=3000)
        self.assertEqual(1, tester.ci_test_amount(contract, invoice).result)

        invoice = Invoice()
        self.assertIsNone( tester.ci_test_amount(contract, invoice).result)

        invoice = Invoice(amount_different_currency=1000, )
        self.assertEqual(1, tester.ci_test_amount(contract, invoice).result)

        invoice = Invoice(amount_different_currency=500, )
        self.assertEqual(0.5, tester.ci_test_amount(contract, invoice).result)

        invoice = Invoice(amount_with_dph=4000, )
        self.assertEqual(0.5, tester.ci_test_amount(contract, invoice).result)

        invoice = Invoice(amount_without_dph=0)
        self.assertEqual(0, tester.ci_test_amount(contract, invoice).result)

        invoice = Invoice(amount_different_currency=500, amount_with_dph=0, )
        self.assertEqual(0.25, tester.ci_test_amount(contract, invoice).result)

    def test_ci_test_purpose(self):
        tester = CIStaticTest()
        contract = Contract(purpose="Úprava kanceláří 115 a 116 Sociálního oddělení ÚMČ Brno - Komín částečná odhlučněná příčka")
        invoice = Invoice()
        self.assertIsNone(tester.ci_test_purpose(contract, invoice).result)

        invoice = Invoice(purpose="Úprava")
        self.assertEqual(6/77, tester.ci_test_purpose(contract, invoice).result)

        invoice = Invoice(purpose="Úprava kanceláří 115 a 116 Sociálního oddělení ÚMČ Brno - Komín částečná odhlučněná příčka")
        self.assertEqual(1, tester.ci_test_purpose(contract, invoice).result)

        invoice = Invoice(purpose="Úprava Brno 115 Komín")
        self.assertEqual(18/77, tester.ci_test_purpose(contract, invoice).result)

        invoice = Invoice(purpose="kancelář")
        self.assertEqual(8/77, tester.ci_test_purpose(contract, invoice).result)

        contract = Contract()
        invoice = Invoice(purpose="kancelář")
        self.assertEqual(None, tester.ci_test_purpose(contract, invoice).result)

    def test_ci_test_ammount_not_greater_than_contract(self):
        tester = CIStaticTest()

        contract = Contract(amount_with_dph=11000, amount_without_dph=10000)
        invoice = Invoice()
        self.assertIsNone(tester.ci_test_amount_not_greater_than_contract(contract, invoice).result)

        contract = Contract()
        invoice = Invoice()
        self.assertIsNone(tester.ci_test_amount_not_greater_than_contract(contract, invoice).result)

        contract = Contract()
        invoice = Invoice(amount_with_dph=11000, amount_without_dph=10000)
        self.assertIsNone(tester.ci_test_amount_not_greater_than_contract(contract, invoice).result)

        contract = Contract(amount_with_dph=1000000, )
        invoice = Invoice(amount_with_dph=11000, amount_without_dph=10000)
        self.assertEqual(1, tester.ci_test_amount_not_greater_than_contract(contract, invoice).result)

        contract = Contract(amount_without_dph=1000000)
        invoice = Invoice(amount_with_dph=11000, amount_without_dph=10000)
        self.assertEqual(1, tester.ci_test_amount_not_greater_than_contract(contract, invoice).result)

        contract = Contract(amount_without_dph=11000)
        invoice = Invoice(amount_with_dph=1000000, )
        self.assertEqual(0, tester.ci_test_amount_not_greater_than_contract(contract, invoice).result)

        contract = Contract(amount_with_dph=11000, )
        invoice = Invoice(amount_without_dph=1000000)
        self.assertEqual(0, tester.ci_test_amount_not_greater_than_contract(contract, invoice).result)

        contract = Contract(amount_without_dph=11000)
        invoice = Invoice(amount_with_dph=11000, amount_without_dph=10000)
        self.assertEqual(1, tester.ci_test_amount_not_greater_than_contract(contract, invoice).result)

        contract = Contract(amount_without_dph=10999)
        invoice = Invoice(amount_with_dph=11000, amount_without_dph=10000)
        self.assertEqual(0, tester.ci_test_amount_not_greater_than_contract(contract, invoice).result)

    def test_ci_test_contract_num_in_invoice_purpose(self):
        tester = CIStaticTest()

        contract = Contract()
        invoice = Invoice()
        self.assertEqual(0, tester.ci_test_contract_num_in_invoice_purpose(contract, invoice).result)

        contract = Contract(contract_number = "test")
        invoice = Invoice(purpose = "plnění povinností dle smlouvy 165710581 - údržba lesních porostů, prevence šíření")
        self.assertEqual(0, tester.ci_test_contract_num_in_invoice_purpose(contract, invoice).result)

        contract = Contract(contract_number="165710500")
        invoice = Invoice(purpose="plnění povinností dle smlouvy 165710581 - údržba lesních porostů, prevence šíření")
        self.assertEqual(0, tester.ci_test_contract_num_in_invoice_purpose(contract, invoice).result)

        contract = Contract(contract_number="165710581")
        invoice = Invoice(purpose="plnění povinností dle smlouvy 165710581 - údržba lesních porostů, prevence šíření")
        self.assertEqual(1, tester.ci_test_contract_num_in_invoice_purpose(contract, invoice).result)

        contract = Contract(contract_number="165/7105/81")
        invoice = Invoice(purpose="plnění povinností dle smlouvy 165710581 - údržba lesních porostů, prevence šíření")
        self.assertEqual(0, tester.ci_test_contract_num_in_invoice_purpose(contract, invoice).result)

        contract = Contract(contract_number="10/2017-MSP-CES")
        invoice = Invoice(purpose="5166 - právní služby - veřejné zakázky IT, smlouva 10/2017-MSP-CES")
        self.assertEqual(1, tester.ci_test_contract_num_in_invoice_purpose(contract, invoice).result)

    def test_ci_test_clean_contract_num_in_invoice_purpose(self):
        tester = CIStaticTest()

        contract = Contract()
        invoice = Invoice()
        self.assertEqual(0, tester.ci_test_clean_contract_num_in_invoice_purpose(contract, invoice).result)

        contract = Contract(contract_number="test")
        invoice = Invoice(purpose="plnění povinností dle smlouvy 165710581 - údržba lesních porostů, prevence šíření")
        self.assertEqual(0, tester.ci_test_clean_contract_num_in_invoice_purpose(contract, invoice).result)

        contract = Contract(contract_number="165710500")
        invoice = Invoice(purpose="plnění povinností dle smlouvy 165710581 - údržba lesních porostů, prevence šíření")
        self.assertEqual(0, tester.ci_test_clean_contract_num_in_invoice_purpose(contract, invoice).result)

        contract = Contract(contract_number="165710581")
        invoice = Invoice(purpose="plnění povinností dle smlouvy 165710581 - údržba lesních porostů, prevence šíření")
        self.assertEqual(1, tester.ci_test_clean_contract_num_in_invoice_purpose(contract, invoice).result)

        contract = Contract(contract_number="165/7105/81")
        invoice = Invoice(purpose="plnění povinností dle smlouvy 165710581 - údržba lesních porostů, prevence šíření")
        self.assertEqual(1, tester.ci_test_clean_contract_num_in_invoice_purpose(contract, invoice).result)

        contract = Contract(contract_number="10/2017-MSP-CES")
        invoice = Invoice(purpose="5166 - právní služby - veřejné zakázky IT, smlouva 10/2017-MSP-CES")
        self.assertEqual(0, tester.ci_test_clean_contract_num_in_invoice_purpose(contract, invoice).result)

    def test_ci_test_contract_is_valid(self):
        tester = CIStaticTest()

        contract = Contract()
        invoice = Invoice()
        self.assertIsNone(tester.ci_test_contract_is_valid(contract, invoice).result)

        contract = Contract(valid='2')
        self.assertIsNone(tester.ci_test_contract_is_valid(contract, invoice).result)


        contract = Contract(valid='-1')
        self.assertIsNone(tester.ci_test_contract_is_valid(contract, invoice).result)

        contract = Contract(valid='valid')
        self.assertIsNone(tester.ci_test_contract_is_valid(contract, invoice).result)

        contract = Contract(valid='1')
        self.assertEqual(1, tester.ci_test_contract_is_valid(contract, invoice).result)

        contract = Contract(valid='0')
        self.assertEqual(0, tester.ci_test_contract_is_valid(contract, invoice).result)

    def test_ci_test_months_invoice_agreed_from_contract(self):
        tester = CIStaticTest()

        contract = Contract()
        invoice = Invoice()
        self.assertIsNone(tester.ci_test_days_invoice_agreed_from_contract(contract, invoice).result)

        contract = Contract(date_agreed = datetime.datetime(day=1, month=1, year=2000))
        invoice = Invoice()
        self.assertIsNone(tester.ci_test_days_invoice_agreed_from_contract(contract, invoice).result)

        contract = Contract()
        invoice = Invoice(date_issue = datetime.datetime(day=1, month=1, year=2000))
        self.assertIsNone(tester.ci_test_days_invoice_agreed_from_contract(contract, invoice).result)

        contract = Contract(date_agreed = datetime.datetime(day=1, month=1, year=2000))
        invoice = Invoice(date_issue = datetime.datetime(day=1, month=1, year=2000))
        self.assertEqual(0, tester.ci_test_days_invoice_agreed_from_contract(contract, invoice).result)

        contract = Contract(date_agreed = datetime.datetime(day=1, month=1, year=2000))
        invoice = Invoice(date_issue = datetime.datetime(day=2, month=1, year=2000))
        self.assertEqual(1, tester.ci_test_days_invoice_agreed_from_contract(contract, invoice).result)

        contract = Contract(date_agreed=datetime.datetime(day=2, month=1, year=2000))
        invoice = Invoice(date_issue=datetime.datetime(day=1, month=1, year=2000))
        self.assertEqual(-1, tester.ci_test_days_invoice_agreed_from_contract(contract, invoice).result)

        contract = Contract(date_agreed=datetime.datetime(day=1, month=1, year=2000))
        invoice = Invoice(date_issue=datetime.datetime(day=1, month=2, year=2000))
        self.assertEqual(31, tester.ci_test_days_invoice_agreed_from_contract(contract, invoice).result)

        contract = Contract(date_agreed=datetime.datetime(day=1, month=1, year=2000))
        invoice = Invoice(date_issue=datetime.datetime(day=1, month=1, year=2001))
        self.assertEqual(366, tester.ci_test_days_invoice_agreed_from_contract(contract, invoice).result)

        contract = Contract(date_agreed=datetime.datetime(day=1, month=1, year=2001))
        invoice = Invoice(date_issue=datetime.datetime(day=1, month=1, year=2002))
        self.assertEqual(365, tester.ci_test_days_invoice_agreed_from_contract(contract, invoice).result)

        contract = Contract(date_agreed=datetime.datetime(day=1, month=1, year=2000))
        invoice = Invoice(date_issue=datetime.datetime(day=1, month=1, year=2010))
        self.assertEqual(3653, tester.ci_test_days_invoice_agreed_from_contract(contract, invoice).result)

        contract = Contract(date_agreed=datetime.datetime(day=1, month=1, year=2010))
        invoice = Invoice(date_issue=datetime.datetime(day=1, month=1, year=2000))
        self.assertEqual(-3653, tester.ci_test_days_invoice_agreed_from_contract(contract, invoice).result)

        contract = Contract(date_agreed=datetime.datetime(day=1, month=1, year=2000, hour=1, minute=1, second=1))
        invoice = Invoice(date_issue=datetime.datetime(day=1, month=1, year=2010))
        self.assertEqual(3652, tester.ci_test_days_invoice_agreed_from_contract(contract, invoice).result)

        contract = Contract(date_agreed=datetime.datetime(day=1, month=1, year=2000, hour=23, minute=59, second=59))
        invoice = Invoice(date_issue=datetime.datetime(day=1, month=1, year=2010))
        self.assertEqual(3652, tester.ci_test_days_invoice_agreed_from_contract(contract, invoice).result)

        contract = Contract(date_agreed=datetime.datetime(day=1, month=1, year=2000))
        invoice = Invoice(date_issue=datetime.datetime(day=1, month=1, year=2010, hour=1, minute=1, second=1))
        self.assertEqual(3653, tester.ci_test_days_invoice_agreed_from_contract(contract, invoice).result)

        contract = Contract(date_agreed=datetime.datetime(day=1, month=1, year=2000))
        invoice = Invoice(date_issue=datetime.datetime(day=1, month=1, year=2010, hour=23, minute=59, second=59))
        self.assertEqual(3653, tester.ci_test_days_invoice_agreed_from_contract(contract, invoice).result)
