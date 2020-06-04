from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Contract(Base):
    """
    Třída reprezentující smlouvu. Třída obsahuje všechny atributy, které obsahuje smlouva v registru smluv.
    Atributy nejsou povinné a proto mají nastavenou výchozí hodnotu na None.

    :param __tablename__: Název korespondující tabulce v databázi.
    :param contract_id: Identifikátor smlouvy v databazi.
    :param external_id: Identifikátor smlouvy v registru smluv.
    :param version_id: Verze záznamu.
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
    :param date_published: Datum zvěřejnění.
    :param date_agreed: Datum uzavření.
    :param date_expiry: Datum uzavření.
    :param amount_without_dph: Částka bez DPH.
    :param amount_with_dph: Částka s DPH.
    :param amount_different_currency: Částka v cizí měně.
    :param contract_number: Číslo smlouvy (nemusí se nutně jednat o číslo).
    :param approved: Jméno osoby, které smlouvu schválila.
    :param currency: Cizí měna.
    :param valid: Označení, zda je záznam platný.
    :param linked_record: Identifikátor smlouvy, ke které je tato smlouva navázána.
    :param link: url Odkazující na záznam v registu smluv.

    """

    __tablename__ = 'contract'

    contract_id = Column(Integer, primary_key=True)
    external_id = Column(String)
    version_id = Column(String)
    ministry_name = Column(String)
    ministry_data_box = Column(String)
    ministry_ico = Column(String)
    ministry_address = Column(String)
    ministry_department = Column(String)
    ministry_payer_flag = Column(String)
    supplier_name = Column(String)
    supplier_date_box = Column(String)
    supplier_ico = Column(String)
    supplier_address = Column(String)
    supplier_department = Column(String)
    supplier_receiver_flag = Column(String)
    purpose = Column(String)
    date_published = Column(DateTime)
    date_agreed = Column(DateTime)
    date_expiry = Column(DateTime)
    amount_without_dph = Column(Float)
    amount_with_dph = Column(Float)
    amount_different_currency = Column(Float)
    contract_number = Column(String)
    approved = Column(String)
    currency = Column(String)
    valid = Column(String)
    linked_record = Column(String)
    link = Column(String)

    possible_relations = relationship("PossibleRelation", back_populates="contract", lazy='select', cascade=None)

    def __str__(self):
        return f"Contract[{self.contract_id}]: m_name: {self.ministry_name}, m_ico: {self.ministry_ico}, " \
               f"s_name: {self.supplier_name}, s_ico: {self.supplier_ico}, agreed: {self.date_agreed}, " \
               f"amount: {self.amount_with_dph}"

class Invoice(Base):
    """
    Třída reprezentující fakturu. Třída obsahuje všechny možné atributy, které může. Počítá s tím, že některé nebudou
    dostupné a proto mají všechny nastaveny výchozí hodnotu na None.

    :param __tablename__: Název korespondující tabulce v databázi.
    :param invoice_id: Identifikátor v databázi.
    :param external_id: Indentifikátor ve zdroji dat.
    :param ministry_ico: IČO ministerstva. IČO může obsahovat úvodní nuly a proto je použit text.
    :param ministry_name: Celý název ministerstva.
    :param supplier_ico: IČO dodavatele. IČO může obsahovat úvodní nuly a proto je použit text.
    :param supplier_name: Celý název dodavatele.
    :param purpose: Účet platby
    :param date_acceptance: Datum přijetí faktury.
    :param date_payment: Datum zaplacení faktury.
    :param date_due: Datum splatnosti faktury.
    :param date_issue: Datum vystavení faktury.
    :param amount_with_dph: Částka s DPH.
    :param amount_without_dph: Částka bez DPH.
    :param amount_different_currency: Částka v cizí měně.
    :param amount_per_item: Částka za položku.
    :param currency: Zkratka měny, ve které byla faktura zaplacena.
    :param supplier_invoice_identifier: Identifikátor faktury ze systému dodavatele.
    :param variable_symbol: Variabilní symbol.
    :param document_label: Označení dokladu.
    :param document_number: Číslo dokladu.
    :param budget_item_code: Kód rozpočtové položky.
    :param budget_item_name: Název rozpočtové položky.
    :param contract_identifier: Identifikátor smlouvy.
    """

    __tablename__ = 'invoice'

    invoice_id = Column(Integer, primary_key=True)
    external_id = Column(String)
    ministry_ico = Column(String)
    ministry_name = Column(String)
    supplier_ico = Column(String)
    supplier_name = Column(String)
    purpose = Column(String)
    date_acceptance = Column(DateTime)
    date_payment = Column(DateTime)
    date_due = Column(DateTime)
    date_issue = Column(DateTime)
    amount_with_dph = Column(Float)
    amount_without_dph = Column(Float)
    amount_different_currency = Column(Float)
    amount_per_item = Column(Float)
    currency = Column(String)
    supplier_invoice_identifier = Column(String)
    variable_symbol = Column(String)
    document_label = Column(String)
    document_number = Column(String)
    budget_item_code = Column(String)
    budget_item_name = Column(String)
    contract_identifier = Column(String)

    possible_relations = relationship("PossibleRelation", back_populates="invoice", lazy='select', cascade=None)

    def __str__(self):
        return f"Invoice[{self.invoice_id}]: ministry_ico: {self.ministry_ico}, ministry_name: {self.ministry_name}, " \
               f"supplier_ico: {self.supplier_ico}, supplier_name: {self.supplier_name}, amount: {self.amount_with_dph}, " \
               f"date_acceptance: {self.date_acceptance}"

class PossibleRelation(Base):
    """
    Třída, která je má sloužit k reprezentaci možného spojení mezi smlouvou a fakturou

    :param __tablename__: Název korespondující tabulce v databázi.
    :param possible_relation_id: Identifikátor spojení v databazi.
    :param invoice_id: Identifikátor faktury v databázi
    :param contract_id: Identifikátor smlouvy v databázi
    :param score: Score, které bylo spojení přiřazeno.
    :param real: Bool hodnota, která označuje spojení za reálné.

    :param test_results: Výsledky jednotlivých testů
    :param contract: Smlouva, které se spojení týká
    :param invoice: Faktura, které se spojení týká
    """

    __tablename__ = 'possible_relation'

    possible_relation_id = Column(Integer, primary_key=True)

    score = Column(Float)
    real = Column(Boolean)
    invoice_id = Column(Integer, ForeignKey('invoice.invoice_id'))
    contract_id = Column(Integer, ForeignKey('contract.contract_id'))

    contract = relationship("Contract", back_populates="possible_relations")
    invoice = relationship("Invoice", back_populates="possible_relations")
    test_results = relationship("TestResult", back_populates="possible_relation")

    def __str__(self):
        return f"PossibleRelation [{self.possible_relation_id}]: contract_id: {None if self.contract is None else self.contract.contract_id}, " \
               f"invoice_id: {self.invoice.invoice_id}, score: {self.score}, real: {self.real}"

class TestResult(Base):
    """
    Třída pro reprezentaci testu provedeného na spojení mezi fakturou a smlouvou

    :param __tablename__: Název korespondující tabulce v databázi.
    :param test_result_id: Identifikator výsledku v databázi
    :param possible_relation_id: Identifikator spojení v databázi
    :param test_name: Jméno testu
    :param result: Číselná hodnota, která vyjadřuje výsledek testu. Možné hodnoty výsldku určuje test, který výsledek vytvořil.
    """

    __tablename__ = 'test_result'

    test_result_id = Column(Integer, primary_key=True)
    possible_relation_id = Column(Integer, ForeignKey('possible_relation.possible_relation_id'))
    test_name = Column(String)
    result = Column(Float)

    possible_relation = relationship("PossibleRelation", back_populates="test_results")

    def __str__(self):
        return f"TestResult[{self.test_result_id}] test_name: {self.test_name}, result: {self.result}"

class BlockedSupplier(Base):
    """
    Třída pro reprezentaci záznamu v tabulce blocked_supplier

    :param __tablename__: Název korespondující tabulce v databázi.
    :param blocked_supplier_id: Identifikátor blokovaného dodavatele v databázi.
    :param supplier_name: Jméno dodavatele.
    :param supplier_ico: IČO dodavatele.
    """

    __tablename__ = 'blocked_supplier'

    blocked_supplier_id = Column(Integer, primary_key=True)
    supplier_name = Column(String)
    supplier_ico = Column(String)

    def __str__(self):
        return f"BlockedSupplier[{self.blocked_supplier_id}] supplier_name: {self.supplier_name}, supplier_ico: {self.supplier_ico}"