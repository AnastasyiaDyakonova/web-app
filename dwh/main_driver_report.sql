create table INTERN_TEAM8.stg_driver_report as select * from INTERN_TEAM8.main_driver_report  where 1=0

create table INTERN_TEAM8.stg_driver_report_del as select ID from INTERN_TEAM8.main_driver_report where 1=0;


create table INTERN_TEAM8.dwh_driver_report_hist (
	id INTEGER NOT NULL, 
	task_number INTEGER NOT NULL , 
	odometr_from INTEGER NOT NULL , 
	odometr_to INTEGER NOT NULL , 
	check_number INTEGER NOT NULL , 
	date_check DATE NOT NULL , 
	sum_check FLOAT(126) NOT NULL , 
	image_check NVARCHAR2(500),
	effective_from DATE,
	effective_to DATE,
    deleted_flg CHAR(1)
);


-- 1. Загрузка в STG (захват, extract)
truncate table INTERN_TEAM8.stg_driver_report;
truncate table INTERN_TEAM8.stg_driver_report_del;


insert into INTERN_TEAM8.stg_driver_report ( id, task_number, odometr_from, odometr_to, check_number, date_check, sum_check, image_check, date_create_driver_report)
select id, task_number, odometr_from, odometr_to, check_number, date_check, sum_check, image_check, date_create_driver_report
from INTERN_TEAM8.main_driver_report
where  date_create_driver_report > coalesce (
    (select max_update_dt
    from INTERN_TEAM8.meta
    where schema_name = 'INTERN_TEAM8' and table_name = 'META'), to_date('01.01.1800 00:00:00','DD.MM.YYYY HH24:MI:SS') );

insert into INTERN_TEAM8.stg_driver_report_del ( id )
select id from INTERN_TEAM8.main_driver_report;

-- 2. Выделение вставок и изменений (transform); вставка в их приемник (load)

insert into INTERN_TEAM8.dwh_driver_report_hist ( id, task_number, odometr_from, odometr_to, check_number, date_check, sum_check, image_check, effective_from, effective_to, deleted_flg ) 
select stg.id, stg.task_number, stg.odometr_from, stg.odometr_to, stg.check_number, stg.date_check, stg.sum_check, stg.image_check, stg.date_create_driver_report, TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0
FROM INTERN_TEAM8.dwh_driver_report_hist tgt
left join INTERN_TEAM8.stg_driver_report stg
on tgt.id = stg.id 
where stg.id is not NULL 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
	and (1=0
    or (stg.task_number <> tgt.task_number or (stg.task_number is null and tgt.task_number is not null ) or ( stg.task_number is not null and tgt.task_number is null ))
	or (stg.odometr_from <> tgt.odometr_from or ( stg.odometr_from is null and tgt.odometr_from is not null ) or ( stg.odometr_from is not null and tgt.odometr_from is null ))
	or (stg.odometr_to <> tgt.odometr_to or ( stg.odometr_to is null and tgt.odometr_to is not null ) or ( stg.odometr_to is not null and tgt.odometr_to is null ))
	or (stg.check_number <> tgt.check_number or ( stg.check_number is null and tgt.check_number is not null ) or ( stg.check_number is not null and tgt.check_number is null ))
	or (stg.date_check <> tgt.date_check or ( stg.date_check is null and tgt.date_check is not null ) or ( stg.date_check is not null and tgt.date_check is null ))
	or (stg.sum_check <> tgt.sum_check or ( stg.sum_check is null and tgt.sum_check is not null ) or ( stg.sum_check is not null and tgt.sum_check is null ))
	or (stg.image_check <> tgt.image_check or ( stg.image_check is null and tgt.image_check is not null ) or ( stg.image_check is not null and tgt.image_check is null )));


merge into INTERN_TEAM8.dwh_driver_report_hist tgt
using INTERN_TEAM8.stg_driver_report stg
on( stg.id = tgt.id )
when matched then 
    update set tgt.effective_to=stg.date_create_driver_report - INTERVAL '1' SECOND, deleted_flg = 0
    where effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
	and (1=0
    or (stg.task_number <> tgt.task_number or (stg.task_number is null and tgt.task_number is not null ) or ( stg.task_number is not null and tgt.task_number is null ))
	or (stg.odometr_from <> tgt.odometr_from or ( stg.odometr_from is null and tgt.odometr_from is not null ) or ( stg.odometr_from is not null and tgt.odometr_from is null ))
	or (stg.odometr_to <> tgt.odometr_to or ( stg.odometr_to is null and tgt.odometr_to is not null ) or ( stg.odometr_to is not null and tgt.odometr_to is null ))
	or (stg.check_number <> tgt.check_number or ( stg.check_number is null and tgt.check_number is not null ) or ( stg.check_number is not null and tgt.check_number is null ))
	or (stg.date_check <> tgt.date_check or ( stg.date_check is null and tgt.date_check is not null ) or ( stg.date_check is not null and tgt.date_check is null ))
	or (stg.sum_check <> tgt.sum_check or ( stg.sum_check is null and tgt.sum_check is not null ) or ( stg.sum_check is not null and tgt.sum_check is null ))
	or (stg.image_check <> tgt.image_check or ( stg.image_check is null and tgt.image_check is not null ) or ( stg.image_check is not null and tgt.image_check is null )))
when not matched then 
    insert (id, task_number, odometr_from, odometr_to, check_number, date_check, sum_check, image_check, effective_from,  effective_to, deleted_flg ) 
    values (stg.id, stg.task_number, stg.odometr_from, stg.odometr_to, stg.check_number, stg.date_check, stg.sum_check, stg.image_check, stg.date_create_driver_report, TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0);
	
---- 3. Обработка удалений.	
insert into INTERN_TEAM8.dwh_driver_report_hist ( id, task_number, odometr_from, odometr_to, check_number, date_check, sum_check, image_check, effective_from,  effective_to, deleted_flg)  
select tgt.id, tgt.task_number, tgt.odometr_from, tgt.odometr_to, tgt.check_number, tgt.date_check, tgt.sum_check, tgt.image_check, to_date((select max_update_dt from INTERN_TEAM8.meta), 'dd.mm.yyyy'), TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 1
from INTERN_TEAM8.dwh_driver_report_hist  tgt 
left join INTERN_TEAM8.stg_driver_report_del stg
on tgt.id = stg.id
where stg.id is null 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy') 
and deleted_flg <> 1;

update INTERN_TEAM8.dwh_driver_report_hist
set effective_to = (select distinct effective_from  - INTERVAL '1' SECOND from INTERN_TEAM8.dwh_driver_report_hist where deleted_flg = 1 and effective_from = (select max(effective_from) from INTERN_TEAM8.dwh_driver_report_hist))
where id in(
    select tgt.id
    from INTERN_TEAM8.dwh_driver_report_hist tgt 
    left join INTERN_TEAM8.stg_driver_report_del stg
    on tgt.id = stg.id
    where stg.id is null )
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
and deleted_flg = 0 ;


-- 4. Обновление метаданных.

commit;