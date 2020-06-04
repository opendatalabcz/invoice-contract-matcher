from abc import abstractmethod
from typing import Union, Optional
from Models.models import Contract
import re
import requests
import lxml.html as lh
from urllib.parse import quote
from Constants.Constants import MINISTRY_DICT

class ContractSanitizer:
    """
    Třída, která slouží k opravě slouvy. Třída může doplnit některé údaje, které chybí a je možné je získat nebo odvodit.
    """
    @staticmethod
    def sanitize_contract(contract: Contract) -> Contract:
        """
        Funkce, která slouží k opravení smouvy. Tato funkce shromažďuje všechny dílčí opravy.
        :param contract: smlouva, kteoru chceme opravit
        :return: Smlouvu, která má atributy opravené a doplněné
        """
        new_con = contract
        if new_con.ministry_name is not None:
            new_con.ministry_name = ContractSanitizer._sanitize_name(new_con.ministry_name)
        if new_con.supplier_name is not None:
            new_con.supplier_name = ContractSanitizer._sanitize_name(new_con.supplier_name)
        if new_con.ministry_ico is not None:
            new_con.ministry_ico = ContractSanitizer._sanitize_ico(new_con.ministry_ico)
        if new_con.supplier_ico is not None:
            new_con.supplier_ico = ContractSanitizer._sanitize_ico(new_con.supplier_ico)
        return new_con

    @staticmethod
    def _sanitize_name(name: str) -> Optional[str]:
        """
        Funkce k opravení jména dodavatele nebo ministerstva. Odstraní přebytečné mezery na začáku, konci a uprostřed jména.
        :param name: jméno, které chceme opravit
        :return: None
        """
        res = name
        if res is None or len(res) == 0:
            return None

        # remove spaces from start and end of the string
        res = res.strip()

        # replace multiple spaces by one space
        res = re.sub(' +', ' ', res)

        return res

    @staticmethod
    def _sanitize_ico(ico: str) -> Optional[str]:
        """
        Funkce k opravení IČA. Tato funkce odstraní nučíselné znaky a doplní o nuly na začátku, aby obsahovalo 8 znaků,
        pokud obsahuje méně.
        :param ico: IČO, které chceme opravit
        :return: Opravené IČO, nebo None, pokud již na začátku bylo None nebo po odstranění znaků vznikl prázdný řetězec
        """
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
    def _sanitize_ministry_name(contract: Contract) -> Contract:
        """
        Funkce k opravení jména ministerstva. Jméno ministerstva nebo dodavatele je doplněno podle seznamu IČ ministerstev
        :param contract: smlouva u které chceme změnu provést
        :return: smlouva s doplněným jménem. Pokud IČO není nalezeno, není provedena žádné změna
        """
        res = contract
        if contract.ministry_ico in MINISTRY_DICT:
            res.ministry_name = MINISTRY_DICT[contract.ministry_ico]

        if contract.supplier_ico in MINISTRY_DICT:
            res.supplier_name = MINISTRY_DICT[contract.supplier_ico]

        return res

    @staticmethod
    def _find_ico_for_name(name: str) -> Optional[str]:
        """
        Funkce, které dohledá IČO dodavatele podle jména. Vyhledávání je provedeno na serveru or.justice.cz
        Pokud je při vyhledání vráceno více výsledků než jeden, je vráceno None
        :param name: jméno, pro které chceme vyhledat IČO
        :return: None, pokud jsme získaly 0 nebo více výsledků. None je také vrácen v případě, že se nepovedlo získat výsledky ze stránky.
                Pokud byl vyhledán jeden výsledek, je vráceno odpovídající IČO
        """
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

