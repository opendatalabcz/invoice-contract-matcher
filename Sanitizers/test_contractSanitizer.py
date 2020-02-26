from unittest import TestCase

from Models.Contract import Contract
from Sanitizers import ContractSanitizer


class TestContractSanitizer(TestCase):
    def test_sanitizeContract_empty_values(self):
        test_case = ContractSanitizer.sanitizeContract(
            Contract(supplier_ico="", supplier_name="", ministry_ico="", ministry_name=""))
        res = Contract(supplier_ico=None, supplier_name=None, ministry_ico=None, ministry_name=None)
        self.assertEqual(res.supplier_name, test_case.supplier_name)
        self.assertEqual(res.supplier_ico, test_case.supplier_ico)
        self.assertEqual(res.ministry_name, test_case.ministry_name)
        self.assertEqual(res.ministry_ico, test_case.ministry_ico)

        test_case = ContractSanitizer.sanitizeContract(
            Contract(supplier_ico="", supplier_name=None, ministry_ico=None, ministry_name=""))
        res = Contract(supplier_ico=None, supplier_name=None, ministry_ico=None, ministry_name=None)
        self.assertEqual(res.supplier_name, test_case.supplier_name)
        self.assertEqual(res.supplier_ico, test_case.supplier_ico)
        self.assertEqual(res.ministry_name, test_case.ministry_name)
        self.assertEqual(res.ministry_ico, test_case.ministry_ico)

    def test_sanitizeContract_names(self):
        test_case = ContractSanitizer.sanitizeContract(Contract(supplier_name="      Ministerstvo    kultury    ",
                                                                ministry_name="      Ministerstvo    vnitra     "))
        res = Contract(supplier_name="Ministerstvo kultury", ministry_name="Ministerstvo vnitra")
        self.assertEqual(res.supplier_name, test_case.supplier_name)
        self.assertEqual(res.ministry_name, test_case.ministry_name)

    def test_sanitizeContract_icos(self):
        test_case = ContractSanitizer.sanitizeContract(Contract(supplier_ico="1234", ministry_ico="1234"))
        res = Contract(supplier_ico="00001234", ministry_ico="00001234")
        self.assertEqual(res.supplier_ico, test_case.supplier_ico)
        self.assertEqual(res.ministry_ico, test_case.ministry_ico)

        test_case = ContractSanitizer.sanitizeContract(
            Contract(supplier_ico="    as da sd 12 34    ", ministry_ico="   ?>><>\/==\'':123   "))
        res = Contract(supplier_ico="00001234", ministry_ico="00000123")
        self.assertEqual(res.supplier_ico, test_case.supplier_ico)
        self.assertEqual(res.ministry_ico, test_case.ministry_ico)

    def test_sanitizeName_spaces_before(self):
        self.assertEqual("Ministerstvo kultury", ContractSanitizer.sanitizeName("      Ministerstvo kultury"))
        self.assertEqual("Ministerstvo vnitra", ContractSanitizer.sanitizeName("                  Ministerstvo vnitra"))
        self.assertEqual("Ministerstvo kultury", ContractSanitizer.sanitizeName(" Ministerstvo kultury"))

    def test_sanitizeName_spaces_after(self):
        self.assertEqual("Ministerstvo kultury", ContractSanitizer.sanitizeName("Ministerstvo kultury      "))
        self.assertEqual("Ministerstvo kultury", ContractSanitizer.sanitizeName("Ministerstvo kultury "))

    def test_sanitizeName_spaces_between(self):
        test_case = "Ministerstvo     podohospodárstva    a     rozvoja     vidieka     Slovenskej     republiky"
        result = "Ministerstvo podohospodárstva a rozvoja vidieka Slovenskej republiky"
        self.assertEqual(result, ContractSanitizer.sanitizeName(test_case))
        self.assertEqual("Ministerstvo školství, mládeže",
                         ContractSanitizer.sanitizeName("Ministerstvo  školství,  mládeže"))

    def test_sanitizeName_spaces_combination(self):
        test_case = "     Ministerstvo     podohospodárstva    a     rozvoja     vidieka     Slovenskej     republiky    "
        result = "Ministerstvo podohospodárstva a rozvoja vidieka Slovenskej republiky"
        self.assertEqual(result, ContractSanitizer.sanitizeName(test_case))
        self.assertEqual("Ministerstvo školství, mládeže",
                         ContractSanitizer.sanitizeName("    Ministerstvo  školství,     mládeže        "))

    def test_sanitizeICO_leading_zeros(self):
        self.assertEqual(None, ContractSanitizer.sanitizeICO(None))
        self.assertEqual("00101000", ContractSanitizer.sanitizeICO("101000"))
        self.assertEqual("00164801", ContractSanitizer.sanitizeICO("164801"))
        self.assertEqual("00007064", ContractSanitizer.sanitizeICO("7064"))
        self.assertEqual("00022985", ContractSanitizer.sanitizeICO("22985"))

    def test_sanitizeICO_non_numerics(self):
        self.assertEqual(None, ContractSanitizer.sanitizeICO("  X"))
        self.assertEqual(None, ContractSanitizer.sanitizeICO("asdadsas"))
        self.assertEqual(None, ContractSanitizer.sanitizeICO("ASDASDasdasd"))
        self.assertEqual(None, ContractSanitizer.sanitizeICO(None))
        self.assertEqual("60162694", ContractSanitizer.sanitizeICO("¨60162694"))
        self.assertEqual("60162694", ContractSanitizer.sanitizeICO("asdasdas60162694asdasdasd"))
        self.assertEqual("60162694", ContractSanitizer.sanitizeICO("¨.?.60162>?>//694>>>>"))
        self.assertEqual("60162694", ContractSanitizer.sanitizeICO("6   0   1   6  2   6   9   4    "))

    def test_sanitizeICO_combination(self):
        self.assertEqual("00000012", ContractSanitizer.sanitizeICO("  12X"))
        self.assertEqual("02345678", ContractSanitizer.sanitizeICO("asdadsas     2 345 678"))
        self.assertEqual("00162694", ContractSanitizer.sanitizeICO("¨0 1 6   26 9 4 "))

    def test_sanitizeMinistryName_empty_name(self):
        test_case = ContractSanitizer.sanitizeMinistryName(Contract(ministry_ico="00023671", ministry_name=None))
        res = Contract(ministry_ico='00023671', ministry_name='Ministerstvo kultury')
        self.assertEqual(res.ministry_name, test_case.ministry_name)
        self.assertEqual(res.ministry_ico, test_case.ministry_ico)

    def test_sanitizeMinistryName_part(self):
        test_case = ContractSanitizer.sanitizeMinistryName(Contract(ministry_ico="00023671", ministry_name='Ministerstvo'))
        res = Contract(ministry_ico='00023671', ministry_name='Ministerstvo kultury')
        self.assertEqual(res.ministry_name, test_case.ministry_name)
        self.assertEqual(res.ministry_ico, test_case.ministry_ico)

    def test_sanitizeMinistryName_with_additional_text(self):
        test_case = ContractSanitizer.sanitizeMinistryName(Contract(ministry_ico="00023671", ministry_name='Česká republika - Ministerstvo kultury'))
        res = Contract(ministry_ico='00023671', ministry_name='Ministerstvo kultury')
        self.assertEqual(res.ministry_name, test_case.ministry_name)
        self.assertEqual(res.ministry_ico, test_case.ministry_ico)

    def test_sanitizeMinistryName_not_ministry(self):
        test_case = ContractSanitizer.sanitizeMinistryName(Contract(ministry_ico="00023600", ministry_name='Test s.r.o.'))
        res = Contract(ministry_ico='00023600', ministry_name='Test s.r.o.')
        self.assertEqual(res.ministry_name, test_case.ministry_name)
        self.assertEqual(res.ministry_ico, test_case.ministry_ico)

    def test_sanitizeMinistryName_ico_none(self):
        test_case = ContractSanitizer.sanitizeMinistryName(Contract(ministry_ico=None, ministry_name='Test s.r.o.'))
        res = Contract(ministry_ico=None, ministry_name='Test s.r.o.')
        self.assertEqual(res.ministry_name, test_case.ministry_name)
        self.assertEqual(res.ministry_ico, test_case.ministry_ico)