from unittest import TestCase

from Configuration.Config import config
from Database.SQLAlchemyController import SQLAlchemyController


class TestSQLAlchemyController(TestCase):

    def test_connect(self):
        try:
            cont = SQLAlchemyController()
            matcher_conf = config("matcherdb")
            cont.connect(host=matcher_conf["host"], database=matcher_conf["database"], user=matcher_conf["user"],
                      password=matcher_conf["password"], port=matcher_conf["port"])
        except Exception as e:
            self.fail()

    def test_insert_contract(self):
        self.fail()

    def test_update_contract(self):
        self.fail()

    def test_remove_contract(self):
        self.fail()

    def test_get_contract(self):
        self.fail()

    def test_insert_invoice(self):
        self.fail()

    def test_insert_possible_relation(self):
        self.fail()

    def test_insert_test_result(self):
        self.fail()

    def test_update_invoice(self):
        self.fail()

    def test_remove_invoice(self):
        self.fail()

    def test_get_invoice(self):
        self.fail()

    def test_get_invoices(self):
        self.fail()

    def test_get_contracts(self):
        self.fail()

    def test_execute_query(self):
        self.fail()

    def test_execute_non_query(self):
        self.fail()
