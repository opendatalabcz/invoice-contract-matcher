from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Integer, Table, MetaData, ForeignKey
from sqlalchemy.orm import mapper, relationship


class ContractAttachment:
    """
    Třída reprezentující přílohu smlouvy.
    """
    def __init__(self, name: str = None, hash_value: str = None, link: str = None):
        """
        Konstruktor přílohy.
        :param name: Název souboru.
        :param hash_value: Hash souboru.
        :param link: URL odkazující na přiložený soubor.
        """
        self.name = name
        self.hash_value = hash_value
        self.link = link

