DROP TABLE IF EXISTS contract;
CREATE TABLE contract(
   contract_id serial PRIMARY KEY,
   external_id VARCHAR(50),
   version_id VARCHAR(50),
   link VARCHAR(50),
   date_published TIMESTAMP without time zone,
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
   supplier_department VARCHAR(200),
   supplier_receiver_flag VARCHAR(5),
   purpose VARCHAR(1000),
   date_agreed TIMESTAMP without time zone,
   contract_number VARCHAR(250),
   approved VARCHAR(500),
   amount_without_dph Float,
   amount_with_dph Float,
   amount_different_currency Float,
   currency VARCHAR(50),
   hash_value VARCHAR(100),
   link_pdf VARCHAR(250),
   valid VARCHAR(5),
   linked_record VARCHAR(250)
);

DROP TABLE IF EXISTS invoice;
CREATE TABLE invoice(
   invoice_id serial PRIMARY KEY,
   ministry_ico VARCHAR(20),
   ministry_name VARCHAR(500),
   supplier_ico VARCHAR(20),
   supplier_name VARCHAR(500),
   amount Float,
   currency VARCHAR(20),
   purpose VARCHAR(1000),
   supplier_invoice_identifier VARCHAR(100),
   document_label VARCHAR(100),
   document_number VARCHAR(100),
   variable_symbol VARCHAR(100),
   date_acceptance TIMESTAMP without time zone,
   date_payment TIMESTAMP without time zone,
   date_due TIMESTAMP without time zone,
   date_issue TIMESTAMP without time zone,
   budget_item_code VARCHAR(100),
   budget_item_name VARCHAR(200),
   contract_identifier VARCHAR(100),
   amount_per_item Float,
   amount_without_tax Float,
   amount_in_diff_currency Float
);

DROP TABLE IF EXISTS contract_attachment;
CREATE TABLE contract_attachment(
   contract_attachment_id serial PRIMARY KEY,
   contract_id Integer,
   name VARCHAR(100),
   hash_value VARCHAR(100),
   link VARCHAR(100),
   CONSTRAINT contract_id_fkey FOREIGN KEY (contract_id)
      REFERENCES contract (contract_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

DROP TABLE IF EXISTS possible_relation;
CREATE TABLE possible_relation(
    possible_relation_id serial PRIMARY KEY,
    contract_id Integer,
    invoice_id Integer,
    final_score float,
    final boolean,
    CONSTRAINT contract_id_fkey FOREIGN KEY (contract_id)
      REFERENCES contract (contract_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT invoice_id_fkey FOREIGN KEY (invoice_id)
      REFERENCES invoice (invoice_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

DROP TABLE IF EXISTS test_result;
CREATE TABLE test_result(
    test_id serial PRIMARY KEY,
    possible_relation_id INTEGER,
    test_name VARCHAR(50),
    test_result float,
    CONSTRAINT possible_relation_id_fkey FOREIGN KEY (possible_relation_id)
      REFERENCES possible_relation (possible_relation_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)