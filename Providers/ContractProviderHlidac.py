import urllib3
import json

from Providers.ContractProvider import Provider

icos = ["66002222",  # Ministerstvo pro místní rozvoj
        "00164801",  # Ministerstvo životního prostředí
        "00551023",  # Ministerstvo práce a sociálních věcí
        "00007064",  # Ministerstvo vnitra
        "45769851",  # Ministerstvo zahraničních věcí
        "60162694",  # Ministerstvo obrany
        "47609109",  # Ministerstvo průmyslu a obchodu
        "00024341",  # Ministerstvo zdravotnictví
        "00025429",  # Ministerstvo spravedlnosti
        "00006947",  # Ministerstvo financí
        "00022985",  # Ministerstvo školství, mládeže a tělovýchovy
        "30416094",  # Ministerstvo dopravy
        "00020478",  # Ministerstvo zemědělství
        "00023671",  # Ministerstvo kultury
        ]

class InvoiceProvider(Provider):

    def __init__(self, ico):
        self.ico = ico
        self.page = 1
        self.http = urllib3.PoolManager()

    def getInvoices(self, page):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token ...'
        }

        request = self.http.request(
            method='GET',
            url=f'https://www.hlidacstatu.cz/api/v1/DatasetSearch/ministry-invoices?q=ico%3A{self.ico}&page={page}&sort=dateCreated&desc=0',
            headers=headers)

        if request.status != 200:
            print(f"[{request.status}] {request.data}")
            return False, request.data
        data = json.loads(request.data)
        if data["total"] == 0:
            return False, request.data
        results = data["results"]
        # print(f"[{request.status}] {json.dumps(results, indent=4, sort_keys=True)}")
        return True, results

    def getAll(self):
        pass

    # TODO - predelat na iterator
    def getNext(self):
        flag, data = self.getInvoices(self.page)
        if flag:
            self.page += 1
            return data

        # with open(f"faktury/{ico}.json", "w+", encoding='utf-8') as file:
        #     print(f"Getting data for ico: {ico}")
        #
        #     flag, data = self.getInvoices(ico, 1)
        #     if flag:
        #         print(f"Data: {json.dumps(data, indent=4, sort_keys=True)}")
        #         file.write(f"{json.dumps(data, indent=4, sort_keys=True)}\n")
        #     file.close()

# for ico in icos:
#     with open(f"{ico}.json", "w+", encoding='utf-8') as file:
#         print(f"Getting data for ico: {ico}")
#
#         flag, data = InvoiceProvider(ico).getInvoices(1)
#         if flag:
#             print(f"Data: {json.dumps(data, indent=4, sort_keys=True)}")
#             file.write(f"{json.dumps(data, indent=4, sort_keys=True)}\n")
#         file.close()