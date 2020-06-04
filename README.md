# Portá srovnávače faktur a smluv ministerstev České Republiky

Tato aplikace vznikla za účelem mapování faktur zveřejněných ministerstvi České Republiky na uzavřené smlouvy v Registru Smluv.

#Instalační příručka

##Backend

Je potřeba mít nainstalován Python 3
Stažení: https://www.python.org/downloads/
Postup instalace: https://realpython.com/installing-python/

Pro nainstalování potřebných knihoven použijeme instalační manager pip, spusťte

        pip install -r requirements.txt
        
Pokud máte více Python verzí nainstalováno, je možné specifikovat verzi použitím 
        
        pip3 install -r requirements.txt
        
###Naplnění databáze daty

V tomto projektu je při vývoji použita databáze PostgreSQL.

Stažení: https://www.postgresql.org/download/
Instalace: https://www.postgresqltutorial.com/install-postgresql/

Pro práci s databází je možné využít terminál: https://www.postgresql.org/docs/12/app-psql.html
Nebo je zde možnost využítí nástroje pgAdmin: https://www.pgadmin.org/
Nebo využít nástrojů ve vývojovém prostředí, například Pycharm: https://www.jetbrains.com/help/pycharm/relational-databases.html

### Konfigurační soubor
Jako zdroj nastavení slouží soubor configuration.ini

Soubor obsahuje 6 částí:

- Flask
    - Obsahuje nastavení frameworku flask
    - paramtery host a port určují, na jaké adrese bude REST API dostupné
    - pokud chcete, aby bylo možné se k API připojit ze sítě, nastavte host na adresu 0.0.0.0

- matcherdb
    - obsahuje údaje potřebné k připojení k databázi, která bude využita pro uložení dat, které budou následně použity
    při párování

- opendatadb
    - obsahuje údaje potřebné k připojení k databázi, která slouží jako zdroj faktur
  
- contract_provider
    - slouží k specifikování parametrů pro třídu invoice provider

- deciding_pipeline
    - slouží k specifikování parametrů pro třídu deciding pipeline

v souboru configuration.ini je potřeba nastavit sekce matcherdb a opendatadb
Matcherdb jsou údaje pro připojení k databázi, kam budou data uložena

Při využití opendata databáze:
- Opendatadb jsou údaje pro připojení k databázi, ze které se stáhnou faktury
- Opendata databázi je možné naplnit daty pomocí aplikace OpendataLabu dostupné zde: https://github.com/opendatalabcz/opendata

Při využití smluv z Registru smluv:
- Pro stažení smluv z Registru smluv není potřeba upravovat nic. 
- Pouze zdrojovou adresu v sekci contract_provider, pokud se změnila.

Pokud chcete využít vlastní provider dat, je potřeba ho nastavit v souboru data_downloader.py


### Spuštění

Před spuštěním nahrávání dat je nutné vytvořit tabulky, do kterých jsou nahrány smlouvy a faktury.
- Pro vytvoření tabulek v databázi a nahrání základních dat spusťte create script v ./Database/scripts/drop_create_tables.sql
- 

### Stažení dat
Po nastavení potřebných údajů, je třeba spustit soubor data_downloader.py

        python data_downloader.py
        
### Spuštění párování
Pro spuštění párování je spusťe main.py

        python main.py

### REST API
Pokud jsou napárována, je možné spustit flask aplikaci, která vystaví REST API.

1) Nejdříve nastavíme proměnou FLASK_APP:

        export FLASK_APP=flask_runner.py
        
2) Flask poté spustíme příkazem:
        
        python flask_runner.py
   
   Nebo je možné použít příkaz:
   
        flask run 
   
   Ale tento příkaz bude ignorovat nastavení, které je uložené v souboru configuration.ini
   Host a port je možné nastavit pomocí parametrů v parametrech
   
        flask run --host 0.0.0.0

##Frontend

Pro spuštění webového klienta je nutné nainstalovat Node.js
https://nodejs.org/en/download/

1) pro nainstalování potřebných balíčků spusťe 

        npm install
        
2) Po nainstalování potřebných balíčků je možné spustit server pomocí přípazu
        
        npm start
        
   Tento příkaz spustí server na adrese http://127.0.0.1:3000
   Na této adrese je také dostupná dokumentace k REST API, kde je možné spojení otestovat.
 
3) Pro vytvotření produkční verze spusťe

        npm run-script build
        
   Build je následně uložen v adresáři build
   
Úprava adresy odkazující na REST API, ze kterého jsou získávány data, je možná v souboru: 

frontend/src/variables/general.js
   
Nastavení npm příkazů je možné v souboru package.json
V tomto souboru jsou uloženy také dependencies 

Při vývoji byly použity následující knihovny nebo projekty:
Material Dashboard - https://github.com/creativetimofficial/material-dashboard
Chartist - https://gionkunz.github.io/chartist-js/
Material UI - https://material-ui.com/
