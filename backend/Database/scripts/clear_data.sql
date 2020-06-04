delete from invoice;
alter sequence invoice_invoice_id_seq RESTART;

delete from contract;
alter sequence contract_contract_id_seq RESTART;

delete from test_result;
ALTER SEQUENCE test_result_test_result_id_seq RESTART;

delete from possible_relation;
ALTER SEQUENCE possible_relation_possible_relation_id_seq RESTART;

delete from contract_warning;
alter sequence public.contract_warning_contract_warning_id_seq RESTART;