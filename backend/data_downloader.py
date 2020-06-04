from Database.SQLAlchemyController import SQLAlchemyController
from Providers.ContractProviderRegistr.CProviderRegistr import ContractProviderRegistr
from Providers.InvoiceProviderOpenData.IProviderOpenData import InvoiceProviderOpenData
from Configuration.Config import config
import logging


"""
Data Downloader

Data Downloader slouží ke stažení smluv a faktur z ministerstva
"""


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)

    matcher_conf = config('matcherdb')
    matcher_conn = SQLAlchemyController()
    log.info("Connecting to the matcherdb")
    matcher_conn.connect(host=matcher_conf["host"],
                         database=matcher_conf["database"],
                         user=matcher_conf["user"],
                         password=matcher_conf["password"],
                         port=matcher_conf["port"])
    log.info("Connected to the matcherdb")

    # log.info("Starting to download invoices from opendata database")
    # iprovier = InvoiceProviderOpenData()
    # for i, inv in enumerate(iprovier.get_generator()):
    #     matcher_conn.insert_invoice(inv)
    # matcher_conn.commit()
    # log.info("Invoices downloaded.")

    log.info("Starting to download contracts from registr")
    cprovider = ContractProviderRegistr()
    for i, con in enumerate(cprovider.get_generator()):
        log.debug(f"Inserting[{i}]: {con}")
        matcher_conn.insert_contract(con)
    matcher_conn.commit()
    log.info("Contracts downloaded.")