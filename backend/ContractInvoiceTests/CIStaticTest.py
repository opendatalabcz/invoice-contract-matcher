from typing import List
import re
from Models.models import Invoice, Contract, TestResult


class CIStaticTest:

    @staticmethod
    def ci_test_amount(contract: Contract, invoice: Invoice) -> TestResult:
        """
        Test mezi smlouvou a fakturou. Vyhodnotí procentualni rozdil mezi cenami, které jsou uvedené ve faktuře a
        smlouvě a poté výsledky zprůměruje a vrátí.
        Test porovnává cenu bez dph, cenu s dph, cenu v jiné měně. Pokud je jedna ze dvou položek None, tak se do
        finálního výsledku nezapočítává. Porovnání je vždy použito tak, aby se menší hodnota porovnívala s větší a
        výsledek nebude nikdy větší než 1.
        :param contract: smlouva, kterou chceme porovnat
        :param invoice: faktura, kterou chceme porovnat
        :return: TestResult s hodnotou result:
        1 pokud jsou všechny atributy stejné, nebo jen ty, které mají obě hodnoty neprázdné.
        0.5 v případě že faktura nebo smlouva má poloviční hodnotu oprovi druhému objektu.
        None pokud není u každé ceny je aspoň jeden prázdný
        """
        test_name = "Amount of money"
        result = None
        results = []
        if invoice.amount_with_dph is not None and contract.amount_with_dph is not None:
            max_value = max(invoice.amount_with_dph, contract.amount_with_dph)
            min_value = min(invoice.amount_with_dph, contract.amount_with_dph)
            results.append(min_value / max_value)

        if invoice.amount_without_dph is not None and contract.amount_without_dph is not None:
            max_value = max(invoice.amount_without_dph, contract.amount_without_dph)
            min_value = min(invoice.amount_without_dph, contract.amount_without_dph)
            results.append(min_value / max_value)

        if invoice.amount_different_currency is not None and contract.amount_different_currency is not None:
            max_value = max(invoice.amount_different_currency, contract.amount_different_currency)
            min_value = min(invoice.amount_different_currency, contract.amount_different_currency)
            results.append(min_value / max_value)
        if len(results) != 0:
            result = sum(results) / len(results)
        return TestResult(result=result, test_name=test_name)

    @staticmethod
    def ci_test_purpose(contract: Contract, invoice: Invoice) -> TestResult:
        """
        Test, který testuje počet stejných slov v předmětu smlouvy a faktury. Výsledkem je počet písmen slov,
        které se shodují vydělené počtem písmen celkem ve faktuře.
        :param contract: smlouva, kterou chceme porovnat
        :param invoice: faktura, kterou chceme porovnat
        :return: TestResult s hodnotou result:
        1 pokud jsou všechny slova stejná.
        0 pokud žádné slovo není stejné.
        None pokud je předmět smolouvy nebo faktury prázdný
        """
        test_name = "Same words in purpose"
        if invoice.purpose is not None and contract.purpose is not None:
            parts = invoice.purpose.split(" ")
            num_of_chars = len(invoice.purpose.replace(" ", ""))
            if num_of_chars == 0:
                return TestResult(test_name=test_name)
            num_of_matched = 0
            for part in parts:
                if part in contract.purpose:
                    num_of_matched = num_of_matched + len(part)
            res = num_of_matched / num_of_chars
            return TestResult(result=res, test_name=test_name)
        else:
            return TestResult(test_name=test_name)

    @staticmethod
    def ci_test_amount_not_greater_than_contract(contract: Contract, invoice: Invoice) -> TestResult:
        """
        Test, který vybere maximální cenu uvnitř faktury a smlouvy a porovná, zda je hodnota faktury menší než smlouvy.
        :param contract: smlouva, kterou chceme porovnat
        :param invoice: faktura, kterou chceme porovnat
        :return: TestResult s hodnotou result:
        1 pokud je maximální hodnota faktury menší než maximální hodnota smlouvy.
        0 pokud je hodnota faktury větší než smlouvy
        None pokud fakura nebo smlouva nemá žádnou cenu definovanou
        """
        test_name = "Max amount of the invoice is smaller then max contract price"

        invoice_max_amount = list(filter(lambda v: v is not None, [invoice.amount_without_dph, invoice.amount_with_dph]))
        contract_max_amount = list(filter(lambda v: v is not None, [contract.amount_without_dph, contract.amount_with_dph]))

        if invoice_max_amount and contract_max_amount:
            max_invoice = max(invoice_max_amount)
            max_contract = max(contract_max_amount)

            if max_invoice <= max_contract:
                return TestResult(result=1, test_name=test_name)
            else:
                return TestResult(result=0, test_name=test_name)
        else:
            return TestResult(test_name=test_name)

    @staticmethod
    def ci_test_clean_contract_num_in_invoice_purpose(contract: Contract, invoice: Invoice) -> TestResult:
        """
        Test, který zjistí, zda je číslo smlouvy (contract number) uvnitř předmětu faktury. Před porovnáním jsou
        z čísla smlouvy odraněny všechny nečíselné znaky
        :param contract: smlouva, kterou chceme porovnat
        :param invoice: faktura, kterou chceme porovnat
        :return: TestResult s hodnotou result:
        1 pokud číslo smlouvy (bez nečíselných znaků) je v předmětu faktury
        0 pokud číslo smlouvy není v předmětu faktury
        """
        test_name = "contract number (only numeric characters) in the purpose of the invoice"
        if contract.contract_number is not None and len(contract.contract_number) >= 5 and invoice.purpose is not None and re.sub("[^0-9]", "", contract.contract_number) is not "" and invoice.purpose.find(re.sub("[^0-9]", "", contract.contract_number)) != -1 :
            return TestResult(result=1, test_name=test_name)
        else:
            return TestResult(result=0, test_name=test_name)

    @staticmethod
    def ci_test_contract_num_in_invoice_purpose(contract: Contract, invoice: Invoice) -> TestResult:
        """
        Test, který zjistí, zda je číslo smlouvy (contract number) uvnitř předmětu faktury.
        :param contract: smlouva, kterou chceme porovnat
        :param invoice: faktura, kterou chceme porovnat
        :return: TestResult s hodnotou result:
        1 pokud číslo smlouvy je v předmětu faktury
        0 pokud číslo smlouvy není v předmětu faktury
        """
        test_name = "contract number in the purpose of the invoice"

        if contract.contract_number is not None and len(contract.contract_number) >= 5 and invoice.purpose is not None and invoice.purpose.lower().find(contract.contract_number.lower()) != -1:
            return TestResult(result=1, test_name=test_name)
        else:
            return TestResult(result=0, test_name=test_name)

    @staticmethod
    def ci_test_invoice_contract_dates(contract: Contract, invoice: Invoice) -> TestResult:
        """
        Test, který kontroluje zda faktura ke smlouvě může patřit na základě časových údajů.
        :param contract: smlouva, kterou chceme porovnat
        :param invoice: faktura, kterou chceme porovnat
        :return: TestResult s hodnotou result:
        1 pokud je spojení možné (invoice.date_issue, invoice.date_payment, invoice.date_acceptance, invoice.date_due jsou po vytvoření smlouvy)
        0 pokud spojení není možné
        None, pokud datum všechny časové údaje faktury jsou None nebo podepsání smlouvy je None
        """
        test_name = "invoice date issued after contract agreed"


        if (invoice.date_issue is not None or invoice.date_acceptance is not None or invoice.date_payment is not None or invoice.date_due is not None) and contract.date_agreed is not None:
            if contract.date_agreed <= min(x for x in [invoice.date_issue, invoice.date_payment, invoice.date_acceptance, invoice.date_due] if x is not None):
                return TestResult(result=1, test_name=test_name)
            else:
                return TestResult(result=0, test_name=test_name)
        else:
            return TestResult(test_name=test_name)



    @staticmethod
    def ci_test_contract_is_valid(contract: Contract, invoice: Invoice) -> TestResult:
        """
        Test, který kontroluje, zda je smlouva platná v Registru smluv
        :param contract: smlouva, kterou chceme porovnat
        :param invoice: faktura, kterou chceme porovnat
        :return: TestResult s hodnotou result:
        1 pokud je smlouva platná
        0 pokud platní není
        None pokud je atribut valid je prázdný nebo se nerovná definovaným hodnotám.
        """
        test_name = "Contract validity check"
        if contract.valid is not None:
            if contract.valid == '1':
                return TestResult(result=1, test_name=test_name)
            elif contract.valid == '0':
                return TestResult(result=0, test_name=test_name)
        return TestResult(test_name=test_name)

    @staticmethod
    def ci_test_contract_is_linked(contract: Contract, invoice: Invoice) -> TestResult:
        """
        Test, který zjistí, zda je je smlouva provázaná s jinou smlouvou.
        :param contract: smlouva, kterou chceme porovnat
        :param invoice: faktura, kterou chceme porovnat
        :return: TestResult s hodnotou result:
        1 pokud je hodnota linked_record neprázdná
        0 pokud je hodnota prázdná
        """
        test_name = "Check if contract has linked_record"
        if contract.linked_record is not None:
            return TestResult(result=1, test_name=test_name)
        else:
            return TestResult(result=0, test_name=test_name)

    @staticmethod
    def ci_test_days_invoice_agreed_from_contract(contract: Contract, invoice: Invoice) -> TestResult:
        """
        Test, který vrátí počet dní vytvoření faktury od data uzavření smlouvy. Pokud je fakuktura vykázána před
        vytvořením smlouvy, vrací záporné číslo.
        :param contract: smlouva, kterou chceme porovnat
        :param invoice: faktura, kterou chceme porovnat
        :return: TestResult s hodnotou result:
        Pokud je datum vytvoření faktury po uzavření smlouvy, je vrácen kladné celé číslo odpovídající počtu dnů.
        V opačném případě je vráceno záporně celé číslo odpovídající počtu dnů.
        Pokud datum vystavení faktury nebo datum uzavření smlouvy je prázdné, poté je vrácen result roven None
        """
        test_name = "Get number of months invoice issued from contract agreed"
        if invoice.date_issue is not None and contract.date_agreed is not None:
            res = (invoice.date_issue - contract.date_agreed).days
            return TestResult(result=res, test_name=test_name)
        else:
            return TestResult(test_name=test_name)