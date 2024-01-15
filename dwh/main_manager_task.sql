create table INTERN_TEAM8.stg_manager_task as select * from INTERN_TEAM8.main_manager_task  where 1=0

create table INTERN_TEAM8.stg_manager_task_del as select task_number from INTERN_TEAM8.main_manager_task where 1=0;

create table INTERN_TEAM8.dwh_manager_task_hist (
	task_number INTEGER NOT NULL,
	phone_manager NVARCHAR2(11) NOT NULL,
	phone_driver NVARCHAR2(11) NOT NULL,
	number_route NVARCHAR2(7) NOT NULL,
	effective_from DATE,
	effective_to DATE,
    deleted_flg CHAR(1)
);

-- 1. Загрузка в STG (захват, extract)
truncate table INTERN_TEAM8.stg_manager_task;
truncate table INTERN_TEAM8.stg_manager_task_del;


insert into INTERN_TEAM8.stg_manager_task ( task_number, date_task, phone_manager, phone_driver, number_route)
select task_number, date_task, phone_manager, phone_driver, number_route
from INTERN_TEAM8.main_manager_task;
where  date_task > coalesce (
    (select max_update_dt
    from INTERN_TEAM8.meta
    where schema_name = 'INTERN_TEAM8' and table_name = 'META'), to_date('01.01.1800 00:00:00','DD.MM.YYYY HH24:MI:SS') );

insert into INTERN_TEAM8.stg_manager_task_del ( task_number )
select task_number from INTERN_TEAM8.main_manager_task;

-- 2. Выделение вставок и изменений (transform); вставка в их приемник (load)

insert into INTERN_TEAM8.dwh_manager_task_hist (task_number, phone_manager, phone_driver, number_route, effective_from, effective_to, deleted_flg ) 
select stg.task_number, stg.phone_manager, stg.phone_driver, stg.number_route, stg.date_task, TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0
FROM INTERN_TEAM8.dwh_manager_task_hist tgt
left join INTERN_TEAM8.stg_manager_task stg
on tgt.task_number = stg.task_number 
where stg.task_number is not NULL 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
and (1=0
   or (stg.phone_manager <> tgt.phone_manager or ( stg.phone_manager is null and tgt.phone_manager is not null ) or ( stg.phone_manager is not null and tgt.phone_manager is null ))
	or (stg.phone_driver <> tgt.phone_driver or ( stg.phone_driver is null and tgt.phone_driver is not null ) or ( stg.phone_driver is not null and tgt.phone_driver is null ))
	or (stg.number_route <> tgt.number_route or ( stg.number_route is null and tgt.number_route is not null ) or ( stg.number_route is not null and tgt.number_route is null )));



merge into INTERN_TEAM8.dwh_manager_task_hist tgt
using INTERN_TEAM8.stg_manager_task stg
on( stg.task_number = tgt.task_number )
when matched then 
    update set tgt.effective_to=stg.date_task - INTERVAL '1' SECOND, deleted_flg = 0
    where effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
	and (1=0
   or (stg.phone_manager <> tgt.phone_manager or ( stg.phone_manager is null and tgt.phone_manager is not null ) or ( stg.phone_manager is not null and tgt.phone_manager is null ))
	or (stg.phone_driver <> tgt.phone_driver or ( stg.phone_driver is null and tgt.phone_driver is not null ) or ( stg.phone_driver is not null and tgt.phone_driver is null ))
	or (stg.number_route <> tgt.number_route or ( stg.number_route is null and tgt.number_route is not null ) or ( stg.number_route is not null and tgt.number_route is null )))
when not matched then 
    insert ( task_number, phone_manager, phone_driver, number_route, effective_from, effective_to, deleted_flg) 
    values (stg.task_number, stg.phone_manager, stg.phone_driver, stg.number_route, stg.date_task, TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0);
	
-- 3. Обработка удалений.
insert into INTERN_TEAM8.dwh_manager_task_hist ( task_number, phone_manager, phone_driver, number_route, effective_from, effective_to, deleted_flg) 
select tgt.task_number, tgt.phone_manager, tgt.phone_driver, tgt.number_route, to_date((select max_update_dt from INTERN_TEAM8.meta), 'dd.mm.yyyy'), TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 1
from INTERN_TEAM8.dwh_manager_task_hist tgt 
left join INTERN_TEAM8.stg_manager_task_del stg
on tgt.task_number = stg.task_number
where stg.task_number is null 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy') 
and deleted_flg <> 1;

update INTERN_TEAM8.dwh_manager_task_hist
set effective_to = (select distinct effective_from  - INTERVAL '1' SECOND from INTERN_TEAM8.dwh_manager_task_hist where deleted_flg = 1 and effective_from = (select max(effective_from) from INTERN_TEAM8.dwh_manager_task_hist))
where task_number in(
    select tgt.task_number
    from INTERN_TEAM8.dwh_manager_task_hist tgt 
    left join INTERN_TEAM8.stg_manager_task_del stg
    on tgt.task_number = stg.task_number
    where stg.task_number is null )
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
and deleted_flg = 0 ;


-- 4. Обновление метаданных.


commit;
	