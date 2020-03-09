from Models.Contract import Contract

MINISTRY_ICOS = ['60162694',
                 '00006947',
                 '00007064',
                 '00024341',
                 '00020478',
                 '00551023',
                 '47609109',
                 '66002222',
                 '00022985',
                 '66003008',
                 '45769851',
                 '00164801',
                 '00023671',
                 '00025429',
]

MINISTRY_NAMES = ['Ministerstvo obrany',
 'Ministerstvo financí',
 'Ministerstvo vnitra',
 'Ministerstvo zdravotnictví',
 'Ministerstvo zemědělství',
 'Ministerstvo práce a sociálních věcí',
 'Ministerstvo průmyslu a obchodu',
 'Ministerstvo pro místní rozvoj',
 'Ministerstvo školství, mládeže a tělovíchovy',
 'Ministerstvo dopravy',
 'Ministerstvo zahraničí',
 'Ministerstvo životního prostředí',
 'Ministerstvo kultury',
 'Ministerstvo spravedlnosti']


def custom_filter(contract: Contract) -> bool:
    if (contract.ministry_ico is not None and any(substring in contract.ministry_ico for substring in MINISTRY_ICOS)) \
            or (contract.supplier_ico is not None and any(substring in contract.supplier_ico for substring in MINISTRY_ICOS)):
        return True

    try:
        if (contract.ministry_name is not None and any(substring in contract.ministry_name.lower() for substring in MINISTRY_NAMES)) \
                or (contract.supplier_name is not None and any(substring in contract.supplier_name.lower() for substring in MINISTRY_NAMES)):
            return True
    except Exception as e:
        pass

    return False