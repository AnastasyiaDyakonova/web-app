create table INTERN_TEAM8.stg_catalog_route_url as select * from INTERN_TEAM8.main_catalog_route_url where 1=0;

create table INTERN_TEAM8.stg_catalog_route_url_del as select number_route from INTERN_TEAM8.main_catalog_route_url where 1=0;


create table INTERN_TEAM8.dwh_catalog_route_url_hist (
	number_route varchar2(7) NOT NULL,
	count_point_to_route integer NOT NULL,
	url_route varchar2(500) NOT null,
	effective_from date,
	effective_to date,
    deleted_flg char(1)
);

create table INTERN_TEAM8.dwh_catalog_route_point_hist (
	number_route varchar(7) NOT NULL,
	point_1 NVARCHAR2(20) NOT NULL,
	point_2 NVARCHAR2(20) NOT NULL,
	point_3 NVARCHAR2(20) NOT NULL,
	point_4 NVARCHAR2(20) NOT NULL,
	point_5 NVARCHAR2(20) NOT NULL,
	point_6 NVARCHAR2(20) NOT NULL,
	point_7 NVARCHAR2(20) NOT NULL,
	point_8 NVARCHAR2(20) NOT NULL,
	point_9 NVARCHAR2(20) NOT NULL,
	point_10 NVARCHAR2(20) NOT NULL,
	effective_from date,
	effective_to date,
    deleted_flg char(1)
);


-- 1. Загрузка в STG (захват, extract)
truncate table INTERN_TEAM8.stg_catalog_route_url;
truncate table INTERN_TEAM8.stg_catalog_route_url_del;


insert into INTERN_TEAM8.stg_catalog_route_url ( number_route, count_point_to_route, point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9, point_10, url_route, date_create_route)
select number_route, count_point_to_route, point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9, point_10, url_route, date_create_route 
from INTERN_TEAM8.main_catalog_route_url
where  date_create_route > coalesce (
    (select max_update_dt
    from INTERN_TEAM8.meta
    where schema_name = 'INTERN_TEAM8' and table_name = 'META'), to_date('01.01.1800 00:00:00','DD.MM.YYYY HH24:MI:SS') );

insert into INTERN_TEAM8.stg_catalog_route_url_del ( number_route )
select number_route from INTERN_TEAM8.main_catalog_route_url;

-- 2. Выделение вставок и изменений (transform); вставка в их приемник (load)

insert into INTERN_TEAM8.dwh_catalog_route_url_hist (number_route, count_point_to_route, url_route, effective_from, effective_to, deleted_flg ) 
select stg.number_route, stg.count_point_to_route, stg.url_route, stg.date_create_route, TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0
FROM INTERN_TEAM8.dwh_catalog_route_url_hist tgt
left join INTERN_TEAM8.stg_catalog_route_url stg
on tgt.number_route = stg.number_route 
where stg.number_route is not NULL 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
and (1=0
    or (stg.count_point_to_route <> tgt.count_point_to_route or (stg.count_point_to_route is null and tgt.count_point_to_route is not null ) or ( stg.count_point_to_route is not null and tgt.count_point_to_route is null ))
	or (stg.url_route <> tgt.url_route or ( stg.url_route is null and tgt.url_route is not null ) or ( stg.url_route is not null and tgt.url_route is null)))


merge into INTERN_TEAM8.dwh_catalog_route_url_hist tgt
using INTERN_TEAM8.stg_catalog_route_url stg
on( stg.number_route = tgt.number_route )
when matched then 
    update set tgt.effective_to=stg.date_create_route - INTERVAL '1' SECOND, deleted_flg = 0
    where effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
	and (1=0
	or (stg.count_point_to_route <> tgt.count_point_to_route or (stg.count_point_to_route is null and tgt.count_point_to_route is not null ) or ( stg.count_point_to_route is not null and tgt.count_point_to_route is null ))
	or (stg.url_route <> tgt.url_route or ( stg.url_route is null and tgt.url_route is not null ) or ( stg.url_route is not null and tgt.url_route is null)))
when not matched then 
    insert ( number_route, count_point_to_route, url_route, effective_from, effective_to, deleted_flg) 
    values (stg.number_route, stg.count_point_to_route, stg.url_route, stg.date_create_route, TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0);
	


insert into INTERN_TEAM8.dwh_catalog_route_point_hist (number_route, point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9, point_10, effective_from, effective_to, deleted_flg) 
select stg.number_route, stg.point_1, stg.point_2, stg.point_3, stg.point_4, stg.point_5, stg.point_6, stg.point_7, stg.point_8, stg.point_9, stg.point_10, stg.date_create_route, TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0
FROM INTERN_TEAM8.dwh_catalog_route_point_hist tgt
left join INTERN_TEAM8.stg_catalog_route_url stg
on tgt.number_route = stg.number_route 
where stg.number_route is not NULL 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
	and (1=0
	or (stg.point_1 <> tgt.point_1 or ( stg.point_1 is null and tgt.point_1 is not null ) or ( stg.point_1 is not null and tgt.point_1 is null ))
	or (stg.point_2 <> tgt.point_2 or ( stg.point_2 is null and tgt.point_2 is not null ) or ( stg.point_2 is not null and tgt.point_2 is null ))
	or (stg.point_3 <> tgt.point_3 or ( stg.point_3 is null and tgt.point_3 is not null ) or ( stg.point_3 is not null and tgt.point_3 is null ))
	or (stg.point_4 <> tgt.point_4 or ( stg.point_4 is null and tgt.point_4 is not null ) or ( stg.point_4 is not null and tgt.point_4 is null ))
	or (stg.point_5 <> tgt.point_5 or ( stg.point_5 is null and tgt.point_5 is not null ) or ( stg.point_5 is not null and tgt.point_5 is null ))
	or (stg.point_6 <> tgt.point_6 or ( stg.point_6 is null and tgt.point_6 is not null ) or ( stg.point_6 is not null and tgt.point_6 is null ))
	or (stg.point_7 <> tgt.point_7 or ( stg.point_7 is null and tgt.point_7 is not null ) or ( stg.point_7 is not null and tgt.point_7 is null ))
	or (stg.point_8 <> tgt.point_8 or ( stg.point_8 is null and tgt.point_8 is not null ) or ( stg.point_8 is not null and tgt.point_8 is null ))
	or (stg.point_9 <> tgt.point_9 or ( stg.point_9 is null and tgt.point_9 is not null ) or ( stg.point_9 is not null and tgt.point_9 is null ))
	or (stg.point_10 <> tgt.point_10 or ( stg.point_10 is null and tgt.point_10 is not null ) or ( stg.point_10 is not null and tgt.point_10 is null )));
	
	
merge into INTERN_TEAM8.dwh_catalog_route_point_hist tgt
using INTERN_TEAM8.stg_catalog_route_url stg
on( stg.number_route = tgt.number_route )
when matched then 
    update set tgt.effective_to=stg.date_create_route - INTERVAL '1' SECOND, deleted_flg = 0
    where effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
	and (1=0
	or (stg.point_1 <> tgt.point_1 or ( stg.point_1 is null and tgt.point_1 is not null ) or ( stg.point_1 is not null and tgt.point_1 is null ))
	or (stg.point_2 <> tgt.point_2 or ( stg.point_2 is null and tgt.point_2 is not null ) or ( stg.point_2 is not null and tgt.point_2 is null ))
	or (stg.point_3 <> tgt.point_3 or ( stg.point_3 is null and tgt.point_3 is not null ) or ( stg.point_3 is not null and tgt.point_3 is null ))
	or (stg.point_4 <> tgt.point_4 or ( stg.point_4 is null and tgt.point_4 is not null ) or ( stg.point_4 is not null and tgt.point_4 is null ))
	or (stg.point_5 <> tgt.point_5 or ( stg.point_5 is null and tgt.point_5 is not null ) or ( stg.point_5 is not null and tgt.point_5 is null ))
	or (stg.point_6 <> tgt.point_6 or ( stg.point_6 is null and tgt.point_6 is not null ) or ( stg.point_6 is not null and tgt.point_6 is null ))
	or (stg.point_7 <> tgt.point_7 or ( stg.point_7 is null and tgt.point_7 is not null ) or ( stg.point_7 is not null and tgt.point_7 is null ))
	or (stg.point_8 <> tgt.point_8 or ( stg.point_8 is null and tgt.point_8 is not null ) or ( stg.point_8 is not null and tgt.point_8 is null ))
	or (stg.point_9 <> tgt.point_9 or ( stg.point_9 is null and tgt.point_9 is not null ) or ( stg.point_9 is not null and tgt.point_9 is null ))
	or (stg.point_10 <> tgt.point_10 or ( stg.point_10 is null and tgt.point_10 is not null ) or ( stg.point_10 is not null and tgt.point_10 is null )))
when not matched then 
    insert ( number_route, point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9, point_10, effective_from, effective_to, deleted_flg) 
    values (stg.number_route, stg.point_1, stg.point_2, stg.point_3, stg.point_4, stg.point_5, stg.point_6, stg.point_7, stg.point_8, stg.point_9, stg.point_10, stg.date_create_route , TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0);
   



-- 3. Обработка удалений.
insert into INTERN_TEAM8.dwh_catalog_route_url_hist ( number_route, count_point_to_route, url_route, effective_from, effective_to, deleted_flg)  
select tgt.number_route, tgt.count_point_to_route, tgt.url_route, to_date((select max_update_dt from INTERN_TEAM8.meta), 'dd.mm.yyyy'), TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 1
from INTERN_TEAM8.dwh_catalog_route_url_hist tgt 
left join INTERN_TEAM8.stg_catalog_route_url_del stg
on tgt.number_route = stg.number_route
where stg.number_route is null 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy') 
and deleted_flg <> 1;



update INTERN_TEAM8.dwh_catalog_route_url_hist
set effective_to = (select distinct effective_from  - INTERVAL '1' SECOND from INTERN_TEAM8.dwh_catalog_route_url_hist where deleted_flg = 1 and effective_from = (select max(effective_from) from INTERN_TEAM8.dwh_catalog_route_url_hist))
where number_route in(
    select tgt.number_route
    from INTERN_TEAM8.dwh_catalog_route_url_hist tgt 
    left join INTERN_TEAM8.stg_catalog_route_url_del stg
    on tgt.number_route = stg.number_route
    where stg.number_route is null )
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
and deleted_flg = 0 ;


insert into INTERN_TEAM8.dwh_catalog_route_point_hist ( number_route, point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9, point_10, effective_from, effective_to, deleted_flg) 
select tgt.number_route, tgt.point_1, tgt.point_2, tgt.point_3, tgt.point_4, tgt.point_5, tgt.point_6, tgt.point_7, tgt.point_8, tgt.point_9, tgt.point_10, to_date((select max_update_dt from INTERN_TEAM8.meta), 'dd.mm.yyyy'), TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 1
from INTERN_TEAM8.dwh_catalog_route_point_hist tgt 
left join INTERN_TEAM8.stg_catalog_route_url_del stg
on tgt.number_route = stg.number_route
where stg.number_route is null 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy') 
and deleted_flg <> 1;




update INTERN_TEAM8.dwh_catalog_route_point_hist 
set effective_to = (select distinct effective_from  - INTERVAL '1' SECOND from INTERN_TEAM8.dwh_catalog_route_point_hist  where deleted_flg = 1 and effective_from = (select max(effective_from) from INTERN_TEAM8.dwh_catalog_route_point_hist))
where number_route in(
    select tgt.number_route
    from INTERN_TEAM8.dwh_catalog_route_point_hist tgt 
    left join INTERN_TEAM8.stg_catalog_route_url_del stg
    on tgt.number_route = stg.number_route
    where stg.number_route is null )
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
and deleted_flg = 0 ;


-- 4. Обновление метаданных.

commit;