from typing import List, Generator
import psycopg2
from Models.models import Invoice
from Providers.IProvider import IProvider
from Configuration.Config import config
from tqdm import tqdm

class InvoiceProviderOpenData(IProvider):

    def __init__(self):
        """
        Konstruktor pro Invoice Provider.
        Při vytvoření si provider načte přihlašovací údaje z konfiguračního souboru.
        Není vytvořeno spojení s databází. To je vytvořeno až při vytvoření generátoru.
        """
        opendata_conf = config("opendatadb")
        self._host = opendata_conf["host"]
        self._database = opendata_conf["database"]
        self._user = opendata_conf["user"]
        self._password = opendata_conf["password"]
        self._port = opendata_conf.getint("port")

    def get_generator(self) -> Generator[Invoice, None, None]:
        """
        Funkce pro získání faktur z databáze Opendata.
        Je vytvořené spojení s databází pomocí údajů načtěných v konstruktoru.
        :return: Generátor, který při iterování extrahuje data z databáze a vrací Invoice
        """
        opendata_conn = psycopg2.connect(host=self._host, database=self._database, user=self._user,
                                         password=self._password, port=self._port)
        cur = opendata_conn.cursor()
        cur.itersize = 10000
        try:
            cur.execute("""
                select 
                    external_id,
                    auth_ico, 
                    auth_name,  
                    part_ico,
                    part_name, 
                    amount_czk,  
                    currency, 
                    subject,
                    variable_symbol, 
                    date_of_payment,
                    due_date,
                    date_created,
                    budget_item_name
                from (
                    select distinct 
                        re.record_id,
                        re.authority_identifier as external_id,
                        en_auth.ico as auth_ico, 
                        en_auth.name as auth_name,  
                        en_part.ico as part_ico,
                        en_part.name as part_name, 
                        re.amount_czk,  
                        re.currency, 
                        re.subject, 
                        re.variable_symbol, 
                        re.date_of_payment,
                        re.due_date,
                        re.date_created,
                        re.budget_category as budget_item_name
                    from public.record re
                    left join public.entity en_auth on en_auth.entity_id = re.authority
                    left join public.entity en_part on en_part.entity_id = re.partner
                    where re.record_type = 'invoice' 
                ) as res 
            """)
        except Exception as e:
            print(e)

        for line in tqdm(cur):
            yield Invoice(external_id=line[0], ministry_ico=line[1], ministry_name=line[2],
                          supplier_ico=line[3], supplier_name=line[4], amount_with_dph=line[5],
                          currency=line[6], purpose=line[7], variable_symbol=line[8],
                          date_payment=line[9], date_due=line[10], date_issue=line[11],
                          budget_item_name=line[12])
        cur.close()
        return None
