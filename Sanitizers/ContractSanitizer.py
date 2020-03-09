from abc import abstractmethod
from typing import Union, Optional
from Models.Contract import Contract
import re
import requests
import lxml.html as lh
from urllib.parse import quote

MINISTRY_ICOS = {'60162694': 'Ministerstvo obrany',
                 '00006947': 'Ministerstvo financí',
                 '00007064': 'Ministerstvo vnitra',
                 '00024341': 'Ministerstvo zdravotnictví',
                 '00020478': 'Ministerstvo zemědělství',
                 '00551023': 'Ministerstvo práce a sociálních věcí',
                 '47609109': 'Ministerstvo průmyslu a obchodu',
                 '66002222': 'Ministerstvo pro místní rozvoj',
                 '00022985': 'Ministerstvo školství, mládeže a tělovíchovy',
                 '66003008': 'Ministerstvo dopravy',
                 '45769851': 'Ministerstvo zahraničí',
                 '00164801': 'Ministerstvo životního prostředí',
                 '00023671': 'Ministerstvo kultury',
                 '00025429': 'Ministerstvo spravedlnosti',
}


class ContractSanitizer:
    @staticmethod
    def sanitize_contract(contract: Contract) -> Contract:
        new_con = contract
        if new_con.ministry_name is not None:
            new_con.ministry_name = ContractSanitizer.sanitize_name(new_con.ministry_name)
        if new_con.supplier_name is not None:
            new_con.supplier_name = ContractSanitizer.sanitize_name(new_con.supplier_name)
        if new_con.ministry_ico is not None:
            new_con.ministry_ico = ContractSanitizer.sanitize_ico(new_con.ministry_ico)
        if new_con.supplier_ico is not None:
            new_con.supplier_ico = ContractSanitizer.sanitize_ico(new_con.supplier_ico)

        new_con = ContractSanitizer.sanitize_ministry_name(new_con)

        return new_con

    @staticmethod
    def sanitize_name(name: str) -> Union[str, None]:
        res = name
        if res is None or len(res) == 0:
            return None

        # remove spaces from start and end of the string
        res = res.strip()

        # replace multiple spaces by one space
        res = re.sub(' +', ' ', res)

        return res

    @staticmethod
    def sanitize_ico(ico: str) -> Union[str, None]:
        res = ico
        if res is None:
            return res

        # remove non-numeric characters
        res = re.sub('[^0-9]', '', res)

        # check if the ico is not empty
        if len(res) == 0:
            return None

        # add leading zeros to the number
        res = '0' * (8 - len(res)) + res
        return res

    @staticmethod
    def sanitize_ministry_name(contract: Contract) -> Contract:
        res = contract
        if contract.ministry_ico in MINISTRY_ICOS:
            res.ministry_name = MINISTRY_ICOS[contract.ministry_ico]

        if contract.supplier_ico in MINISTRY_ICOS:
            res.supplier_name = MINISTRY_ICOS[contract.supplier_ico]

        return res

    @staticmethod
    def find_ico_for_name(name:str) -> Optional[str]:
        c_name = name.lower()
        url = 'https://or.justice.cz/ias/ui/rejstrik-dotaz?dotaz=' + quote(name)
        response = requests.get(url)
        if response.status_code == 200:
            doc = lh.fromstring(response.content)
            tr_elements = doc.xpath('//tr')
            icos = []
            i = 0
            for t in tr_elements:
                i += 1
                line = " ".join(str(t.text_content()).split()).lower()
                prefix = f"název subjektu: {c_name} ičo: "
                if line.startswith(prefix):
                    ico = line.replace(prefix, "")
                    icos.append(ico)
            if len(icos) == 1:
                return icos[0]
            else:
                return None
        else:
            return None

