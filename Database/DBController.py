from Models.Contract import Contract
from Models.Invoice import Invoice


class DBController:

    def connect(self, config_file: str):
        pass

    def disconnect(self):
        pass

    def insertContract(self, contract: Contract):
        pass

    def updateContract(self, contract: Contract):
        pass

    def removeContract(self, contract: Contract):
        pass

    def getContract(self, contract: Contract):
        pass

    def insertInvoice(self, invoice: Invoice):
        pass

    def updateInvoice(self, invoice: Invoice):
        pass

    def removeInvoice(self, invoice: Invoice):
        pass

    def getInvoice(self, invoice: Invoice):
        pass

    def executeQuery(self, command: str):
        pass