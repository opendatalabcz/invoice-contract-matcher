import psycopg2
from abc import abstractmethod, ABC
from Models.Invoice import Invoice
from Configuration.Config import config


class InvoiceProviderOpenData:

    @staticmethod
    def get_invoices(config_file: str, page: int, page_size: int) -> list:
        row_start = (page_size * page) - page_size + 1
        row_end = page * page_size

        invoices = []
        conn = None
        try:
            params = config(filename=config_file, section="opendatadb")
            print('Connecting to the database...')
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("""
                select 
                    auth_ico, 
                    auth_name,  
                    part_ico,
                    part_name, 
                    amount_czk,  
                    currency, 
                    subject,
                    supplier_invoice_identifier,
                    document_label,
                    document_number, 
                    variable_symbol, 
                    date_of_acceptence,
                    date_of_payment,
                    due_date,
                    date_created,
                    budget_item_code,
                    budget_item_name,
                    contract_identifier,
                    amount_per_item,
                    amount_without_tax,
                    amount_in_diff_currency
                from (
                    select distinct 
                        re.record_id,
                        en_auth.ico as auth_ico, 
                        en_auth.name as auth_name,  
                        en_part.ico as part_ico,
                        en_part.name as part_name, 
                        re.amount_czk,  
                        re.currency, 
                        re.subject,
                        null as supplier_invoice_identifier,
                        null as document_label,
                        null as document_number, 
                        re.variable_symbol, 
                        null as date_of_acceptence,
                        re.date_of_payment,
                        re.due_date,
                        re.date_created,
                        null as budget_item_code,
                        re.budget_category as budget_item_name,
                        null as contract_identifier,
                        null as amount_per_item,
                        null as amount_without_tax,
                        null as amount_in_diff_currency,
                        row_number() OVER (ORDER BY re.record_id) AS rn
                    from public.record re
                    left join public.entity en_auth on en_auth.entity_id = re.authority
                    left join public.entity en_part on en_part.entity_id = re.partner
                    where re.record_type = 'invoice' 
                ) as res 
                where res.rn >= %s and res.rn <= %s
            """, (row_start, row_end))

            results = cur.fetchall()
            cur.close()

            for line in results:
                # print(line)
                invoices.append(Invoice(None, *line))
        except Exception as e:
            print(e)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
        return invoices

    @staticmethod
    def getAllInvoices(config_file: str):
        invoices = []
        conn = None
        try:
            params = config(config_file, "opendatadb")
            # print('Connecting to the database...')
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("""
                select distinct
                    en_auth.ico as auth_ico, 
                    en_auth.name as auth_name,  
                    en_part.ico as part_ico,
                    en_part.name as part_name, 
                    re.amount_czk,  
                    re.currency, 
                    re.subject,
                    null as supplier_invoice_identifier,
                    null as document_label,
                    null as document_number, 
                    re.variable_symbol, 
                    null as date_of_acceptence,
                    re.date_of_payment,
                    re.due_date,
                    re.date_created,
                    re.budget_category as budget_item_code,
                    null as budget_item_name,
                    null as contract_identifier,
                    null as amount_per_item,
                    null as amount_without_tax,
                    null as amount_in_diff_currency
                from public.record re
                left join public.entity en_auth on en_auth.entity_id = re.authority
                left join public.entity en_part on en_part.entity_id = re.partner
                where re.record_type = 'invoice'
            """)

            results = cur.fetchall()
            for line in results:
                # print(line)
                invoices.append(Invoice(*line))
            cur.close()
        except Exception as e:
            print(e)
        finally:
            if conn is not None:
                conn.close()
                # print('Database connection closed.')
        return invoices
