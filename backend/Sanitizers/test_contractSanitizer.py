from unittest import TestCase

from Models.Contract import Contract
from Sanitizers.ContractSanitizer import ContractSanitizer


class TestContractSanitizer(TestCase):
    def test_sanitize_contract_empty_values(self):
        test_case = ContractSanitizer.sanitize_contract(
            Contract(supplier_ico="", supplier_name="", ministry_ico="", ministry_name=""))
        res = Contract(supplier_ico=None, supplier_name=None, ministry_ico=None, ministry_name=None)
        self.assertEqual(res.supplier_name, test_case.supplier_name)
        self.assertEqual(res.supplier_ico, test_case.supplier_ico)
        self.assertEqual(res.ministry_name, test_case.ministry_name)
        self.assertEqual(res.ministry_ico, test_case.ministry_ico)

        test_case = ContractSanitizer.sanitize_contract(
            Contract(supplier_ico="", supplier_name=None, ministry_ico=None, ministry_name=""))
        res = Contract(supplier_ico=None, supplier_name=None, ministry_ico=None, ministry_name=None)
        self.assertEqual(res.supplier_name, test_case.supplier_name)
        self.assertEqual(res.supplier_ico, test_case.supplier_ico)
        self.assertEqual(res.ministry_name, test_case.ministry_name)
        self.assertEqual(res.ministry_ico, test_case.ministry_ico)

    def test_sanitize_contract_names(self):
        test_case = ContractSanitizer.sanitize_contract(Contract(supplier_name="      Ministerstvo    kultury    ",
                                                                ministry_name="      Ministerstvo    vnitra     "))
        res = Contract(supplier_name="Ministerstvo kultury", ministry_name="Ministerstvo vnitra")
        self.assertEqual(res.supplier_name, test_case.supplier_name)
        self.assertEqual(res.ministry_name, test_case.ministry_name)

    def test_sanitize_contract_icos(self):
        test_case = ContractSanitizer.sanitize_contract(Contract(supplier_ico="1234", ministry_ico="1234"))
        res = Contract(supplier_ico="00001234", ministry_ico="00001234")
        self.assertEqual(res.supplier_ico, test_case.supplier_ico)
        self.assertEqual(res.ministry_ico, test_case.ministry_ico)

        test_case = ContractSanitizer.sanitize_contract(
            Contract(supplier_ico="    as da sd 12 34    ", ministry_ico="   ?>><>\/==\'':123   "))
        res = Contract(supplier_ico="00001234", ministry_ico="00000123")
        self.assertEqual(res.supplier_ico, test_case.supplier_ico)
        self.assertEqual(res.ministry_ico, test_case.ministry_ico)

    def test_sanitize_name_spaces_before(self):
        self.assertEqual("Ministerstvo kultury", ContractSanitizer._sanitize_name("      Ministerstvo kultury"))
        self.assertEqual("Ministerstvo vnitra", ContractSanitizer._sanitize_name("                  Ministerstvo vnitra"))
        self.assertEqual("Ministerstvo kultury", ContractSanitizer._sanitize_name(" Ministerstvo kultury"))

    def test_sanitize_name_spaces_after(self):
        self.assertEqual("Ministerstvo kultury", ContractSanitizer._sanitize_name("Ministerstvo kultury      "))
        self.assertEqual("Ministerstvo kultury", ContractSanitizer._sanitize_name("Ministerstvo kultury "))

    def test_sanitize_name_spaces_between(self):
        test_case = "Ministerstvo     podohospodárstva    a     rozvoja     vidieka     Slovenskej     republiky"
        result = "Ministerstvo podohospodárstva a rozvoja vidieka Slovenskej republiky"
        self.assertEqual(result, ContractSanitizer._sanitize_name(test_case))
        self.assertEqual("Ministerstvo školství, mládeže",
                         ContractSanitizer._sanitize_name("Ministerstvo  školství,  mládeže"))

    def test_sanitize_name_spaces_combination(self):
        test_case = "     Ministerstvo     podohospodárstva    a     rozvoja     vidieka     Slovenskej     republiky    "
        result = "Ministerstvo podohospodárstva a rozvoja vidieka Slovenskej republiky"
        self.assertEqual(result, ContractSanitizer._sanitize_name(test_case))
        self.assertEqual("Ministerstvo školství, mládeže",
                         ContractSanitizer._sanitize_name("    Ministerstvo  školství,     mládeže        "))

    def test_sanitize_ico_leading_zeros(self):
        self.assertEqual(None, ContractSanitizer._sanitize_ico(None))
        self.assertEqual("00101000", ContractSanitizer._sanitize_ico("101000"))
        self.assertEqual("00164801", ContractSanitizer._sanitize_ico("164801"))
        self.assertEqual("00007064", ContractSanitizer._sanitize_ico("7064"))
        self.assertEqual("00022985", ContractSanitizer._sanitize_ico("22985"))

    def test_sanitize_ico_non_numerics(self):
        self.assertEqual(None, ContractSanitizer._sanitize_ico("  X"))
        self.assertEqual(None, ContractSanitizer._sanitize_ico("asdadsas"))
        self.assertEqual(None, ContractSanitizer._sanitize_ico("ASDASDasdasd"))
        self.assertEqual(None, ContractSanitizer._sanitize_ico(None))
        self.assertEqual("60162694", ContractSanitizer._sanitize_ico("¨60162694"))
        self.assertEqual("60162694", ContractSanitizer._sanitize_ico("asdasdas60162694asdasdasd"))
        self.assertEqual("60162694", ContractSanitizer._sanitize_ico("¨.?.60162>?>//694>>>>"))
        self.assertEqual("60162694", ContractSanitizer._sanitize_ico("6   0   1   6  2   6   9   4    "))

    def test_sanitize_ico_combination(self):
        self.assertEqual("00000012", ContractSanitizer._sanitize_ico("  12X"))
        self.assertEqual("02345678", ContractSanitizer._sanitize_ico("asdadsas     2 345 678"))
        self.assertEqual("00162694", ContractSanitizer._sanitize_ico("¨0 1 6   26 9 4 "))

    def test_sanitize_ministry_name_empty_name(self):
        test_case = ContractSanitizer._sanitize_ministry_name(Contract(ministry_ico="00023671", ministry_name=None))
        res = Contract(ministry_ico='00023671', ministry_name='Ministerstvo kultury')
        self.assertEqual(res.ministry_name, test_case.ministry_name)
        self.assertEqual(res.ministry_ico, test_case.ministry_ico)

    def test_sanitize_ministry_name_part(self):
        test_case = ContractSanitizer._sanitize_ministry_name(Contract(ministry_ico="00023671", ministry_name='Ministerstvo'))
        res = Contract(ministry_ico='00023671', ministry_name='Ministerstvo kultury')
        self.assertEqual(res.ministry_name, test_case.ministry_name)
        self.assertEqual(res.ministry_ico, test_case.ministry_ico)

    def test_sanitize_ministry_name_with_additional_text(self):
        test_case = ContractSanitizer._sanitize_ministry_name(Contract(ministry_ico="00023671", ministry_name='Česká republika - Ministerstvo kultury'))
        res = Contract(ministry_ico='00023671', ministry_name='Ministerstvo kultury')
        self.assertEqual(res.ministry_name, test_case.ministry_name)
        self.assertEqual(res.ministry_ico, test_case.ministry_ico)

    def test_sanitize_ministry_name_not_ministry(self):
        test_case = ContractSanitizer._sanitize_ministry_name(Contract(ministry_ico="00023600", ministry_name='Test s.r.o.'))
        res = Contract(ministry_ico='00023600', ministry_name='Test s.r.o.')
        self.assertEqual(res.ministry_name, test_case.ministry_name)
        self.assertEqual(res.ministry_ico, test_case.ministry_ico)

    def test_sanitize_ministry_name_ico_none(self):
        test_case = ContractSanitizer._sanitize_ministry_name(Contract(ministry_ico=None, ministry_name='Test s.r.o.'))
        res = Contract(ministry_ico=None, ministry_name='Test s.r.o.')
        self.assertEqual(res.ministry_name, test_case.ministry_name)
        self.assertEqual(res.ministry_ico, test_case.ministry_ico)

    def test_find_ico_for_name(self):
        # jedno ico
        ico = ContractSanitizer._find_ico_for_name("AURIGA SYSTEMS S.R.O.")
        self.assertEqual("28871235", ico)

        # vice vysledku
        ico = ContractSanitizer._find_ico_for_name("tes")
        self.assertIsNone(ico)

        # fyzicka osoba
        ico = ContractSanitizer._find_ico_for_name("MÜLLNEROVÁ ZDISLAVA")
        self.assertIsNone(ico)