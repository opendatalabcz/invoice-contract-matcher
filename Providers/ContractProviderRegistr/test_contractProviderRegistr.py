from unittest import TestCase

from Models.Contract import Contract
from Providers.ContractProviderRegistr.ContractProviderRegistr import ContractProviderRegistr
import xml.etree.ElementTree as ET
from datetime import datetime

class TestContractProviderRegistr(TestCase):
    def test_get_file_name(self):
        self.assertEqual("dump_2020_10.xml", ContractProviderRegistr.get_file_name(year=2020, month=10))
        self.assertEqual("dump_2019_01.xml", ContractProviderRegistr.get_file_name(year=2019, month=1))
        self.assertRaises(Exception, ContractProviderRegistr.get_file_name, 2020, 100)
        self.assertRaises(Exception, ContractProviderRegistr.get_file_name, 999, 1)

    def test_trim_tag_name(self):
        self.assertEqual("testtext",
                         ContractProviderRegistr.trim_tag_name("{http://portal.gov.cz/rejstriky/ISRS/1.2/}testtext"))
        self.assertEqual("Currency",
                         ContractProviderRegistr.trim_tag_name("{http://portal.gov.cz/rejstriky/ISRS/1.2/}Currency"))
        self.assertEqual("Subject", ContractProviderRegistr.trim_tag_name("Subject"))

    def test_get_attributes_from_smluvni_strana(self):
        xml_text = """<smluvniStrana><nazev>CARDION s.r.o.</nazev><ico>60719877</ico><adresa>Rybnická 136, BRNO</adresa></smluvniStrana>"""
        root = ET.fromstring(xml_text)
        contract = Contract()
        res = ContractProviderRegistr.get_attributes_from_smluvni_strana(root, contract)
        self.assertEqual("CARDION s.r.o.", res.supplier_name)
        self.assertEqual("60719877", res.supplier_ico)
        self.assertEqual("Rybnická 136, BRNO", res.supplier_address)



    def test_get_currency_from_mena(self):
        xml_text = """<ciziMena><hodnota>8866</hodnota><mena>EUR</mena></ciziMena>"""
        root = ET.fromstring(xml_text)
        contract = Contract()
        res = ContractProviderRegistr.get_currency_from_mena(root, contract)
        self.assertEqual("EUR", res.currency)
        self.assertEqual(8866, res.amount_different_currency)

    def test_get_identifikator_from_zaznam(self):
        xml_text = "<identifikator><idSmlouvy>9104775</idSmlouvy><idVerze>11241768</idVerze></identifikator>"
        root = ET.fromstring(xml_text)
        contract = Contract()
        res = ContractProviderRegistr.get_identifikator_from_zaznam(root, contract)
        self.assertEqual("9104775", res.external_id)
        self.assertEqual("11241768", res.version_id)

    def test_get_attributes_from_subjekt(self):
        xml_text = "<subjekt><datovaSchranka>tj8vfp3</datovaSchranka><nazev>Dům zahraniční spolupráce</nazev><ico>61386839</ico><adresa> ,  Na poříčí 1035 / 4 Nové Město 11006, Praha Hlavní město Praha, </adresa><utvar>310 - Oddělení mobilit mládeže</utvar></subjekt>"
        root = ET.fromstring(xml_text)
        contract = Contract()
        res = ContractProviderRegistr.get_attributes_from_subjekt(root, contract)
        self.assertEqual("tj8vfp3", res.ministry_data_box)
        self.assertEqual("Dům zahraniční spolupráce", res.ministry_name)
        self.assertEqual("61386839", res.ministry_ico)
        self.assertEqual(" ,  Na poříčí 1035 / 4 Nové Město 11006, Praha Hlavní město Praha, ", res.ministry_address)
        self.assertEqual("310 - Oddělení mobilit mládeže", res.ministry_department)

    def test_get_attributes_from_smlouva(self):
        xml_text = "<smlouva><subjekt><datovaSchranka>5gueuef</datovaSchranka><nazev>Krajská zdravotní, a.s.</nazev><ico>25488627</ico><adresa>Sociální péče 3316/12a, 40011 Ústí nad Labem, CZ</adresa></subjekt><smluvniStrana><nazev>Bio-Rad spol. s r.o.</nazev><ico>49243764</ico><adresa>Pikrtova 1737/1a 140 00 Praha 4 -  Nusle</adresa><utvar>Obchodní oddělení</utvar><prijemce>0</prijemce></smluvniStrana><predmet>2LEK-K309647-Bio-Rad spol. s r.o.</predmet><datumUzavreni>2019-12-31</datumUzavreni><cisloSmlouvy>2LEK-K309647</cisloSmlouvy><hodnotaBezDph>433773</hodnotaBezDph><hodnotaVcetneDph>501949</hodnotaVcetneDph></smlouva>"
        root = ET.fromstring(xml_text)
        contract = Contract()
        res = ContractProviderRegistr.get_attributes_from_smlouva(root, contract)
        self.assertEqual("5gueuef", res.ministry_data_box)
        self.assertEqual("Krajská zdravotní, a.s.", res.ministry_name)
        self.assertEqual("25488627", res.ministry_ico)
        self.assertEqual("Sociální péče 3316/12a, 40011 Ústí nad Labem, CZ", res.ministry_address)
        self.assertEqual("Bio-Rad spol. s r.o.", res.supplier_name)
        self.assertEqual("49243764", res.supplier_ico)
        self.assertEqual("Pikrtova 1737/1a 140 00 Praha 4 -  Nusle", res.supplier_address)
        self.assertEqual("Obchodní oddělení", res.supplier_department)
        self.assertEqual("0", res.supplier_receiver_flag)
        self.assertEqual(datetime(year=2019, month=12, day=31), res.date_agreed)
        self.assertEqual("2LEK-K309647", res.contract_number)
        self.assertEqual("2LEK-K309647-Bio-Rad spol. s r.o.", res.purpose)
        self.assertEqual(433773, res.amount_without_dph)
        self.assertEqual(501949, res.amount_with_dph)


    def test_get_attachments_from_prilohy(self):
        xml_text = """<prilohy><priloha><nazevSouboru>D2020001_AEC_EPS Plavecký areál Klíše.pdf</nazevSouboru><hash algoritmus="sha256">6e49d36ef1e0142df82346d03b25c157c50529b5d6773aae93db65154a30ba83</hash><odkaz>https://smlouvy.gov.cz/smlouva/soubor/14623880/D2020001_AEC_EPS%20Plaveck%C3%BD%20are%C3%A1l%20Kl%C3%AD%C5%A1e.pdf</odkaz></priloha></prilohy>"""
        root = ET.fromstring(xml_text)
        contract = Contract()
        res = ContractProviderRegistr.get_attachments_from_prilohy(root, contract)
        self.assertEqual(1, len(res.attachments))
        self.assertEqual("6e49d36ef1e0142df82346d03b25c157c50529b5d6773aae93db65154a30ba83", res.attachments[0].hash_value)
        self.assertEqual("https://smlouvy.gov.cz/smlouva/soubor/14623880/D2020001_AEC_EPS%20Plaveck%C3%BD%20are%C3%A1l%20Kl%C3%AD%C5%A1e.pdf", res.attachments[0].link)
        self.assertEqual("D2020001_AEC_EPS Plavecký areál Klíše.pdf", res.attachments[0].name)

    def test_get_contract_from_zaznam(self):
        xml_text = """<zaznam><identifikator><idSmlouvy>9104775</idSmlouvy><idVerze>11241768</idVerze></identifikator><odkaz>https://smlouvy.gov.cz/smlouva/11241768</odkaz><casZverejneni>2019-12-31T11:00:30+01:00</casZverejneni><smlouva><subjekt><datovaSchranka>tj8vfp3</datovaSchranka><nazev>Dům zahraniční spolupráce</nazev><ico>61386839</ico><adresa> ,  Na poříčí 1035 / 4 Nové Město 11006, Praha Hlavní město Praha, </adresa><utvar>310 - Oddělení mobilit mládeže</utvar></subjekt><smluvniStrana><nazev>Charita Vyškov</nazev><adresa>Charita Vyškov, Horáková Zdeňka, Morávkova 745/1a, 68201 Vyškov</adresa></smluvniStrana><predmet>Grant na projekt s názvem Život s druhými a pro druhé v rámci programu Evropský sbor solidarity, 2019-2-CZ01-ESC11-061562</predmet><datumUzavreni>2019-07-09</datumUzavreni><cisloSmlouvy>DZSP00913077</cisloSmlouvy><ciziMena><hodnota>8866</hodnota><mena>EUR</mena></ciziMena></smlouva><prilohy><priloha><nazevSouboru>Grantová dohoda_2019-2-CZ01-ESC11-061562.pdf</nazevSouboru><hash algoritmus="sha256">e658f5b7e97b52449a90f5388e79686618b68b11bab220161d1e8e8a0a38e8df</hash><odkaz>https://smlouvy.gov.cz/smlouva/soubor/12856359/Grantov%C3%A1%20dohoda_2019-2-CZ01-ESC11-061562.pdf</odkaz></priloha><priloha><nazevSouboru>Přílohy grantové dohody_2019-2-CZ01-ESC11-061562.pdf</nazevSouboru><hash algoritmus="sha256">72cde96cdc39c654f218cd0af2911d56b9df0cf50c3de49de6ced24b342715b7</hash><odkaz>https://smlouvy.gov.cz/smlouva/soubor/12856363/P%C5%99%C3%ADlohy%20grantov%C3%A9%20dohody_2019-2-CZ01-ESC11-061562.pdf</odkaz></priloha><priloha><nazevSouboru>dodatek ke grantové dohodě_2019-2-CZ01-ESC11-061562.pdf</nazevSouboru><hash algoritmus="sha256">c2d34d5d26a63abbec231133abbef3e16574af9db75093da77957a54dc875e90</hash><odkaz>https://smlouvy.gov.cz/smlouva/soubor/14623884/dodatek%20ke%20grantov%C3%A9%20dohod%C4%9B_2019-2-CZ01-ESC11-061562.pdf</odkaz></priloha></prilohy><platnyZaznam>1</platnyZaznam></zaznam>"""
        root = ET.fromstring(xml_text)
        contract = ContractProviderRegistr.get_contract_from_zaznam(root)
        self.assertEqual(8866, contract.amount_different_currency)
        self.assertIsNone(contract.amount_with_dph)
        self.assertIsNone(contract.amount_without_dph)
        self.assertIsNone(contract.approved)
        self.assertEqual(3, len(contract.attachments))
        self.assertIsNone(contract.contract_id)
        self.assertEqual("DZSP00913077", contract.contract_number)
        self.assertEqual("EUR", contract.currency)
        self.assertEqual(datetime(year=2019, month=12, day=31, hour=11, minute=0, second=30), contract.date_published)
        self.assertEqual(datetime(year=2019, month=7, day=9), contract.date_agreed)
        self.assertEqual("9104775", contract.external_id)
        self.assertIsNone(contract.hash_value)
        self.assertEqual("https://smlouvy.gov.cz/smlouva/11241768", contract.link)
        self.assertIsNone(contract.link_pdf)
        self.assertIsNone(contract.linked_record)
        self.assertEqual(" ,  Na poříčí 1035 / 4 Nové Město 11006, Praha Hlavní město Praha, ", contract.ministry_address)
        self.assertEqual('tj8vfp3', contract.ministry_data_box)
        self.assertEqual('310 - Oddělení mobilit mládeže', contract.ministry_department)
        self.assertEqual('61386839', contract.ministry_ico)
        self.assertEqual('Dům zahraniční spolupráce', contract.ministry_name)
        self.assertEqual('Grant na projekt s názvem Život s druhými a pro druhé v rámci programu Evropský sbor solidarity, 2019-2-CZ01-ESC11-061562', contract.purpose)
        self.assertIsNone(contract.ministry_payer_flag)
        self.assertEqual('Charita Vyškov, Horáková Zdeňka, Morávkova 745/1a, 68201 Vyškov', contract.supplier_address)
        self.assertIsNone(contract.supplier_date_box)
        self.assertIsNone(contract.supplier_department)
        self.assertIsNone(contract.supplier_ico)
        self.assertEqual('Charita Vyškov', contract.supplier_name)
        self.assertIsNone(contract.supplier_receiver_flag)
        self.assertEqual('1', contract.valid)
        self.assertEqual('11241768', contract.version_id)
