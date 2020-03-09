from unittest import TestCase

from ContractInvoiceTests.ContractInoviceTests import ic_test_amount, ic_test_purpose
from Models.Contract import Contract
from Models.Invoice import Invoice


class TestIC_tests(TestCase):
    def test_ic_test_amount(self):
        contract = Contract(amount_different_currency=1000, amount_with_dph=2000, amount_without_dph=3000)

        invoice = Invoice(amount_in_diff_currency=1000, amount=2000, amount_without_tax=3000)
        self.assertEqual(1, ic_test_amount(invoice, contract).result)

        invoice = Invoice(amount_in_diff_currency=None, amount=None, amount_without_tax=None)
        self.assertIsNone(ic_test_amount(invoice, contract).result)

        invoice = Invoice(amount_in_diff_currency=1000, amount=None, amount_without_tax=None)
        self.assertEqual(1, ic_test_amount(invoice, contract).result)

        invoice = Invoice(amount_in_diff_currency=500, amount=None, amount_without_tax=None)
        self.assertEqual(0.5, ic_test_amount(invoice, contract).result)

        invoice = Invoice(amount_in_diff_currency=None, amount=4000, amount_without_tax=None)
        self.assertEqual(0.5, ic_test_amount(invoice, contract).result)

        invoice = Invoice(amount_in_diff_currency=None, amount=None, amount_without_tax=0)
        self.assertEqual(0, ic_test_amount(invoice, contract).result)

        invoice = Invoice(amount_in_diff_currency=500, amount=0, amount_without_tax=None)
        self.assertEqual(0.25, ic_test_amount(invoice, contract).result)

    def test_ic_test_purpose(self):
        contract = Contract(purpose="Úprava kanceláří 115 a 116 Sociálního oddělení ÚMČ Brno - Komín částečná odhlučněná příčka")
        invoice = Invoice(purpose=None)
        self.assertIsNone(ic_test_purpose(invoice, contract).result)

        invoice = Invoice(purpose="Úprava")
        self.assertEqual(6/77, ic_test_purpose(invoice, contract).result)

        invoice = Invoice(purpose="Úprava kanceláří 115 a 116 Sociálního oddělení ÚMČ Brno - Komín částečná odhlučněná příčka")
        self.assertEqual(1, ic_test_purpose(invoice, contract).result)

        invoice = Invoice(purpose="Úprava Brno 115 Komín")
        self.assertEqual(18/77, ic_test_purpose(invoice, contract).result)

        invoice = Invoice(purpose="kancelář")
        self.assertEqual(8/77, ic_test_purpose(invoice, contract).result)

        contract = Contract(purpose=None)
        invoice = Invoice(purpose="kancelář")
        self.assertEqual(None, ic_test_purpose(invoice, contract).result)