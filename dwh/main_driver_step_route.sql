create table INTERN_TEAM8.stg_driver_step_route as select * from INTERN_TEAM8.main_driver_step_route  where 1=0

create table INTERN_TEAM8.stg_driver_step_route_del as select task_number from INTERN_TEAM8.main_driver_step_route where 1=0;

create table INTERN_TEAM8.dwh_driver_step_route_hist (
	task_number INTEGER,
	date_and_time_route_from TIMESTAMP NOT NULL,
	point_1 INTEGER,
	point_2 INTEGER,
	point_3 INTEGER,
	point_4 INTEGER,
	point_5 INTEGER,
	point_6 INTEGER,
	point_7 INTEGER,
	point_8 INTEGER,
	point_9 INTEGER,
	point_10 INTEGER,
	date_and_time_route_to TIMESTAMP NOT NULL,
	effective_from DATE,
	effective_to DATE,
    deleted_flg CHAR(1)
);


-- 1. Загрузка в STG (захват, extract)
truncate table INTERN_TEAM8.stg_driver_step_route;
truncate table INTERN_TEAM8.stg_driver_step_route_del;


insert into INTERN_TEAM8.stg_driver_step_route ( task_number, date_and_time_route_from, point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9, point_10, date_and_time_route_to)
select task_number, date_and_time_route_from, point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9, point_10, date_and_time_route_to
from INTERN_TEAM8.main_driver_step_route
where  TRUNC(date_and_time_route_to  > coalesce (
    (select max_update_dt
    from INTERN_TEAM8.meta
    where schema_name = 'INTERN_TEAM8' and table_name = 'META'), to_date('01.01.1800 00:00:00','DD.MM.YYYY HH24:MI:SS') );

insert into INTERN_TEAM8.stg_driver_step_route_del ( task_number )
select task_number from INTERN_TEAM8.main_driver_step_route;


-- 2. Выделение вставок и изменений (transform); вставка в их приемник (load)

insert into INTERN_TEAM8.dwh_driver_step_route_hist (task_number, date_and_time_route_from, point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9, point_10, date_and_time_route_to, effective_from, effective_to, deleted_flg) 
select stg.task_number, stg.date_and_time_route_from, stg.point_1, stg.point_2, stg.point_3, stg.point_4, stg.point_5, stg.point_6, stg.point_7, stg.point_8, stg.point_9, stg.point_10, stg.date_and_time_route_to, TRUNC(stg.date_and_time_route_to), TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0
FROM INTERN_TEAM8.dwh_driver_step_route_hist tgt
left join INTERN_TEAM8.stg_driver_step_route stg
on tgt.task_number = stg.task_number 
where stg.task_number is not NULL 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
	and (1=0
	or (stg.date_and_time_route_from <> tgt.date_and_time_route_from or ( stg.date_and_time_route_from is null and tgt.date_and_time_route_from is not null ) or ( stg.date_and_time_route_from is not null and tgt.date_and_time_route_from is null ))
	or (stg.point_1 <> tgt.point_1 or ( stg.point_1 is null and tgt.point_1 is not null ) or ( stg.point_1 is not null and tgt.point_1 is null ))
	or stg.point_2 <> tgt.point_2 or ( stg.point_2 is null and tgt.point_2 is not null ) or ( stg.point_2 is not null and tgt.point_2 is null ))
	or (stg.point_3 <> tgt.point_3 or ( stg.point_3 is null and tgt.point_3 is not null ) or ( stg.point_3 is not null and tgt.point_3 is null ))
	or (stg.point_4 <> tgt.point_4 or ( stg.point_4 is null and tgt.point_4 is not null ) or ( stg.point_4 is not null and tgt.point_4 is null ))
	or (stg.point_5 <> tgt.point_5 or ( stg.point_5 is null and tgt.point_5 is not null ) or ( stg.point_5 is not null and tgt.point_5 is null ))
	or (stg.point_6 <> tgt.point_6 or ( stg.point_6 is null and tgt.point_6 is not null ) or ( stg.point_6 is not null and tgt.point_6 is null ))
	or (stg.point_7 <> tgt.point_7 or ( stg.point_7 is null and tgt.point_7 is not null ) or ( stg.point_7 is not null and tgt.point_7 is null ))
	or (stg.point_8 <> tgt.point_8 or ( stg.point_8 is null and tgt.point_8 is not null ) or ( stg.point_8 is not null and tgt.point_8 is null ))
	or (stg.point_9 <> tgt.point_9 or ( stg.point_9 is null and tgt.point_9 is not null ) or ( stg.point_9 is not null and tgt.point_9 is null ))
	or (stg.point_10 <> tgt.point_10 or ( stg.point_10 is null and tgt.point_10 is not null ) or ( stg.point_10 is not null and tgt.point_10 is null ))
	or (stg.date_and_time_route_to <> tgt.date_and_time_route_to or ( stg.date_and_time_route_to is null and tgt.date_and_time_route_to is not null ) or ( stg.date_and_time_route_to is not null and tgt.date_and_time_route_to is null )));
	
	
merge into INTERN_TEAM8.dwh_driver_step_route_hist tgt
using INTERN_TEAM8.stg_driver_step_route stg
on( stg.task_number = tgt.task_number )
when matched then 
    update set tgt.effective_to=TRUNC(stg.date_and_time_route_to )- INTERVAL '1' SECOND, deleted_flg = 0
    where effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
	and (1=0
	or (stg.date_and_time_route_from <> tgt.date_and_time_route_from or ( stg.date_and_time_route_from is null and tgt.date_and_time_route_from is not null ) or ( stg.date_and_time_route_from is not null and tgt.date_and_time_route_from is null ))
	or (stg.point_1 <> tgt.point_1 or ( stg.point_1 is null and tgt.point_1 is not null ) or ( stg.point_1 is not null and tgt.point_1 is null ))
	or stg.point_2 <> tgt.point_2 or ( stg.point_2 is null and tgt.point_2 is not null ) or ( stg.point_2 is not null and tgt.point_2 is null ))
	or (stg.point_3 <> tgt.point_3 or ( stg.point_3 is null and tgt.point_3 is not null ) or ( stg.point_3 is not null and tgt.point_3 is null ))
	or (stg.point_4 <> tgt.point_4 or ( stg.point_4 is null and tgt.point_4 is not null ) or ( stg.point_4 is not null and tgt.point_4 is null ))
	or (stg.point_5 <> tgt.point_5 or ( stg.point_5 is null and tgt.point_5 is not null ) or ( stg.point_5 is not null and tgt.point_5 is null ))
	or (stg.point_6 <> tgt.point_6 or ( stg.point_6 is null and tgt.point_6 is not null ) or ( stg.point_6 is not null and tgt.point_6 is null ))
	or (stg.point_7 <> tgt.point_7 or ( stg.point_7 is null and tgt.point_7 is not null ) or ( stg.point_7 is not null and tgt.point_7 is null ))
	or (stg.point_8 <> tgt.point_8 or ( stg.point_8 is null and tgt.point_8 is not null ) or ( stg.point_8 is not null and tgt.point_8 is null ))
	or (stg.point_9 <> tgt.point_9 or ( stg.point_9 is null and tgt.point_9 is not null ) or ( stg.point_9 is not null and tgt.point_9 is null ))
	or (stg.point_10 <> tgt.point_10 or ( stg.point_10 is null and tgt.point_10 is not null ) or ( stg.point_10 is not null and tgt.point_10 is null ))
	or (stg.date_and_time_route_to <> tgt.date_and_time_route_to or ( stg.date_and_time_route_to is null and tgt.date_and_time_route_to is not null ) or ( stg.date_and_time_route_to is not null and tgt.date_and_time_route_to is null )))
when not matched then 
    insert ( task_number, date_and_time_route_from, point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9, point_10, date_and_time_route_to, effective_from, effective_to, deleted_flg) 
    values (stg.task_number, stg.date_and_time_route_from, stg.point_1, stg.point_2, stg.point_3, stg.point_4, stg.point_5, stg.point_6, stg.point_7, stg.point_8, stg.point_9, stg.point_10, stg.date_and_time_route_to, stg.date_and_time_route_to, TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0);
 


-- 3. Обработка удалений.

insert into INTERN_TEAM8.dwh_driver_step_route_hist ( task_number, date_and_time_route_from, point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9, point_10, date_and_time_route_to, effective_from, effective_to, deleted_flg) 
select tgt.task_number, tgt.date_and_time_route_from, tgt.point_1, tgt.point_2, tgt.point_3, tgt.point_4, tgt.point_5, tgt.point_6, tgt.point_7, tgt.point_8, tgt.point_9, tgt.point_10, tgt.date_and_time_route_to, to_date((select max_update_dt from INTERN_TEAM8.meta), 'dd.mm.yyyy'), TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 1
from INTERN_TEAM8.dwh_driver_step_route_hist tgt 
left join INTERN_TEAM8.stg_driver_step_route_del stg
on tgt.task_number = stg.task_number
where stg.task_number is null 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy') 
and deleted_flg <> 1;


update INTERN_TEAM8.dwh_driver_step_route_hist 
set effective_to = (select distinct effective_from  - INTERVAL '1' SECOND from INTERN_TEAM8.dwh_driver_step_route_hist  where deleted_flg = 1 and effective_from = (select max(effective_from) from INTERN_TEAM8.dwh_driver_step_route_hist))
where task_number in(
    select tgt.task_number
    from INTERN_TEAM8.dwh_driver_step_route_hist tgt 
    left join INTERN_TEAM8.stg_driver_step_route_del stg
    on tgt.task_number = stg.task_number
    where stg.task_number is null )
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
and deleted_flg = 0 ;


-- 4. Обновление метаданных.

commit;


