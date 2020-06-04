import logging
import urllib.request
import requests
import xml.etree.ElementTree as ET
import os
from typing import Callable, List, Optional, Any, Generator
from Models.models import Contract
from datetime import datetime
from tqdm import tqdm
from Providers.CProvider import CProvider
from Configuration.Config import config
from Constants.Constants import MINISTRY_ICOS, MINISTRY_NAMES
from Sanitizers.ContractSanitizer import ContractSanitizer

log = logging.getLogger(__name__)

def ministry_filter(contract: Contract) -> bool:
    if (contract.ministry_ico is not None and any(substring in contract.ministry_ico for substring in MINISTRY_ICOS)) \
            or (contract.supplier_ico is not None and any(substring in contract.supplier_ico for substring in MINISTRY_ICOS)):
        return True

    try:
        if (contract.ministry_name is not None and any(
                substring in contract.ministry_name.lower() for substring in MINISTRY_NAMES)) \
                or (contract.supplier_name is not None and any(substring in contract.supplier_name.lower() for substring in MINISTRY_NAMES)):
            return True
    except Exception as e:
        pass

    return False



class ContractProviderRegistr(CProvider):
    """
    Provider smluv stažených z Registru smluv.
    """
    def __init__(self):
        conf = config("contract_provider")
        self.base_url = conf["base_url"]

    @staticmethod
    def _get_file_name(year: int, month: int) -> str:
        """
        Funkce k vygenerování jména souboru, který je možné stáhnout z Registru Smluv
        Šablona je dump_{year}_{month}.xml
        Nekontroluje, zda je rok a měsíc správný (jestli je měsíc větší než 12 atd.)
        :param year: rok, který může být převeden do formátu yyyy
        :param month: měsíc, který může být převeden do formátu mm
        :return: jméno souboru, který je možné stánout z registu
        """
        if len(str(year)) != 4:
            raise Exception(f"Year has to be in format yyyy. {year}")
        if len(str(month).zfill(2)) != 2:
            raise Exception(f"Year has to be in format mm. {month}")
        filename = f"dump_{str(year)}_{str(month).zfill(2)}.xml"
        return filename

    @staticmethod
    def _download_contacts(filename: str = None, link: str = None) -> str:
        """
        Funkce ke stažení souboru z registru smluv buď pomocí linku nebo pomocí jména souboru (v tomto případě je
        doplněna webová stránka. Po stáhnutí vrátí jméno souboru.
        Soubor je stáhnut do aktuálního adresáře. Jméno souboru je stejné, jako je jméno stahovaného souboru.
        Vyvolá vyjímku v případě, že se soubor nepodařilo stáhnout.
        :param link: link k souboru.
        :param filename: jméno souboru.
        :return: jméno souboru
        """
        if filename is not None:
            url = f'https://data.smlouvy.gov.cz/{filename}'
        elif link is not None:
            url = link
            filename = link.replace('https://data.smlouvy.gov.cz/', '')
        else:
            raise Exception("You have to specify the source file or link.")

        r = requests.get(url, stream=True)
        filelength = int(r.headers['Content-Length'])
        with open(filename, 'wb') as f:
            pbar = tqdm(total=int(filelength / 1024), desc=f"Downloading {filename}", position=0, leave=True)
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    pbar.update()
                    f.write(chunk)
        return filename

    @staticmethod
    def _trim_tag_name(tag: str) -> str:
        """
        Funkce k odstranění textu, který se objevuje na začátku některých částí v xml souboru.
        :param tag: tag, ze kterého chceme text odstranit.
        :return: string bez zmíněného textu
        """
        return tag.replace("{http://portal.gov.cz/rejstriky/ISRS/1.2/}", "")

    @staticmethod
    def _get_attributes_from_smluvni_strana(subjekt: Any, contract: Contract) -> Contract:
        """
        Extrahuje jednotlivé atributy ze subjektu v xml souboru a poté je doplní do contractu, který je předán v
        argumentu.
        Vyvolá vyjímku v případě, že narazí na atribut, který nezná.
        :param subjekt: xml objekt, který chceme zpracovat
        :param contract: contract, který chceme doplnit o získané informace
        :return: contract doplněný o informace
        """
        new_contract = contract
        for part in subjekt:
            part_tag = ContractProviderRegistr._trim_tag_name(part.tag)
            if part_tag == "nazev":
                new_contract.supplier_name = part.text
            elif part_tag == "ico":
                new_contract.supplier_ico = part.text
            elif part_tag == "adresa":
                new_contract.supplier_address = part.text
            elif part_tag == "datovaSchranka":
                new_contract.supplier_date_box = part.text
            elif part_tag == "utvar":
                new_contract.supplier_department = part.text
            elif part_tag == "prijemce":
                new_contract.supplier_receiver_flag = part.text
            else:
                raise Exception(f"Unknown attribute in Subjekt: '{part_tag}'")
        return new_contract

    @staticmethod
    def _get_currency_from_mena(mena: Any, contract: Contract) -> Contract:
        """
        Extrahuje měnu a hodnotu, ve které byla smlouva zaplacena z xml objektu.
        Získané informace jsou uloženy do contractu, který je předán v argumentech.
        Pokud narazí na atribut, který nezpracovává, vyvolá vyjímku.
        :param mena: xml objekt, ze kterého chceme extrahovat informace
        :param contract: contract, do kterého chceme uložit informace
        :return: contract doplněný o informace
        """
        new_contract = contract
        for part in mena:
            part_tag = ContractProviderRegistr._trim_tag_name(part.tag)
            if part_tag == "mena":
                new_contract.currency = part.text
            elif part_tag == "hodnota":
                new_contract.amount_different_currency = float(part.text)
            else:
                raise Exception(f"Unknown attribute in Currency: {part_tag}")
        return new_contract

    @staticmethod
    def _get_identifikator_from_zaznam(identifikator: Any, contract: Contract) -> Contract:
        """
        Extrahuje id verze a smlouvy.
        Získané informace jsou uloženy do contractu, který je předán v argumentech.
        Pokud narazí na atribut, který nezpracovává, vyvolá vyjímku.
        :param identifikator: xml objekt, ze kterého chceme extrahovat informace
        :param contract: contract, který chceme doplnit o získané informace
        :return: contract doplěný o informace
        """
        new_contract = contract
        for part in identifikator:
            part_tag = ContractProviderRegistr._trim_tag_name(part.tag)
            if part_tag == "idVerze":
                new_contract.version_id = part.text
            elif part_tag == "idSmlouvy":
                new_contract.external_id = part.text
            else:
                raise Exception(f"Unknown attribute in Currency: {part_tag}")
        return new_contract

    @staticmethod
    def _get_attributes_from_subjekt(strana: Any, contract: Contract) -> Contract:
        """
        Extrahuje informace o subjektu.
        Získané informace jsou uloženy do contractu, který je předán v argumentech.
        Pokud narazí na atribut, který nezpracovává, vyvolá vyjímku.
        :param strana: xml objekt, ze kterého chceme informace extrahovat
        :param contract: contract, který chceme doplnit o získané informace
        :return: contract doplěný o informace
        """
        new_contract = contract
        for part in strana:
            part_tag = ContractProviderRegistr._trim_tag_name(part.tag)
            if part_tag == "nazev":
                new_contract.ministry_name = part.text
            elif part_tag == "ico":
                new_contract.ministry_ico = part.text
            elif part_tag == "adresa":
                new_contract.ministry_address = part.text
            elif part_tag == "datovaSchranka":
                new_contract.ministry_data_box = part.text
            elif part_tag == "utvar":
                new_contract.ministry_department = part.text
            elif part_tag == "platce":
                new_contract.ministry_payer_flag = part.text
            else:
                raise Exception(f"Unknown attribute in Smluvni Strana: {part_tag}")
        return new_contract

    @staticmethod
    def _get_attributes_from_smlouva(smlouva: Any, contract: Contract) -> Contract:
        """
        Extrahuje informace o smlouve.
        Získané informace jsou uloženy do contractu, který je předán v argumentech.
        Pokud narazí na atribut, který nezpracovává, vyvolá vyjímku.
        :param smlouva:  xml objekt, ze kterého chceme informace extrahovat
        :param contract: contract, který chceme doplnit o získané informace
        :return: contract doplěný o informace
        """
        new_contract = contract
        for part in smlouva:
            part_tag = ContractProviderRegistr._trim_tag_name(part.tag)
            if part_tag == "predmet":
                new_contract.purpose = part.text
            elif part_tag == "smluvniStrana":
                new_contract = ContractProviderRegistr._get_attributes_from_smluvni_strana(part, new_contract)
            elif part_tag == "subjekt":
                new_contract = ContractProviderRegistr._get_attributes_from_subjekt(part, new_contract)
            elif part_tag == "datumUzavreni":
                new_contract.date_agreed = datetime.strptime(part.text, '%Y-%m-%d')
            elif part_tag == "cisloSmlouvy":
                new_contract.contract_number = part.text
            elif part_tag == "hodnotaVcetneDph":
                new_contract.amount_with_dph = float(part.text)
            elif part_tag == "hodnotaBezDph":
                new_contract.amount_without_dph = float(part.text)
            elif part_tag == "schvalil":
                new_contract.approved = part.text
            elif part_tag == "navazanyZaznam":
                new_contract.linked_record = part.text
            elif part_tag == "ciziMena":
                ContractProviderRegistr._get_currency_from_mena(part, new_contract)
            else:
                raise Exception(f"Unknown attribute in Smlouva: {part_tag}")
        return new_contract

    @staticmethod
    def _get_contract_from_zaznam(zaznam: Any) -> Contract:
        """
        Extrahuje informace o smlouve jako celku.
        Vytvoří nový contract, do kteréhouloží všechny informace.
        :param zaznam: xml objekt, ze kterého chceme informace extrahovat
        :return: contract do kterého jsou doplněny všechny informace
        """
        contract = Contract()
        for attrib in zaznam:
            tag = ContractProviderRegistr._trim_tag_name(attrib.tag)
            if tag == "identifikator":
                contract = ContractProviderRegistr._get_identifikator_from_zaznam(attrib, contract)
            elif tag == "odkaz":
                contract.link = attrib.text
            elif tag == "casZverejneni":
                contract.date_published = datetime.strptime(attrib.text[0:19], '%Y-%m-%dT%H:%M:%S')
            elif tag == "smlouva":
                contract = ContractProviderRegistr._get_attributes_from_smlouva(attrib, contract)
            elif tag == "prilohy":
                pass
            elif tag == "platnyZaznam":
                contract.valid = attrib.text
            else:
                raise Exception(f"Unknown attribute in Zaznam: {tag}")
        return contract

    @staticmethod
    def _get_contracts_from_file(filename: str, custom_filter: Callable[[Contract], bool] = None) -> List[Contract]:
        """
        Nahraje xml soubor a extrahuje záznamy, které obsahuje. Pokud je specifikován filtr, jsou uloženy jen ty smlouvy,
        které projdou filtrem.
        :param filename: cesta k souboru , který chceme zpracovat
        :param custom_filter: nepovinný filtr, který pro contract vrátí True nebo False.
        :return: List smluv, které byli extrahovány ze souboru.
        """
        result = []
        tree = ET.parse(filename)
        root = tree.getroot()
        for zaznam in tqdm(root, position=0, leave=True, desc="Extracting contracts"):
            tag = ContractProviderRegistr._trim_tag_name(zaznam.tag)
            if tag != "zaznam":
                pass
            else:
                res_con = ContractProviderRegistr._get_contract_from_zaznam(zaznam=zaznam)
                if custom_filter is not None and custom_filter(res_con) is True:
                    result.append(res_con)
                elif custom_filter is None:
                    result.append(res_con)
        return result

    @staticmethod
    def _delete_file(filename: str) -> None:
        """
        Funkce ke smazáno souboru. Tato funkce je využita ke smazání stažených a zpracovaných souborů.
        :param filename: cesta k souboru, který chceme smazat.
        :return: None
        """
        os.remove(filename)

    @staticmethod
    def _get_contracts_with_date(year: int, month: int, custom_filter: Callable[[Contract], bool]) -> Optional[List[Contract]]:
        """
        Funkce, která vygeneruje jméno souboru, který chceme stáhnout.
        Poté soubor stáhne z registru smluv a uloží ho.
        Tento soubor je poté zpracován a smlouvy, které obsahoval jsou vráceny v listu.
        Soubor je po zpracování smazán.
        :param year: rok, ze kterého chceme smlouvy získat
        :param month: měsíc, ze kterého chceme smlouvy získat
        :param custom_filter: nepovinný filtr, který pro contract vrátí True nebo False.
        :return: List smluv, které soubor obsahoval.
        """
        filename = ContractProviderRegistr._get_file_name(year, month)
        try:
            filename = ContractProviderRegistr._download_contacts(filename=filename)
            res = ContractProviderRegistr._get_contracts_from_file(filename, custom_filter)
            ContractProviderRegistr._delete_file(filename)
            return res
        except Exception as e:
            log.error(f"Could not download file '{filename}'. Exception: {e}")
            return None

    @staticmethod
    def _get_contracts_with_link(link: str, custom_filter: Optional[Callable[[Contract], bool]] = None) -> Optional[List[Contract]]:
        """
        Funkce, která stáhne soubor z linku předaného v argumentech.
        Poté soubor stáhne z registru smluv a uloží ho.
        Tento soubor je poté zpracován a smlouvy, které obsahoval jsou vráceny v listu.
        Soubor je po zpracování smazán.
        :param link: link na soubor, který chceme stáhnout a zpracovat
        :param custom_filter: nepovinný filtr, který pro contract vrátí True nebo False.
        :return: List smluv, které soubor obsahoval.
        """
        try:
            filename = ContractProviderRegistr._download_contacts(link=link)
            res = ContractProviderRegistr._get_contracts_from_file(filename, custom_filter)
            ContractProviderRegistr._delete_file(filename)
            return res
        except Exception as e:
            log.error(f"Could not download file from link: '{link}'. Exception: {e}")
            return None

    @staticmethod
    def _get_available_link(root: Any) -> Optional[str]:
        """
        Extrahuje link na soubor v registru smluv z xml objektu.
        :param root: xml objekt, obsahující linky na soubory se smlouvami
        :return: Pokud obsahuje odkaz, vrátí ho. Pokud ne, vrátí None.
        """
        for child in root:
            tag = ContractProviderRegistr._trim_tag_name(child.tag)
            if tag == "odkaz":
                return child.text
        return None


    def _get_available_files(self) -> List[str]:
        """
        Extrahuje linky na dostupné soubory se smlouvama z registru smluv.
        Vyvolá vyjímku, pokud není možné data přečíst ze stránky.
        :return: List linků.
        """
        data = ""
        url = self.base_url
        with urllib.request.urlopen(url) as response:
            if response.getcode() == 200:
                data = response.read()
            else:
                raise Exception(f"Could not download the file. {response.getcode()} {response.info()}")

        result = []
        root = ET.fromstring(data)
        for child in root:
            tag = ContractProviderRegistr._trim_tag_name(child.tag)
            if tag != "dump":
                pass
            else:
                link = ContractProviderRegistr._get_available_link(child)
                if link is not None:
                    result.append(link)
        return result

    def get_generator(self) -> Generator[Contract, None, None]:
        """
        Funkce pro extrahování smluv z registru smluv.
        :return: Generátor, který vrací smlouvy z registru smluv.
        """
        links = self._get_available_files()

        for link in links[2:]:
            contracts = ContractProviderRegistr._get_contracts_with_link(link, ministry_filter)
            if not contracts:
                raise Exception(f"No contracts downloaded. Check the url {link} if data are available.")
            for contract in contracts:
                ContractSanitizer.sanitize_contract(contract)
                yield contract

        return

