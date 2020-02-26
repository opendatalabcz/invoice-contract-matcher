INSERT INTO public.contract(
	contract_id, external_id, version_id, link, date_published, ministry_name, ministry_data_box, ministry_ico, ministry_address, ministry_department, ministry_payer_flag, supplier_name, supplier_date_box, supplier_ico, supplier_address, supplier_department, supplier_receiver_flag, purpose, date_agreed, contract_number, approved, amount_without_dph, amount_with_dph, amount_different_currency, currency, hash_value, link_pdf, valid, linked_record)
	VALUES ({contract_id}, {external_id}, {version_id}, {link}, {date_published}, {ministry_name}, {ministry_data_box}, {ministry_ico}, {ministry_address}, {ministry_department}, {ministry_payer_flag}, {supplier_name}, {supplier_date_box}, {supplier_ico}, {supplier_address}, {supplier_department}, {supplier_receiver_flag}, {purpose}, {date_agreed}, {contract_number}, {approved}, {amount_without_dph}, {amount_with_dph}, {amount_different_currency}, {currency}, {hash_value}, {link_pdf}, {valid}, {linked_record});