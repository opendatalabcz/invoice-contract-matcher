import urllib.request
import shutil
import xml.etree.ElementTree as ET
import os
from typing import Union, Callable
from Decorators.Timer import timer
from Providers.ContractProvider import Provider
from Models.ContractAttachment import ContractAttachment
from Models.Contract import Contract
from datetime import datetime
from tqdm import tqdm


class ContractProviderRegistr(Provider):
    def __init__(self):
        pass

    def getFileName(self, year: int, month: int) -> str:
        """
        Function to get name of the file that can be downloaded from the Registr Smluv.
        The template of the name is dump_{year}_{month}.xml.
        If the year nad month are not in the desired format, will raise exception.
        Does not check the correctness of the numbers (month greater then 12)
        :param year: int that can be converted to format yyyy
        :param month: nt that can be converted to format mm
        :return: name of the file for specific month and year.
        """

        if len(str(year)) != 4:
            raise Exception(f"Year has to be in format yyyy. {year}")
        if len(str(month).zfill(2)) != 2:
            raise Exception(f"Year has to be in format mm. {month}")
        filename = f"dump_{str(year)}_{str(month).zfill(2)}.xml"
        return filename

    def downloadContacts(self, filename: str = None, link: str = None) -> str:
        """
        Function to download file from the web page with contracts.
        File is downloaded to the actual directory. Name of the saved file is same as the name of downloaded file.
        Will raise exception if the file could not be downloaded.
        :param link: direct url to the file
        :param filename: string name of the file. To this filename will be added webpage.
        :return: None
        """
        if filename is not None:
            url = f'https://data.smlouvy.gov.cz/{filename}'
        elif link is not None:
            url = link
            filename = link.replace('https://data.smlouvy.gov.cz/', '')
        else:
            raise Exception("You have to specify the source file or link.")

        print(f"Starting to download file {filename} from url: {url} ...")
        with urllib.request.urlopen(url) as response, open(filename, 'wb') as out_file:
            if response.getcode() == 200:
                shutil.copyfileobj(response, out_file)
            else:
                raise Exception(f"Could not download the file. {response.getcode()} {response.info()}")
        print(f"File downloaded {filename}...")
        return filename

    def printInfo(self, root, pred: str) -> None:
        pred_new = pred + "\t"
        for zaznam in root:
            res = ""
            tag = zaznam.tag.replace("{http://portal.gov.cz/rejstriky/ISRS/1.2/}", "")
            res += f"{pred}[{tag}] Text: {zaznam.text}"
            if len(zaznam.attrib) != 0:
                res += f", Attrib: {zaznam.attrib}"
            print(res)
            self.printInfo(zaznam, pred_new)
        return

    def printContractsFromFile(self, filename: str) -> None:
        tree = ET.parse(filename)
        root = tree.getroot()
        self.printInfo(root, "")
        return

    def trimTagName(self, tag: str) -> str:
        return tag.replace("{http://portal.gov.cz/rejstriky/ISRS/1.2/}", "")

    def getAttributesFromSmluvniStrana(self, subjekt, contract: Contract) -> Contract:
        new_contract = contract
        for part in subjekt:
            part_tag = self.trimTagName(part.tag)
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

    def getCurrencyFromMena(self, mena, contract: Contract) -> Contract:
        new_contract = contract
        for part in mena:
            part_tag = self.trimTagName(part.tag)
            if part_tag == "mena":
                new_contract.currency = part.text
            elif part_tag == "hodnota":
                new_contract.amount_different_currency = float(part.text)
            else:
                raise Exception(f"Unknown attribute in Currency: {part_tag}")
        return new_contract

    def getIdentifikatorFromZaznam(self, identifikator, contract: Contract) -> Contract:
        new_contract = contract
        for part in identifikator:
            part_tag = self.trimTagName(part.tag)
            if part_tag == "idVerze":
                new_contract.version_id = part.text
            elif part_tag == "idSmlouvy":
                new_contract.external_id = part.text
            else:
                raise Exception(f"Unknown attribute in Currency: {part_tag}")
        return new_contract

    def getAttributesFromSubjekt(self, strana, contract: Contract) -> Contract:
        new_contract = contract
        for part in strana:
            part_tag = self.trimTagName(part.tag)
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

    def getAttributesFromSmlouva(self, smlouva, contract: Contract) -> Contract:
        new_contract = contract
        for part in smlouva:
            part_tag = self.trimTagName(part.tag)
            if part_tag == "predmet":
                new_contract.purpose = part.text
            elif part_tag == "smluvniStrana":
                new_contract = self.getAttributesFromSmluvniStrana(part, new_contract)
            elif part_tag == "subjekt":
                new_contract = self.getAttributesFromSubjekt(part, new_contract)
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
                self.getCurrencyFromMena(part, new_contract)
            else:
                raise Exception(f"Unknown attribute in Smlouva: {part_tag}")
        return new_contract

    def getAttachmentsFromPrilohy(self, prilohy, contract: Contract) -> Contract:
        new_contract = contract
        attachments = []
        for attachment_part in prilohy:
            attp_tag = self.trimTagName(attachment_part.tag)
            if attp_tag == "priloha":
                conAttachment = ContractAttachment()
                for attachment in attachment_part:
                    att_tag = self.trimTagName(attachment.tag)
                    if att_tag == "nazevSouboru":
                        conAttachment.name = attachment.text
                    elif att_tag == "odkaz":
                        conAttachment.link = attachment.text
                    elif att_tag == "hash":
                        conAttachment.hash_value = attachment.text
                    else:
                        raise Exception(f"Unknown attribute in Priloha: {att_tag}")
                attachments.append(conAttachment)
        new_contract.attachments = attachments
        return new_contract

    def getContractFromZaznam(self, zaznam) -> Contract:
        contract = Contract()
        for attrib in zaznam:
            tag = self.trimTagName(attrib.tag)
            if tag == "identifikator":
                contract = self.getIdentifikatorFromZaznam(attrib, contract)
            elif tag == "odkaz":
                contract.link = attrib.text
            elif tag == "casZverejneni":
                contract.date_published = datetime.strptime(attrib.text[0:19], '%Y-%m-%dT%H:%M:%S')
            elif tag == "smlouva":
                contract = self.getAttributesFromSmlouva(attrib, contract)
            elif tag == "prilohy":
                contract = self.getAttachmentsFromPrilohy(attrib, contract)
            elif tag == "platnyZaznam":
                contract.valid = attrib.text
            else:
                raise Exception(f"Unknown attribute in Zaznam: {tag}")
        return contract

    def getContractsFromFile(self, filename: str, custom_filter: Callable[[Contract], bool]) -> list:
        result = []
        tree = ET.parse(filename)
        root = tree.getroot()
        for zaznam in tqdm(root):
            tag = self.trimTagName(zaznam.tag)
            if (tag != "zaznam"):
                pass
            else:
                res_con = self.getContractFromZaznam(zaznam=zaznam)
                if custom_filter is not None and custom_filter(res_con) is True:
                    result.append(res_con)
                elif custom_filter is None:
                    result.append(res_con)
        return result

    def deleteFile(self, filename: str) -> None:
        """
        Function to remove file. This function is just to free space when we download the file from the web.
        :param filename: name of the file that we want to remove.
        :return: None
        """
        print(f"Removing {filename}")
        os.remove(filename)
        print(f"File removed.")
        return

    @timer
    def getContractsWithDate(self, year: int, month: int, custom_filter: Callable[[Contract], bool]) -> Union[list, None]:
        filename = self.getFileName(year, month)
        try:
            filename = self.downloadContacts(filename=filename)
            res = self.getContractsFromFile(filename, custom_filter)
            self.deleteFile(filename)
            return res
        except Exception as e:
            print(f"Could not download file '{filename}'. Exception: {e}")
            return None

    @timer
    def getContractsWithLink(self, link: str, custom_filter: Callable[[Contract], bool] = None) -> Union[list, None]:
        try:
            filename = self.downloadContacts(link=link)
            res = self.getContractsFromFile(filename, custom_filter)
            # self.deleteFile(filename)
            return res
        except Exception as e:
            print(f"Could not download file from link: '{link}'. Exception: {e}")
            return None

    def getAvailableLink(self, root) -> Union[str, None]:
        for child in root:
            # print(child.tag)
            tag = self.trimTagName(child.tag)
            if tag == "odkaz":
                return child.text
        return None

    def getAvailableFiles(self) -> list:
        data = ""
        url = f'https://data.smlouvy.gov.cz'
        with urllib.request.urlopen(url) as response:
            if response.getcode() == 200:
                data = response.read()
            else:
                raise Exception(f"Could not download the file. {response.getcode()} {response.info()}")

        # print(data.decode("utf-8"))
        result = []
        root = ET.fromstring(data)
        for child in root:
            # print(child.tag)
            tag = self.trimTagName(child.tag)
            if (tag != "dump"):
                pass
            else:
                link = self.getAvailableLink(root=child)
                if link is not None:
                    result.append(link)
        # print(result)
        return result
