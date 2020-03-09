from datetime import datetime

class Invoice:
    """
    Třída reprezentující fakturu. Třída obsahuje všechny možné atributy, které může. Počítá s tím, že některé nebudou
    dostupné a proto mají všechny nastaveny výchozí hodnotu na None.
    """

    def __init__(self, invoice_id: int = None, ministry_ico: str = None, ministry_name: str = None, supplier_ico:
                 str = None, supplier_name: str = None, amount: float = None, currency: str = None, purpose: str = None,
                 supplier_invoice_identifier: str = None, document_label: str = None, document_number: str = None,
                 variable_symbol: str = None, date_acceptance: datetime = None, date_payment: datetime = None,
                 date_due: datetime = None, date_issue: datetime = None, budget_item_code: str = None,
                 budget_item_name: str = None, contract_identifier: str = None, amount_per_item: float = None,
                 amount_without_tax: float = None, amount_in_diff_currency: float = None):
        """
        Konstruktor faktury. Je navrhnut tak, aby do něj bylo možné uložit co nejvíce dat.
        :param invoice_id: Identifikátor v databázi.
        :param ministry_ico: IČO ministerstva. IČO může obsahovat úvodní nuly a proto je použit text.
        :param ministry_name: Celý název ministerstva.
        :param supplier_ico: IČO dodavatele. IČO může obsahovat úvodní nuly a proto je použit text.
        :param supplier_name: Celý název dodavatele.
        :param amount: Částka, která byla zaplacena.
        :param currency: Zkratka měny, ve které byla faktura zaplacena.
        :param purpose: Účet platby
        :param supplier_invoice_identifier: Identifikátor faktury ze systému dodavatele.
        :param document_label: Označení dokladu.
        :param document_number: Číslo dokladu.
        :param variable_symbol: Variabilní symbol.
        :param date_acceptance: Datum přijetí faktury.
        :param date_payment: Datum zaplacení faktury.
        :param date_due: Datum splatnosti faktury.
        :param date_issue: Datum vystavení faktury.
        :param budget_item_code: Kód rozpočtové položky.
        :param budget_item_name: Název rozpočtové položky.
        :param contract_identifier: Identifikátor smlouvy.
        :param amount_per_item: Částka za položku.
        :param amount_without_tax: Částka bez DPH.
        :param amount_in_diff_currency: Částka v cizí měně.
        """
        self.invoice_id = invoice_id
        self.ministry_ico = ministry_ico
        self.ministry_name = ministry_name
        self.supplier_ico = supplier_ico
        self.supplier_name = supplier_name
        self.amount = amount
        self.currency = currency
        self.purpose = purpose
        self.supplier_invoice_identifier = supplier_invoice_identifier
        self.document_label = document_label
        self.document_number = document_number
        self.variable_symbol = variable_symbol
        self.date_acceptance = date_acceptance
        self.date_payment = date_payment
        self.date_due = date_due
        self.date_issue = date_issue
        self.budget_item_code = budget_item_code
        self.budget_item_name = budget_item_name
        self.contract_identifier = contract_identifier
        self.amount_per_item = amount_per_item
        self.amount_without_tax = amount_without_tax
        self.amount_in_diff_currency = amount_in_diff_currency

    def __str__(self):
        return f"Invoice[{self.invoice_id}]: ministry_ico: {self.ministry_ico}, ministry_name: {self.ministry_name}, " \
               f"supplier_ico: {self.supplier_ico}, supplier_name: {self.supplier_name}, amount: {self.amount}, " \
               f"date_acceptance: {self.date_acceptance}"
