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

select
    *
from contract
where ministry_name like '%Ministerstvo%' and supplier_ico is null and valid = '1' and ministry_payer_flag = '1'

;
select distinct co.contract_id, co.external_id, co.version_id, co.link, co.date_published, co.ministry_name, co.ministry_data_box,
        co.ministry_ico, co.ministry_address, co.ministry_department, co.ministry_payer_flag, co.supplier_name,
        co.supplier_date_box, co.supplier_ico, co.supplier_address, co.supplier_department, co.supplier_receiver_flag,
        co.purpose, co.date_agreed, co.contract_number, co.approved, co.amount_without_dph, co.amount_with_dph,
        co.amount_different_currency, co.currency, co.hash_value, co.link_pdf, co.valid, co.linked_record
        --, row_number() over (order by co.contract_id, inv.invoice_id) as rn
        from invoice inv
        join contract co on inv.ministry_ico = co.ministry_ico and
                            inv.supplier_ico = co.supplier_ico
        where invoice_id < 1000

;
select
 *
--        invoice_id
from possible_relation
;
select
       contract_id, count(invoice_id)
from possible_relation
group by contract_id
order by count(invoice_id) desc
;

select * from contract
where ministry_name like '%inisterstvo%'

;

select * from contract


select * from invoice

;

select res.rel/res.inv::float as percentage
from (
     select count(distinct pr.invoice_id) as rel,
            count(distinct i.invoice_id) as inv
     from invoice i
     left join possible_relation pr on i.invoice_id = pr.invoice_id
) res



;


select * from contract where contract.ministry_name  like '%Ministerstvo%' --and purpose like '%prodlou%'
and contract_number = '0002/2020'


;

select count(*), sum(case when valid = '1' then 1 else 0 end) from contract


;

with invoices as (
    select *
    from invoice
    limit 100000
)
,contracts as (
    select distinct c.*
    from invoices i
    join contract c on i.ministry_ico = c.ministry_ico and i.supplier_ico = c.supplier_ico
)
select distinct round((1-(c.amount_without_dph/c.amount_with_dph))*100), count(round((1-(c.amount_without_dph/c.amount_with_dph))*100))
from contracts c
group by round((1-(c.amount_without_dph/c.amount_with_dph))*100)
;

select c1.ministry_ico, c2.ministry_ico, c3.ministry_ico, c4.ministry_ico, c1.purpose, c2.purpose, c3.purpose, c4.purpose, c1.amount_with_dph, c2.amount_with_dph, c3.amount_with_dph, c4.amount_with_dph, c1.link, c2.link, c1.external_id, c2.external_id,c1.valid, c2.valid from  (
    select * from contract c1
    where ministry_name like '%Ministerstvo%'
--     limit 10000
) c1
join contract c2 on c2.linked_record = c1.external_id
left join contract c3 on c3.linked_record = c2.external_id
left join contract c4 on c4.linked_record = c3.external_id
;

select * from contract c1
where c1.supplier_ico is null and ministry_name like '%Ministerstvo%' and linked_record is null and valid = '1'
order by amount_without_dph desc


;

select count(contract_id), string_agg(contract_id::varchar,', ') ministry_name, ministry_data_box, ministry_ico, ministry_address,
       ministry_department, ministry_payer_flag, supplier_name, supplier_date_box, supplier_ico, supplier_address,
       supplier_department, supplier_receiver_flag, purpose, date_agreed, contract_number, approved, amount_without_dph,
       amount_with_dph, amount_different_currency, currency, valid
from contract
where valid = '1'
group by ministry_name, ministry_data_box, ministry_ico, ministry_address,
       ministry_department, ministry_payer_flag, supplier_name, supplier_date_box, supplier_ico, supplier_address,
       supplier_department, supplier_receiver_flag, purpose, date_agreed, contract_number, approved, amount_without_dph,
       amount_with_dph, amount_different_currency, currency, valid
order by 1 desc
;
select * from contract where external_id::int in (1026553, 1022093, 1022093, 1022085, 1026517, 1022097, 1022085, 1022097, 1026509, 1026509, 1022073, 1026517, 1026517, 1026525, 1026525, 1022073, 1026537, 1022097, 1026509, 1022073, 1026537, 1022097, 1022085, 1026857, 1026857, 1026553, 1026553, 1026549, 1026549, 1026545, 1026545, 1026541, 1026541, 1026509, 1026541, 1022073, 1026537, 1026537, 1026541, 1026545, 1026525, 1026545, 1022085, 1026549, 1026517, 1026549, 1026525, 1026553, 1026857, 1026857, 1022093, 1022093)


;

select * from contract
where valid = '1' and amount_with_dph < 0 and ministry_name like '%Ministerstvo%'

;

select c1.external_id, string_agg(c2.external_id, ', '), max(c2.amount_with_dph), min(c2.amount_with_dph), max(c2.amount_with_dph) != min(c2.amount_with_dph) from contract c1
join contract c2 on c2.linked_record = c1.external_id
where c1.ministry_name like '%Ministerstvo%'
group by c1.external_id

;

select * from contract where external_id::int = 1095029;
select * from contract where external_id::int in (9532850, 3599744, 6635539, 6781695, 6635751, 6635539, 10083888, 9533258, 4178176, 1329786, 7928727, 5972535, 8129947, 5301207, 5301207, 8580583, 2297234)

;

select count(*) as one from contract where valid = '1' and linked_record is null
;
select count(*) as zero from contract where valid = '0' or linked_record is not null
;

select * from contract where (external_id = '1070517' or linked_record = '1070517') and valid = '1'