from datetime import datetime


class Contract:
    """
    Třída reprezentující smlouvu. Třída obsahuje všechny atributy, které obsahuje smlouva v registru smluv.
    Atributy nejsou povinné a proto mají nastavenou výchozí hodnotu na None.
    """

    def __init__(self, contract_id: int = None, external_id: str = None, version_id: str = None, link: str = None,
                 date_published: datetime = None, ministry_name: str = None, ministry_data_box: str = None,
                 ministry_ico: str = None, ministry_address: str = None, ministry_department: str = None,
                 ministry_payer_flag: str = None, supplier_name: str = None, supplier_date_box: str = None,
                 supplier_ico: str = None, supplier_address: str = None, supplier_department: str = None,
                 supplier_receiver_flag: str = None, purpose: str = None, date_agreed: datetime = None,
                 contract_number: str = None, approved: str = None, amount_without_dph: float = None,
                 amount_with_dph: float = None, amount_different_currency: float = None, currency: str = None,
                 hash_value: str = None, link_pdf: str = None, attachments: list = None, valid: str = None,
                 linked_record:str = None):
        """
        Konstruktor smlouvy. Je navrhnut tak, aby do něj bylo možné uložit co nejvice dat.
        :param contract_id: Identifikátor smlouvy v databazi.
        :param external_id: Identifikátor smlouvy v registru smluv.
        :param version_id: Verze záznamu.
        :param link: url Odkazující na záznam v registu smluv.
        :param date_published: Datum zvěřejnění.
        :param ministry_name: Celé jméno ministerstva.
        :param ministry_data_box: Datová schránka ministerstva.
        :param ministry_ico: IČO ministerstva.
        :param ministry_address: Adresa ministerstva.
        :param ministry_department: Odbor ministerstva.
        :param ministry_payer_flag: Flag, který označuje, že je ministerstvo plátce ve vztahu ke smlouvě.
        :param supplier_name: Celé jméno dodavatele.
        :param supplier_date_box: Datová schránka dodavatele.
        :param supplier_ico: IČO dodavatele.
        :param supplier_address: Adresa dodavatele.
        :param supplier_department: Odbor nebo část dodavatele.
        :param supplier_receiver_flag: Flag, který označuje, že je dodavatel příjmce ve vztahu ke smlouvě.
        :param purpose: Předmět smlouvy.
        :param date_agreed: Datum uzavření.
        :param contract_number: Číslo smlouvy (nemusí se nutně jednat o číslo).
        :param approved: Jméno osoby, které smlouvu schválila.
        :param amount_without_dph: Částka bez DPH.
        :param amount_with_dph: Částka s DPH.
        :param amount_different_currency: Částka v cizí měně.
        :param currency: Cizí měna.
        :param hash_value: Hash hodnota smlouvy.
        :param link_pdf: URL odakzující na smlouvu v pdf.
        :param attachments: list příloh. Pokud žádné nejsou, může být None.
        :param valid: Označení, zda je záznam platný.
        :param linked_record: Identifikátor smlouvy, ke které je tato smlouva navázána.
        """
        self.contract_id = contract_id
        self.external_id = external_id
        self.version_id = version_id
        self.link = link
        self.date_published = date_published
        self.ministry_name = ministry_name
        self.ministry_data_box = ministry_data_box
        self.ministry_ico = ministry_ico
        self.ministry_address = ministry_address
        self.ministry_department = ministry_department
        self.ministry_payer_flag = ministry_payer_flag
        self.supplier_name = supplier_name
        self.supplier_date_box = supplier_date_box
        self.supplier_ico = supplier_ico
        self.supplier_address = supplier_address
        self.supplier_department = supplier_department
        self.supplier_receiver_flag = supplier_receiver_flag
        self.purpose = purpose
        self.date_agreed = date_agreed
        self.contract_number = contract_number
        self.approved = approved
        self.amount_without_dph = amount_without_dph
        self.amount_with_dph = amount_with_dph
        self.amount_different_currency = amount_different_currency
        self.currency = currency
        self.hash_value = hash_value
        self.link_pdf = link_pdf
        self.attachments = attachments
        self.valid = valid
        self.linked_record = linked_record

    def __str__(self):
        return f"Contract[{self.contract_id}]: m_name: {self.ministry_name}, m_ico: {self.ministry_ico}, " \
               f"s_name: {self.supplier_name}, s_ico: {self.supplier_ico}, agreed: {self.date_agreed}, " \
               f"amount: {self.amount_with_dph}"

