create table INTERN_TEAM8.stg_user as select * from INTERN_TEAM8.users_user  where 1=0

create table INTERN_TEAM8.stg_user_del as select id from INTERN_TEAM8.users_user where 1=0;

create table INTERN_TEAM8.meta (
    schema_name varchar(30),
    table_name varchar(30),
    max_update_dt date
);


create table INTERN_TEAM8.dwh_user_hist (
	id INTEGER NOT NULL,
	password NVARCHAR2(128),
	last_login TIMESTAMP,
	is_superuser NUMBER(1,0) NOT NULL,
	username NVARCHAR2(11) NOT NULL,
	first_name NVARCHAR2(150) NOT NULL,
	last_name NVARCHAR2(150) NOT NULL,
	email NVARCHAR2(254) NOT NULL,
	is_staff NUMBER(1,0) NOT NULL,
	is_active NUMBER(1,0) NOT NULL,
	role NVARCHAR2(8) NOT NULL,
	effective_from DATE,
	effective_to DATE,
    deleted_flg CHAR(1)
);


-- 1. Загрузка в STG (захват, extract)
-- Сначало записи в таблицах удаляются
truncate table INTERN_TEAM8.stg_user;
truncate table INTERN_TEAM8.stg_user_del;

-- Далее данные из источников загружаются в stg-слой как есть. Условие, что дата записей в источнике больше последней сохраненной записи даты в метаданных --или больше минимальной возможной даты в случае, если записей в метаданных нет
insert into INTERN_TEAM8.stg_user ( id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, role )
select id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, role
from INTERN_TEAM8.users_user
where  TRUNC(date_joined) > coalesce (
    (select max_update_dt
    from INTERN_TEAM8.meta
    where schema_name = 'INTERN_TEAM8' and table_name = 'META'), to_date('01.01.1800 00:00:00','DD.MM.YYYY HH24:MI:SS') );

--Сохраняем id, для дальнейшей обработки удаленных записей
insert into INTERN_TEAM8.stg_user_del ( id )
select id from INTERN_TEAM8.users_user;

-- 2. Выделение вставок и изменений (transform); вставка в их приемник (load)

-- К таблице из tgt присоединяем таблицу из stg по ключу, где ключ stg-таблицы не нулевой, запись есть и она актуальная. Вставляем в tgt-слой данные из stg, --в effective_from прописываем либо дату из метаданных, либо минимальную дату(01.01.1800) в случае если в метаданных записей не было. Делаем запись --актуальной(31.12.9999), ставим флаг 0-запись не удалена.
insert into INTERN_TEAM8.dwh_user_hist (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, role, effective_from, effective_to, deleted_flg ) 
select stg.id, stg.password, stg.last_login, stg.is_superuser, stg.username, stg.first_name, stg.last_name, stg.email, stg.is_staff, stg.is_active, stg.role,stg.date_joined , TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0
FROM INTERN_TEAM8.dwh_user_hist tgt
left join INTERN_TEAM8.stg_user stg
on tgt.id = stg.id 
where stg.id is not NULL 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy');
and (1=0
    or (stg.password <> tgt.password or (stg.password is null and tgt.password is not null ) or ( stg.password is not null and tgt.password is null ))
	or (stg.last_login <> tgt.last_login or ( stg.last_login is null and tgt.last_login is not null ) or ( stg.last_login is not null and tgt.last_login is null ))
	or (stg.is_superuser <> tgt.is_superuser or ( stg.is_superuser is null and tgt.is_superuser is not null ) or ( stg.is_superuser is not null and tgt.is_superuser is null ))
	or (stg.username <> tgt.username or ( stg.username is null and tgt.username is not null ) or ( stg.username is not null and tgt.username is null ))
	or (stg.first_name <> tgt.first_name or ( stg.first_name is null and tgt.first_name is not null ) or ( stg.first_name is not null and tgt.first_name is null ))
	or (stg.last_name <> tgt.last_name or ( stg.last_name is null and tgt.last_name is not null ) or ( stg.last_name is not null and tgt.last_name is null ))
	or (stg.email <> tgt.email or ( stg.email is null and tgt.email is not null ) or ( stg.email is not null and tgt.email is null ))
	or (stg.is_staff <> tgt.is_staff or ( stg.is_staff is null and tgt.is_staff is not null ) or ( stg.is_staff is not null and tgt.is_staff is null ))
	or (stg.is_active <> tgt.is_active or ( stg.is_active is null and tgt.is_active is not null ) or ( stg.is_active is not null and tgt.is_active is null ))
	or (stg.role <> tgt.role or ( stg.role is null and tgt.role is not null ) or ( stg.role is not null and tgt.role is null )))

--Если в результате предыдущего инсерта записи вставились, выполняется обновление в tgt предыдущей строки с таким же id. Изменяется effective_to - ставиться дата предыдущего дня, предшествующего новой записи
--Если в результате предыдущего инсерта записи не вставились, новые записи вставляются в tgt.
merge into INTERN_TEAM8.dwh_user_hist tgt
using INTERN_TEAM8.stg_user stg
on( stg.id = tgt.id )
when matched then 
    update set tgt.effective_to=TRUNC(stg.date_joined) - INTERVAL '1' SECOND, deleted_flg = 0
    where effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
	and (1=0
    or (stg.password <> tgt.password or (stg.password is null and tgt.password is not null ) or ( stg.password is not null and tgt.password is null ))
	or (stg.last_login <> tgt.last_login or ( stg.last_login is null and tgt.last_login is not null ) or ( stg.last_login is not null and tgt.last_login is null ))
	or (stg.is_superuser <> tgt.is_superuser or ( stg.is_superuser is null and tgt.is_superuser is not null ) or ( stg.is_superuser is not null and tgt.is_superuser is null ))
	or (stg.username <> tgt.username or ( stg.username is null and tgt.username is not null ) or ( stg.username is not null and tgt.username is null ))
	or (stg.first_name <> tgt.first_name or ( stg.first_name is null and tgt.first_name is not null ) or ( stg.first_name is not null and tgt.first_name is null ))
	or (stg.last_name <> tgt.last_name or ( stg.last_name is null and tgt.last_name is not null ) or ( stg.last_name is not null and tgt.last_name is null ))
	or (stg.email <> tgt.email or ( stg.email is null and tgt.email is not null ) or ( stg.email is not null and tgt.email is null ))
	or (stg.is_staff <> tgt.is_staff or ( stg.is_staff is null and tgt.is_staff is not null ) or ( stg.is_staff is not null and tgt.is_staff is null ))
	or (stg.is_active <> tgt.is_active or ( stg.is_active is null and tgt.is_active is not null ) or ( stg.is_active is not null and tgt.is_active is null ))
	or (stg.role <> tgt.role or ( stg.role is null and tgt.role is not null ) or ( stg.role is not null and tgt.role is null )))
when not matched then 
    insert ( id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, role, effective_from, effective_to, deleted_flg) 
    values (stg.id, stg.password, stg.last_login, stg.is_superuser, stg.username, stg.first_name, stg.last_name, stg.email, stg.is_staff, stg.is_active, stg.role, stg.date_joined, , TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0);
	
-- 3. Обработка удалений.
--К таблице tgt присоединяется таблица из stg с id. Если в stg нет id, а в tgt такой id есть, запись активна и флага удаления нет, то в tgt вставляется(как --бы дублируется) запись с этим id, но в effective_from записывается текущая дата, запись ставится активной и ставиться флаг удаления
insert into INTERN_TEAM8.dwh_user_hist (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, role, effective_from, effective_to, deleted_flg)  
select tgt.id, tgt.password, tgt.last_login, tgt.is_superuser, tgt.username, tgt.first_name, tgt.last_name, tgt.email, tgt.is_staff, tgt.is_active, tgt.role, to_date((select max_update_dt from INTERN_TEAM8.meta), 'dd.mm.yyyy'), TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 1
from INTERN_TEAM8.dwh_user_hist tgt 
left join INTERN_TEAM8.stg_user_del stg
on tgt.id = stg.id
where stg.id is null 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy') 
and deleted_flg <> 1;


--Далее обновляется предыдущая дата, где effective_to становится предыдущим днем, предшествующим удалению записи
update INTERN_TEAM8.dwh_user_hist
set effective_to = (select distinct effective_from  - INTERVAL '1' SECOND from INTERN_TEAM8.dwh_user_hist where deleted_flg = 1 and effective_from = (select max(effective_from) from INTERN_TEAM8.dwh_user_hist))
where id in(
    select tgt.id
    from INTERN_TEAM8.dwh_user_hist tgt 
    left join INTERN_TEAM8.stg_user_del stg
    on tgt.id = stg.id
    where stg.id is null )
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
and deleted_flg = 0 ;



-- 4. Обновление метаданных.
--При первой записи идет запись очень маленькой даты(01.01.1800), далее дата будет обвовляться в зависимости от даты приходящей записи от источника

merge into INTERN_TEAM8.meta m1
USING ( select 'INTERN_TEAM8' schema_name, 'META' table_name, ( select coalesce (max( date_joined ), current_date) from INTERN_TEAM8.stg_user ) max_update_dt from dual ) m2
on (m1.schema_name = m2.schema_name and m1.table_name = m2.table_name)
when matched then 
	update set m1.max_update_dt = m2.max_update_dt
    where m2.max_update_dt is not null
WHEN NOT matched THEN 
	INSERT (schema_name, table_name, max_update_dt)
	VALUES ( 'INTERN_TEAM8','USERS_USER', to_date(select coalesce (max( date_joined ), current_date) from INTERN_TEAM8.stg_user), 'dd.mm.yyyy'  );

commit;