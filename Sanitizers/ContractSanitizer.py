from abc import abstractmethod
from typing import Union

from Models.Contract import Contract
import re

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
    @abstractmethod
    def sanitizeContract(contract: Contract) -> Contract:
        new_con = contract
        if new_con.ministry_name is not None:
            new_con.ministry_name = ContractSanitizer.sanitizeName(new_con.ministry_name)
        if new_con.supplier_name is not None:
            new_con.supplier_name = ContractSanitizer.sanitizeName(new_con.supplier_name)
        if new_con.ministry_ico is not None:
            new_con.ministry_ico = ContractSanitizer.sanitizeICO(new_con.ministry_ico)
        if new_con.supplier_ico is not None:
            new_con.supplier_ico = ContractSanitizer.sanitizeICO(new_con.supplier_ico)

        new_con = ContractSanitizer.sanitizeMinistryName(new_con)

        return new_con

    @abstractmethod
    def sanitizeName(name: str) -> Union[str, None]:
        res = name
        if res is None or len(res) == 0:
            return None

        # remove spaces from start and end of the string
        res = res.strip()

        # replace multiple spaces by one space
        res = re.sub(' +', ' ', res)

        return res

    @abstractmethod
    def sanitizeICO(ico: str) -> Union[str, None]:
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

    @abstractmethod
    def sanitizeMinistryName(contract: Contract) -> Contract:
        res = contract
        try:
            res.ministry_name = MINISTRY_ICOS[contract.ministry_ico]
        except KeyError as e:
            pass

        try:
            res.supplier_name = MINISTRY_ICOS[contract.supplier_ico]
        except KeyError as e:
            pass
        return res
