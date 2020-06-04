from configparser import ConfigParser, SectionProxy
from typing import Dict, Any

CONFIG_FILE = 'configuration.ini'


def config(section: str) -> SectionProxy:
    """
    Funkce k extrahování dat z configuračního souboru
    :param section: sekce uvnitř konfiguračního souboru označená uvnitř hranatých závorek
    :return: d
    """
    parser = ConfigParser()
    parser.read(CONFIG_FILE)

    if parser.has_section(section):
        return parser[section]
    else:
        raise Exception(f'Section {section} not found in the {CONFIG_FILE} file')
