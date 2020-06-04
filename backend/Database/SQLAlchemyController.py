from abc import abstractmethod, ABC
from typing import Callable, Optional, List, Dict

from Database.DBController import DBController
from Models.models import Contract, Invoice, PossibleRelation, TestResult, Base, BlockedSupplier
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker, Session

class SQLAlchemyController(DBController):

    def __init__(self):
        """
        Konstruktor
        """
        self.session: Optional[Session] = None

    def connect(self, host: str, database: str, user: str, password:str, port: int, echo:bool = False):
        """
        Funkce pro připojení k databázi.
        :param host: adresa host databáze
        :param database: jméno databáze
        :param user: jméno uživatele
        :param password: heslo pro přihlášení
        :param port: port
        :param echo: Boolean hodnota určující, zda má mají být logovány informace z databáze
        :return: None
        """
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}', encoding='utf-8', echo=echo)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.session.autoflush = True
        self.session.autocommit = False
        engine.connect()


    def disconnect(self) -> None:
        """
        Funkce pro odpojení od databáze.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :return: None
        """
        assert self.session is not None
        self.session.close()


    def begin_transaction(self) -> None:
        """
        Funkce pro spuštění nové transakce.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :return: None
        """
        assert self.session is not None
        self.session.begin()

    def commit(self) -> None:
        """
        Funkce pro potvrzení změn.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :return: None
        """
        assert self.session is not None
        self.session.commit()

    def rollback(self) -> None:
        """
        Funkce pro vrácení změn poslední transakce.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :return:
        """
        assert self.session is not None
        self.session.rollback()

    # contract
    def get_contract(self, contract_id: int) -> Optional[Contract]:
        """
        Funkce pro získání smlouvy z databáze pomocí id.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param contract_id: ID smlouvy v databázi.
        :return: Contract, s odpovídajícím id, pokud existuje.
                 None, pokud neexistuje.
        """
        assert self.session is not None
        contract = self.session.query(Contract).filter(Contract.contract_id == contract_id).first()
        return contract

    def insert_contract(self, contract: Contract) -> None:
        """
        Funkce pro vložení smlouvy do databáze.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param contract: Contract, který chceme vložit.
        :return: None
        """
        assert self.session is not None
        self.session.add(contract)
        return

    def update_contract(self, contract: Contract) -> None:
        """
        Funkce pro aktualizaci smlouvy v databázi.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param contract: Contract, kde contract_id musí odpovídat smlouvě v databázi.
        :return: None
        """
        assert self.session is not None
        self.session.merge(contract)
        return

    def remove_contract(self, contract: Contract) -> None:
        """
        Funkce pro odstranění smlouvy z databáze.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param contract: Contract, který chceme odstranit.
        :return: None
        """
        assert self.session is not None
        self.session.delete(contract)
        return

    def get_contracts(self, custom_filter: Callable[[Contract], bool] = None) -> Optional[List[Contract]]:
        """
        Funkce pro získání více smluv.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param custom_filter: Nepovinný filtr, který bude aplikován na každou smlouvu.
        :return: List[Contract] pokud smlouvy existují
                 None, pokud nejsou dostupné žádné smlouvy
        """
        assert self.session is not None
        rows = self.session.query(Contract)

        if custom_filter:
            result = [x for x in rows if custom_filter(x)]
            return result
        else:
            return list(rows)

    #invoice
    def get_invoice(self, invoice_id: int) -> Optional[Invoice]:
        """
        Funkce pro získání faktury z databáze pomocí id.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param invoice_id: ID faktury v databázi.
        :return: Invoice, s odpovídajícím id, pokud existuje.
                 None, pokud neexistuje.
        """
        assert self.session is not None
        invoice = self.session.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
        return invoice

    def insert_invoice(self, invoice: Invoice) -> None:
        """
        Funkce pro vložení faktury do databáze.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param invoice: Invoice, který chceme vložit.
        :return: None
        """
        assert self.session is not None
        self.session.add(invoice)
        return

    def update_invoice(self, invoice: Invoice) -> None:
        """
        Funkce pro aktualizaci faktury v databázi.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param invoice: Invoice, kde invoice_id musí odpovídat faktuře v databázi.
        :return: None
        """
        assert self.session is not None
        self.session.merge(invoice)
        return

    def remove_invoice(self, invoice: Invoice) -> None:
        """
        Funkce pro odstranění faktury z databáze.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param invoice: Invoice, který chceme odstranit.
        :return: None
        """
        assert self.session is not None
        self.session.delete(invoice)
        return

    def get_invoices(self, page: int = None, page_size: int = None, custom_filter: Callable[[Invoice], bool] = None) -> \
    Optional[List[Invoice]]:
        """
        Funkce pro získání více faktur.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param page: číslo stránky, kterou chceme získat.
        :param page_size: Velikost stránky
        :param custom_filter: Filtr, který bude použit pro filtrování faktur.
        :return: List[Invoice] pokud smlouvy existují.
                 None, pokud nejsou dostupné žádné smlouvy.
        """
        assert self.session is not None
        rows = self.session.query(Invoice).order_by(Invoice.invoice_id).limit(page_size).offset(page * page_size)
        if custom_filter:
            result = [x for x in rows if custom_filter(x)]
            return result
        else:
            return list(rows)

    # possible_relation
    def get_possible_relation(self, possible_relation_id: int) -> Optional[PossibleRelation]:
        """
        Funkce pro získání spojení z databáze pomocí id.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param possible_relation_id: ID spojení v databázi.
        :return: PossibleRelation, s odpovídajícím id, pokud existuje.
                 None, pokud neexistuje.
        """
        assert self.session is not None
        possible_relation = self.session.query(PossibleRelation).filter(PossibleRelation.invoice_id == possible_relation_id).first()
        return possible_relation

    def insert_possible_relation(self, relation: PossibleRelation) -> None:
        """
        Funkce pro vložení spojení do databáze.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param relation: PossibleRelation, který chceme vložit.
        :return: None
        """
        assert self.session is not None
        self.session.add(relation)
        return

    def update_possible_relation(self, possible_relation: PossibleRelation) -> None:
        """
        Funkce pro aktualizaci spojení v databázi.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param possible_relation: PossibleRelation, kde possible_relation_id musí odpovídat spojení v databázi.
        :return: None
        """
        assert self.session is not None
        self.session.merge(possible_relation)
        return

    def remove_possible_relation(self, possible_relation: PossibleRelation) -> None:
        """
        Funkce pro odstranění spojení z databáze.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param possible_relation: PossibleRelation, který chceme odstranit.
        :return: None
        """
        assert self.session is not None
        self.session.delete(possible_relation)
        return

    # test_result
    def get_test_result(self, test_result_id: int) -> Optional[TestResult]:
        """
        Funkce pro získání výsledku testu z databáze pomocí id.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param test_result_id: ID výsledku testu v databázi.
        :return: TestResult, s odpovídajícím id, pokud existuje.
                 None, pokud neexistuje.
        """
        assert self.session is not None
        test_result = self.session.query(TestResult).filter(TestResult.test_result_id == test_result_id).first()
        return test_result

    def insert_test_result(self, test_result: TestResult) -> None:
        """
        Funkce pro vložení výsledku testu do databáze.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param test_result: TestResult, který chceme vložit.
        :return: None
        """
        assert self.session is not None
        self.session.add(test_result)
        return None

    def update_test_result(self, test_result: TestResult) -> None:
        """
        Funkce pro aktualizaci výsledku testu v databázi.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param test_result: TestResult, kde possible_relation_id musí odpovídat spojení v databázi.
        :return: None
        """
        assert self.session is not None
        self.session.merge(test_result)
        return

    def remove_test_result(self, test_result: TestResult) -> None:
        """
        Funkce pro odstranění výsledku testu z databáze.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param test_result: TestResult, který chceme odstranit.
        :return: None
        """
        assert self.session is not None
        self.session.delete(test_result)
        return

    # blocked supplier
    def get_blocked_supplier(self, blocked_supplier_id: int) -> BlockedSupplier:
        """
        Funkce pro získání záznamu o blokovaném dodavateli z databáze pomocí id.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param blocked_supplier_id: ID výsledku testu v databázi.
        :return: BlockedSupplier, s odpovídajícím id, pokud existuje.
                 None, pokud neexistuje.
        """
        assert self.session is not None
        blocked_supplier = self.session.query(BlockedSupplier).filter(BlockedSupplier.blocked_supplier_id == blocked_supplier_id).first()
        return blocked_supplier

    def insert_blocked_supplier(self, blocked_supplier: BlockedSupplier) -> None:
        """
        Funkce pro vložení záznamu o blokovaném dodavateli do databáze.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param blocked_supplier: BlockedSupplier, který chceme vložit.
        :return: None
        """
        assert self.session is not None
        self.session.add(blocked_supplier)
        return None

    def update_blocked_supplier(self, blocked_supplier: BlockedSupplier) -> None:
        """
        Funkce pro aktualizaci záznamu o blokovaném dodavateli testu v databázi.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param blocked_supplier: BlockedSupplier, kde possible_relation_id musí odpovídat spojení v databázi.
        :return: None
        """
        assert self.session is not None
        self.session.merge(blocked_supplier)
        return

    def remove_blocked_supplier(self, blocked_supplier: BlockedSupplier) -> None:
        """
        Funkce pro odstranění záznamu o blokovaném dodavateli z databáze.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param blocked_supplier: BlockedSupplier, který chceme odstranit.
        :return: None
        """
        assert self.session is not None
        self.session.delete(blocked_supplier)
        return

    def get_blocked_suppliers(self) -> Optional[List[BlockedSupplier]]:
        """
        Funkce pro získání všech záznamů o blokovaných dodavatelích.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :return: List[BlockedSupplier] pokud zázanmy existují
                 None, pokud nejsou dostupné žádné záznamy
        """
        assert self.session is not None
        rows = self.session.query(BlockedSupplier)
        return list(rows)

    # other
    def execute_query(self, command: str, params: Dict = None) -> Optional[List]:
        """
        Funkce pro vykonání SQL příkazu nad databází, u kterého očekáváme výstup.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param command: SQL příkaz
        :param params: parametry ve formě slovníku, kde klíč je jméno parametru a value je hodnota
        :return: List s výsledky, pokud jsou dostupné
                 None, pokud nejsou vráceny žádné výsledky
        """
        assert self.session is not None
        rows = self.session.execute(command, params=params)
        return rows


    def execute_non_query(self, command: str, params: Dict = None) -> None:
        """
        Funkce pro vykonání SQL příkazu, u kterého neočekáváme výslup.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param command: SQL příkaz
        :param params: parametry ve formě slovníku, kde klíč je jméno parametru a value je hodnota
        :return: None
        """
        assert self.session is not None
        self.session.execute(command, params=params)


    def get_contracts_for_invoice(self, invoice: Invoice) -> Optional[List[Contract]]:
        """
        Funkce pro získání smluv, které mohou být napárovány na fakturu podle IČO ministerstva a dodavatele.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param invoice: Invoice, pro kterou chceme vrátit navázané faktury.
        :return: List[Contract] pokud takové smlouvy existují.
                 None, pokud takové smlouvy neexistují.
        """
        assert self.session is not None
        rows = self.session.query(Contract).filter(Contract.ministry_ico == invoice.ministry_ico, Contract.supplier_ico == invoice.supplier_ico).all()
        return list(rows)

    def create_warnings(self, minimal_percentage_diff: float, maximal_percentage_diff: float) -> None:
        """
        Funkce pro vytvoření záznamu o podezřelé zákázce na základě hodnoty smlouvy a součtu hodnot faktur.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :param minimal_percentage_diff: minimální procentuelní přírustek oproti hodnotě smlouvy.
        :param maximal_percentage_diff: maximální procentuelní přírustek oproti hodnotě smlouvy.
        :return: None
        """
        assert self.session is not None
        command = """
            delete from contract_warning;
            insert into contract_warning (contract_id, contract_amount, invoices_amount, difference)
            select
                res.contract_id,
                res.contract_amount,
                res.invoices_amount,
                round(res.difference_percentage * 100) as difference_percentage
            from (
                select
                    war.contract_id,
                    war.contract_amount,
                    war.contract_amount_diff_curr,
                    sum(war.invoice_amount) as invoices_amount,
                    sum(war.invoice_amount_diff_curr) as invoices_amount_diff_curr,
                    sum(war.invoice_amount) - war.contract_amount as difference,
                    sum(war.invoice_amount_diff_curr) - war.contract_amount_diff_curr as difference_diff_curr,
                    (sum(war.invoice_amount) - war.contract_amount)/war.contract_amount as  difference_percentage,
                    (sum(war.invoice_amount_diff_curr) - war.contract_amount_diff_curr)/war.contract_amount_diff_curr  as difference_diff_percentage
                from (
                   select c.contract_id,
                       case
                       when coalesce(c.amount_with_dph,0) > coalesce(c.amount_without_dph, 0)
                           then coalesce(c.amount_with_dph,0)
                           else coalesce(c.amount_without_dph,0)
                       end as contract_amount,
                       c.amount_different_currency as contract_amount_diff_curr,
                       case
                       when coalesce(i.amount_with_dph,0) > coalesce(i.amount_without_dph,0)
                           then coalesce(i.amount_with_dph,0)
                           else coalesce(i.amount_without_dph,0)
                       end as invoice_amount,
                       i.amount_different_currency as invoice_amount_diff_curr
                    from contract c
                    join ministry m on c.ministry_ico = m.ministry_ico
                    join possible_relation pr on c.contract_id = pr.contract_id and pr.real = true
                    join invoice i on pr.invoice_id = i.invoice_id
                    where
                       case
                       when coalesce(c.amount_with_dph,0) > coalesce(c.amount_without_dph, 0)
                           then coalesce(c.amount_with_dph,0)
                           else coalesce(c.amount_without_dph,0)
                       end != 0
                ) war
                group by war.contract_id,
                         war.contract_amount,
                         war.contract_amount_diff_curr
            ) res
            where difference_percentage > 0 
              and round(res.difference_percentage * 100) >= :mininal_diff 
              and round(res.difference_percentage * 100) <= :maximal_diff
        """
        self.execute_non_query(command, params={"mininal_diff": minimal_percentage_diff, "maximal_diff": maximal_percentage_diff})
        return

    def refresh_statistics(self) -> None:
        """
        Funkce pro vytvoření statistik na základě dat, které jsou dostupné v databázi.
        Předpokládá, že session je připojena k databázi. Pokud ne, vyvolá AssertionError.
        :return: None
        """
        assert self.session is not None
        command = """
        delete from statistics where type like 'num%';
        insert into statistics (type, text_attribute, text_attribute_2, int_attribute, date_attribute)
        select 'num_of_contracts' as type, 
                null as text_attribute, 
               null as text_attribute_2,
               count(*) as int_attribute, 
               now() as date_Attribute 
        from contract
        join ministry m2 on contract.ministry_ico = m2.ministry_ico
        union
        select 'num_of_invoices' as type, null as text_attribute, null as text_attribute_2, count(*) as int_attribute, now() as date_Attribute from invoice
        join ministry m3 on invoice.ministry_ico = m3.ministry_ico
        union
        select 'num_of_linked' as type, null as text_attribute, null as text_attribute_2, count(*) as int_attribute, now() as date_Attribute
        from invoice i
        join possible_relation pr on i.invoice_id = pr.invoice_id and pr.real = true
        union
        select 'num_of_warnings' as type, null as text_attribute, null as text_attribute_2, count(*) as int_attribute, now() as date_Attribute from contract_warning
        union
        select 'num_contracts_per_ministry' as type, 
                m.ministry_name as text_attribute,
               null as text_attribute_2,
               count(*) as int_attribute, now() as date_Attribute from contract c
        join ministry m on c.ministry_ico = m.ministry_ico
        group by m.ministry_name
        union
        select 'num_invoices_per_ministry' as type, m.ministry_name as text_attribute,
               null as text_attribute_2,
               count(*) as int_attribute, 
               now() as date_Attribute 
        from invoice i
        join ministry m on i.ministry_ico = m.ministry_ico
        group by m.ministry_name
        union
        select
               'num_contracts_per_month' as type,
               to_char(co.date_published, 'YYYY_MM') as text_attribute,
               null as text_attribute_2,
               count(co.contract_id) as int_attribute, now() as date_Attribute
        from contract co
        join ministry m on co.ministry_ico = m.ministry_ico
        group by to_char(co.date_published, 'YYYY_MM')
        union
        select
               'num_invoices_per_month' as type,
               to_char(iv.date_issue, 'YYYY_MM') as text_attribute,
               null as text_attribute_2,
               count(iv.invoice_id) as int_attribute, now() as date_Attribute
        from invoice iv
        join ministry m on iv.ministry_ico = m.ministry_ico
        group by to_char(iv.date_issue, 'YYYY_MM')
        union
        select
               'num_invoices_per_month_ministry' as type,
               m.shortcut as text_attribute,
               to_char(iv.date_issue, 'YYYY') as text_attribute_2,
               count(iv.invoice_id) as int_attribute, now() as date_Attribute
        from invoice iv
        join ministry m on iv.ministry_ico = m.ministry_ico
        group by to_char(iv.date_issue, 'YYYY'), m.shortcut
        union
        select
               'num_contracts_per_month_ministry' as type,
               m.shortcut as text_attribute,
               to_char(co.date_agreed, 'YYYY') as text_attribute_2,
               count(co.contract_id) as int_attribute, now() as date_Attribute
        from contract co
        join ministry m on co.ministry_ico = m.ministry_ico
        group by to_char(co.date_agreed, 'YYYY'), m.shortcut
        union
         select 'num_of_contracts_ministry' as type, 
               m2.shortcut as text_attribute, 
               null as text_attribute_2,
               count(*) as int_attribute, 
               now() as date_Attribute 
        from contract
        join ministry m2 on contract.ministry_ico = m2.ministry_ico
        group by m2.shortcut 
        union
        select 'num_of_invoices_ministry' as type, m3.shortcut as text_attribute, null as text_attribute_2, count(*) as int_attribute, now() as date_Attribute from invoice
        join ministry m3 on invoice.ministry_ico = m3.ministry_ico
        group by m3.shortcut
        union
        select 'num_of_linked_ministry' as type, m3.shortcut as text_attribute, null as text_attribute_2, count(*) as int_attribute, now() as date_Attribute
        from invoice i
        join ministry m3 on i.ministry_ico = m3.ministry_ico
        join possible_relation pr on i.invoice_id = pr.invoice_id and pr.real = true
        group by m3.shortcut
        union
        select 'num_of_warnings_ministry' as type, shortcut as text_attribute, null as text_attribute_2, count(*) as int_attribute, now() as date_Attribute from (
             select * from contract_warning cw 
             join contract c on cw.contract_id = c.contract_id
             join ministry m on c.ministry_ico = m.ministry_ico
        ) as res
        group by res.shortcut
        order by 1
        """
        self.execute_non_query(command)
        return