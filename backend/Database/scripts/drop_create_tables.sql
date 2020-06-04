DROP TABLE IF EXISTS contract CASCADE;
CREATE TABLE contract(
   contract_id serial PRIMARY KEY,
   external_id VARCHAR(50),
   version_id VARCHAR(50),
   link VARCHAR(50),
   date_published TIMESTAMP without time zone,
   date_agreed TIMESTAMP without time zone,
   date_expiry TIMESTAMP without time zone,
   ministry_name VARCHAR(500),
   ministry_data_box VARCHAR(7),
   ministry_ico VARCHAR(20),
   ministry_address VARCHAR(500),
   ministry_department VARCHAR(200),
   ministry_payer_flag VARCHAR(5),
   supplier_name VARCHAR(500),
   supplier_date_box VARCHAR(7),
   supplier_ico VARCHAR(20),
   supplier_address VARCHAR(500),
   supplier_department VARCHAR(500),
   supplier_receiver_flag VARCHAR(5),
   purpose VARCHAR(1000),
   contract_number VARCHAR(250),
   approved VARCHAR(500),
   amount_without_dph Float,
   amount_with_dph Float,
   amount_different_currency Float,
   currency VARCHAR(50),
   valid VARCHAR(5),
   linked_record VARCHAR(250)
);
ALTER SEQUENCE contract_contract_id_seq RESTART;

DROP TABLE IF EXISTS invoice CASCADE;
CREATE TABLE invoice(
   invoice_id serial PRIMARY KEY,
   external_id VARCHAR(200),
   ministry_ico VARCHAR(20),
   ministry_name VARCHAR(500),
   supplier_ico VARCHAR(20),
   supplier_name VARCHAR(500),
   date_acceptance TIMESTAMP without time zone,
   date_payment TIMESTAMP without time zone,
   date_due TIMESTAMP without time zone,
   date_issue TIMESTAMP without time zone,
   purpose VARCHAR(1000),
   amount_with_dph Float,
   amount_without_dph Float,
   amount_per_item Float,
   amount_different_currency Float,
   currency VARCHAR(20),
   supplier_invoice_identifier VARCHAR(100),
   document_label VARCHAR(100),
   document_number VARCHAR(100),
   variable_symbol VARCHAR(100),
   budget_item_code VARCHAR(100),
   budget_item_name VARCHAR(200),
   contract_identifier VARCHAR(100)
);
ALTER SEQUENCE invoice_invoice_id_seq RESTART;

DROP TABLE IF EXISTS possible_relation CASCADE ;
CREATE TABLE possible_relation(
    possible_relation_id serial PRIMARY KEY,
    contract_id Integer,
    invoice_id Integer,
    score float,
    real boolean,
    CONSTRAINT contract_id_fkey FOREIGN KEY (contract_id)
      REFERENCES contract (contract_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT invoice_id_fkey FOREIGN KEY (invoice_id)
      REFERENCES invoice (invoice_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);
ALTER SEQUENCE possible_relation_possible_relation_id_seq RESTART;

DROP TABLE IF EXISTS test_result CASCADE;
CREATE TABLE test_result(
    test_result_id serial PRIMARY KEY,
    possible_relation_id INTEGER,
    test_name VARCHAR(500),
    result float,
    CONSTRAINT possible_relation_id_fkey FOREIGN KEY (possible_relation_id)
      REFERENCES possible_relation (possible_relation_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
;
ALTER SEQUENCE test_result_test_result_id_seq RESTART;


DROP TABLE IF EXISTS statistics CASCADE;
create table statistics
(
    statistics_id    serial  not null
        constraint statistics_pk
            primary key,
    type             varchar not null,
    text_attribute   varchar,
    text_attribute_2   varchar,
    text_attribute_3   varchar,
    double_attribute double precision,
    double_attribute_2 double precision,
    double_attribute_3 double precision,
    int_attribute    integer,
    int_attribute_2    integer,
    int_attribute_3    integer,
    date_attribute   timestamp,
    date_attribute_2   timestamp,
    date_attribute_3   timestamp
);
ALTER SEQUENCE statistics_statistics_id_seq RESTART;

DROP TABLE IF EXISTS ministry CASCADE;
create table ministry
(
	ministry_id serial
		constraint ministry_pk
			primary key,
	ministry_name varchar not null,
	ministry_ico varchar not null,
	shortcut varchar not null
);
ALTER SEQUENCE ministry_ministry_id_seq RESTART;

DROP TABLE IF EXISTS contract_warning CASCADE;
create table contract_warning
(
contract_warning_id serial
    constraint contract_warning_pk
        primary key,
contract_id int not null
    constraint contract_warning_contract_id_fk
        references contract,
contract_amount double precision,
invoices_amount double precision,
difference double precision
);
create unique index contract_warning_contract_id_idx
on contract_warning (contract_id);
ALTER SEQUENCE contract_warning_contract_warning_id_seq RESTART;

DROP TABLE IF EXISTS blocked_supplier CASCADE;
create table blocked_supplier
(
	blocked_supplier_id serial
		constraint blocked_supplier_pk
			primary key,
	supplier_name varchar,
	supplier_ico varchar
);
create unique index blocked_supplier_supplier_name_idx
on blocked_supplier (supplier_name);
create unique index blocked_supplier_supplier_ico_idx
on blocked_supplier (supplier_ico);
ALTER SEQUENCE blocked_supplier_blocked_supplier_id_seq RESTART;


INSERT INTO public.ministry (ministry_id, ministry_name, ministry_ico, shortcut) VALUES (1, 'Ministerstvo dopravy', '66003008', 'MD');
INSERT INTO public.ministry (ministry_id, ministry_name, ministry_ico, shortcut) VALUES (2, 'Ministerstvo financí', '00006947', 'MF');
INSERT INTO public.ministry (ministry_id, ministry_name, ministry_ico, shortcut) VALUES (3, 'Ministerstvo kultury', '00023671', 'MK');
INSERT INTO public.ministry (ministry_id, ministry_name, ministry_ico, shortcut) VALUES (4, 'Ministerstvo práce a sociálních věcí', '00551023', 'MPSV');
INSERT INTO public.ministry (ministry_id, ministry_name, ministry_ico, shortcut) VALUES (5, 'Ministerstvo průmyslu a obchodu', '47609109', 'MPO');
INSERT INTO public.ministry (ministry_id, ministry_name, ministry_ico, shortcut) VALUES (6, 'Ministerstvo spravedlnosti', '00025429', 'MS');
INSERT INTO public.ministry (ministry_id, ministry_name, ministry_ico, shortcut) VALUES (7, 'Ministerstvo vnitra', '00007064', 'MV');
INSERT INTO public.ministry (ministry_id, ministry_name, ministry_ico, shortcut) VALUES (8, 'Ministerstvo zahraničních věcí', '45769851', 'MZV');
INSERT INTO public.ministry (ministry_id, ministry_name, ministry_ico, shortcut) VALUES (9, 'Ministerstvo zdravotnictví', '00024341', 'MZ');
INSERT INTO public.ministry (ministry_id, ministry_name, ministry_ico, shortcut) VALUES (10, 'Ministerstvo zemědělství', '00020478', 'MZe');
INSERT INTO public.ministry (ministry_id, ministry_name, ministry_ico, shortcut) VALUES (11, 'Ministerstvo školství, mládeže a tělovýchovy', '00022985', 'MŠMT');
INSERT INTO public.ministry (ministry_id, ministry_name, ministry_ico, shortcut) VALUES (12, 'Ministerstvo životního prostředí', '00164801', 'MŽP');
INSERT INTO public.ministry (ministry_id, ministry_name, ministry_ico, shortcut) VALUES (13, 'Ministerstvo obrany', '60162694', 'MO');


analyze invoice
;
analyse contract
;
analyse possible_relation
;
analyse test_result
;
analyse contract_warning

create index invoice_ministry_ico_idx on invoice (ministry_ico);

create index contract_ministry_ico_idx on contract (ministry_ico);

create index invoice_supplier_ico_idx on invoice (supplier_ico);

create index contract_supplier_ico_idx on contract (supplier_ico);

create index statistics_type_idx on statistics (type);

create index ministry_ministry_ico_idx on ministry (ministry_ico);

create index possible_relation_invoice_id_idx on possible_relation (invoice_id);

create index possible_relation_contract_id_idx on possible_relation (contract_id);

create unique index possible_relation_unique_columns_idx on possible_relation (COALESCE(invoice_id, -1), COALESCE(contract_id,-1))

