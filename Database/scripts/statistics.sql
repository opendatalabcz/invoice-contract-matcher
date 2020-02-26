select * from contract where valid = '0'
--Pocet vsech smluv
select count(*) from contract
;

--Pocet vyskytu dat (kontrola zda nechybí)
select count(*), count(date_published), count(date_agreed) from contract
;

--Pocet smluv po mesicich
select
       to_char(co.date_published, 'YYYY_MM') as mesic,
       count(co.contract_id) as pocet
from contract co
group by to_char(co.date_published, 'YYYY_MM')
order by 1
;

--Vypis vsech smluv v databazi
select * from invoice
;
--delka jednotlivych atributu
select
    max(length(external_id)) as external_id_max,               --varchar(50)
    min(length(external_id)) as external_id_min,               --varchar(50)
    max(length(version_id)) as version_id_max,                --varchar(50)
    min(length(version_id)) as version_id_min,                --varchar(50)
    max(length(link)) as link_max,                      --varchar(50)
    min(length(link)) as link_min,                      --varchar(50)
    max(length(ministry_name)) as ministry_name_max,             --varchar(500)
    min(length(ministry_name)) as ministry_name_min,             --varchar(500)
    max(length(ministry_data_box)) as ministry_data_box_max,         --varchar(7)
    min(length(ministry_data_box)) as ministry_data_box_min,         --varchar(7)
    max(length(ministry_ico)) as ministry_ico_max,              --varchar(20)
    min(length(ministry_ico)) as ministry_ico_min,              --varchar(20)
    max(length(ministry_address)) as ministry_address_max,          --varchar(500)
    min(length(ministry_address)) as ministry_address_min,          --varchar(500)
    max(length(ministry_department)) as ministry_department_max,       --varchar(200)
    min(length(ministry_department)) as ministry_department_min,       --varchar(200)
    max(length(ministry_payer_flag)) as ministry_payer_flag_max,       --varchar(5)
    min(length(ministry_payer_flag)) as ministry_payer_flag_min,       --varchar(5)
    max(length(supplier_name)) as supplier_name_max,             --varchar(500)
    min(length(supplier_name)) as supplier_name_min,             --varchar(500)
    max(length(supplier_date_box)) as supplier_date_box_max,         --varchar(7)
    min(length(supplier_date_box)) as supplier_date_box_min,         --varchar(7)
    max(length(supplier_ico)) as supplier_ico_max,              --varchar(20)
    min(length(supplier_ico)) as supplier_ico_min,              --varchar(20)
    max(length(supplier_address)) as supplier_address_max,          --varchar(500)
    min(length(supplier_address)) as supplier_address_min,          --varchar(500)
    max(length(supplier_department)) as supplier_department_max,       --varchar(200)
    min(length(supplier_department)) as supplier_department_min,       --varchar(200)
    max(length(supplier_receiver_flag)) as supplier_receiver_flag_max,    --varchar(5)
    min(length(supplier_receiver_flag)) as supplier_receiver_flag_min,    --varchar(5)
    max(length(purpose)) as purpose_max,                   --varchar(1000)
    min(length(purpose)) as purpose_min,                   --varchar(1000)
    max(length(contract_number)) as contract_number_max,           --varchar(250)
    min(length(contract_number)) as contract_number_min,           --varchar(250)
    max(length(approved)) as approved_max,                  --varchar(500)
    min(length(approved)) as approved_min,                  --varchar(500)
    max(length(currency)) as currency_max,                  --varchar(50)
    min(length(currency)) as currency_min,                  --varchar(50)
    max(length(hash_value)) as hash_value_max,                --varchar(100)
    min(length(hash_value)) as hash_value_min,                --varchar(100)
    max(length(link_pdf)) as link_pdf_max,                  --varchar(250)
    min(length(link_pdf)) as link_pdf_min,                  --varchar(250)
    max(length(valid)) as valid_max,                    --varchar(5)
    min(length(valid)) as valid_min,                    --varchar(5)
    max(length(linked_record)) as linked_record_max,             --varchar(250)
    min(length(linked_record)) as linked_record_min             --varchar(250)
from contract
;

--Rozdeleni kdy je ministerstvo na miste ministerstva nebo na strane dodavatele
select
    sum(case when co.ministry_name like '%Ministerstvo%' then 1 else 0 end) ministerstvo,
    sum(case when co.supplier_name like '%Ministerstvo%' then 1 else 0 end) supplier
from contract co
;

--Ministerstva, ICO a pocet smluv na ne
select
    case when ministry_name like '%Ministerstvo%' then ministry_name else supplier_name end as name,
    case when ministry_name like '%Ministerstvo%' then ministry_ico else supplier_ico end as ico,
    count(contract_id) as pocet_smluv,
    count(amount_different_currency),
    count(amount_with_dph),
    count(amount_without_dph)
from contract
where ministry_name like '%Ministerstvo%' or supplier_name like '%Ministerstvo%'
group by
    case when ministry_name like '%Ministerstvo%' then ministry_name else supplier_name end,
    case when ministry_name like '%Ministerstvo%' then ministry_ico else supplier_ico end
order by 3 desc, 1, 2


;

--

select co.version_id, sum(1) as count
from contract co
group by co.version_id
;
-- navazane smlouvy
select co.external_id, co.linked_record, co1.external_id, co1.linked_record, co2.external_id, co2.linked_record
from contract co
left join contract co1 on co1.external_id = co.linked_record
left join contract co2 on co2.external_id = co1.linked_record
where co.linked_record is not null
;
select * from possible_relation