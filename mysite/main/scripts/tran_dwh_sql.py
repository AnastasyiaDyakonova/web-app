# 1. Загрузка в STG (захват, extract)
# Сначало записи в таблицах удаляются
tr_stg_user = """truncate table INTERN_TEAM8.stg_user"""
tr_stg_user_del = """truncate table INTERN_TEAM8.stg_user_del"""
tr_stg_driver_step_route = """truncate table INTERN_TEAM8.stg_driver_step_route"""
tr_stg_driver_step_route_del = """truncate table INTERN_TEAM8.stg_driver_step_route_del"""
tr_stg_driver_report = """truncate table INTERN_TEAM8.stg_driver_report"""
tr_stg_driver_report_del = """truncate table INTERN_TEAM8.stg_driver_report_del"""
tr_stg_catalog_route_url = """truncate table INTERN_TEAM8.stg_catalog_route_url"""
tr_stg_catalog_route_url_del = """truncate table INTERN_TEAM8.stg_catalog_route_url_del"""
tr_stg_manager_task = """truncate table INTERN_TEAM8.stg_manager_task"""
tr_stg_manager_task_del = """truncate table INTERN_TEAM8.stg_manager_task_del"""

# Далее данные из источников загружаются в stg-слой как есть. Условие, что дата записей в источнике больше последней сохраненной записи даты в метаданных или больше минимальной возможной даты в случае, если записей в метаданных нет
in_stg_user = """
insert into INTERN_TEAM8.stg_user ( id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, role )
select id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, role
from INTERN_TEAM8.users_user
where  TRUNC(date_joined) > coalesce (
    (select max_update_dt
    from INTERN_TEAM8.meta
    where schema_name = 'INTERN_TEAM8' and table_name = 'META'), to_date('01.01.1800 00:00:00','DD.MM.YYYY HH24:MI:SS') )"""

in_stg_driver_step_route = """
insert into INTERN_TEAM8.stg_driver_step_route ( task_number, date_and_time_route_from, point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9, point_10, date_and_time_route_to)
select task_number, date_and_time_route_from, point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9, point_10, date_and_time_route_to
from INTERN_TEAM8.main_driver_step_route
where  TRUNC(date_and_time_route_to) > coalesce (
    (select max_update_dt
    from INTERN_TEAM8.meta
    where schema_name = 'INTERN_TEAM8' and table_name = 'META'), to_date('01.01.1800 00:00:00','DD.MM.YYYY HH24:MI:SS'))"""

in_stg_driver_report = """
insert into INTERN_TEAM8.stg_driver_report ( id, task_number, odometr_from, odometr_to, check_number, date_check, sum_check, image_check, date_create_driver_report)
select id, task_number, odometr_from, odometr_to, check_number, date_check, sum_check, image_check, date_create_driver_report
from INTERN_TEAM8.main_driver_report
where  date_create_driver_report > coalesce (
    (select max_update_dt
    from INTERN_TEAM8.meta
    where schema_name = 'INTERN_TEAM8' and table_name = 'META'), to_date('01.01.1800 00:00:00','DD.MM.YYYY HH24:MI:SS') )"""

in_stg_catalog_route_url = """
insert into INTERN_TEAM8.stg_catalog_route_url ( number_route, count_point_to_route, point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9, point_10, url_route, date_create_route)
select number_route, count_point_to_route, point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9, point_10, url_route, date_create_route 
from INTERN_TEAM8.main_catalog_route_url
where  date_create_route > coalesce (
    (select max_update_dt
    from INTERN_TEAM8.meta
    where schema_name = 'INTERN_TEAM8' and table_name = 'META'), to_date('01.01.1800 00:00:00','DD.MM.YYYY HH24:MI:SS') )"""

in_stg_manager_task = """
insert into INTERN_TEAM8.stg_manager_task ( task_number, date_task, phone_manager, phone_driver, number_route)
select task_number, date_task, phone_manager, phone_driver, number_route
from INTERN_TEAM8.main_manager_task
where  date_task > coalesce (
    (select max_update_dt
    from INTERN_TEAM8.meta
    where schema_name = 'INTERN_TEAM8' and table_name = 'META'), to_date('01.01.1800 00:00:00','DD.MM.YYYY HH24:MI:SS') )"""

# Сохраняем id, для дальнейшей обработки удаленных записей
in_stg_user_del = """
insert into INTERN_TEAM8.stg_user_del ( id )
select id from INTERN_TEAM8.users_user"""

in_stg_driver_step_route_del = """
insert into INTERN_TEAM8.stg_driver_step_route_del ( task_number )
select task_number from INTERN_TEAM8.main_driver_step_route"""

in_stg_driver_report_del = """
insert into INTERN_TEAM8.stg_driver_report_del ( id )
select id from INTERN_TEAM8.main_driver_report"""

in_stg_catalog_route_url_del = """
insert into INTERN_TEAM8.stg_catalog_route_url_del ( number_route )
select number_route from INTERN_TEAM8.main_catalog_route_url"""

in_stg_manager_task_del = """
insert into INTERN_TEAM8.stg_manager_task_del ( task_number )
select task_number from INTERN_TEAM8.main_manager_task"""

# 2. Выделение вставок и изменений (transform); вставка в их приемник (load)

# Добавляет изменившиеся строки. К таблице из tgt присоединяем таблицу из stg по ключу, где ключ stg-таблицы не нулевой, запись есть и она актуальная. Вставляем в tgt-слой данные из stg, в effective_from прописываем дату изменения записи. Делаем запись актуальной(31.12.9999), ставим флаг 0-запись не удалена.
in_dwh_user_hist = """
insert into INTERN_TEAM8.dwh_user_hist (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, role, effective_from, effective_to, deleted_flg ) 
select stg.id, stg.password, stg.last_login, stg.is_superuser, stg.username, stg.first_name, stg.last_name, stg.email, stg.is_staff, stg.is_active, stg.role,stg.date_joined , TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0
FROM INTERN_TEAM8.dwh_user_hist tgt
left join INTERN_TEAM8.stg_user stg
on tgt.id = stg.id 
where stg.id is not NULL 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
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
	or (stg.role <> tgt.role or ( stg.role is null and tgt.role is not null ) or ( stg.role is not null and tgt.role is null )))"""

in_dwh_driver_step_route_hist = """
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
	or (stg.point_2 <> tgt.point_2 or ( stg.point_2 is null and tgt.point_2 is not null ) or ( stg.point_2 is not null and tgt.point_2 is null ))
	or (stg.point_3 <> tgt.point_3 or ( stg.point_3 is null and tgt.point_3 is not null ) or ( stg.point_3 is not null and tgt.point_3 is null ))
	or (stg.point_4 <> tgt.point_4 or ( stg.point_4 is null and tgt.point_4 is not null ) or ( stg.point_4 is not null and tgt.point_4 is null ))
	or (stg.point_5 <> tgt.point_5 or ( stg.point_5 is null and tgt.point_5 is not null ) or ( stg.point_5 is not null and tgt.point_5 is null ))
	or (stg.point_6 <> tgt.point_6 or ( stg.point_6 is null and tgt.point_6 is not null ) or ( stg.point_6 is not null and tgt.point_6 is null ))
	or (stg.point_7 <> tgt.point_7 or ( stg.point_7 is null and tgt.point_7 is not null ) or ( stg.point_7 is not null and tgt.point_7 is null ))
	or (stg.point_8 <> tgt.point_8 or ( stg.point_8 is null and tgt.point_8 is not null ) or ( stg.point_8 is not null and tgt.point_8 is null ))
	or (stg.point_9 <> tgt.point_9 or ( stg.point_9 is null and tgt.point_9 is not null ) or ( stg.point_9 is not null and tgt.point_9 is null ))
	or (stg.point_10 <> tgt.point_10 or ( stg.point_10 is null and tgt.point_10 is not null ) or ( stg.point_10 is not null and tgt.point_10 is null ))
	or (stg.date_and_time_route_to <> tgt.date_and_time_route_to or ( stg.date_and_time_route_to is null and tgt.date_and_time_route_to is not null ) or ( stg.date_and_time_route_to is not null and tgt.date_and_time_route_to is null )))"""

in_dwh_driver_report_hist = """
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
	or (stg.image_check <> tgt.image_check or ( stg.image_check is null and tgt.image_check is not null ) or ( stg.image_check is not null and tgt.image_check is null )))"""

in_dwh_catalog_route_url_hist = """   
insert into INTERN_TEAM8.dwh_catalog_route_url_hist (number_route, count_point_to_route, url_route, effective_from, effective_to, deleted_flg ) 
select stg.number_route, stg.count_point_to_route, stg.url_route, stg.date_create_route, TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0
FROM INTERN_TEAM8.dwh_catalog_route_url_hist tgt
left join INTERN_TEAM8.stg_catalog_route_url stg
on tgt.number_route = stg.number_route 
where stg.number_route is not NULL 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
and (1=0
    or (stg.count_point_to_route <> tgt.count_point_to_route or (stg.count_point_to_route is null and tgt.count_point_to_route is not null ) or ( stg.count_point_to_route is not null and tgt.count_point_to_route is null ))
	or (stg.url_route <> tgt.url_route or ( stg.url_route is null and tgt.url_route is not null ) or ( stg.url_route is not null and tgt.url_route is null)))"""

in_dwh_catalog_route_point_hist = """
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
	or (stg.point_10 <> tgt.point_10 or ( stg.point_10 is null and tgt.point_10 is not null ) or ( stg.point_10 is not null and tgt.point_10 is null )))"""

in_dwh_manager_task_hist = """
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
	or (stg.number_route <> tgt.number_route or ( stg.number_route is null and tgt.number_route is not null ) or ( stg.number_route is not null and tgt.number_route is null )))"""

# Если в результате предыдущего инсерта записи вставились, выполняется обновление в tgt предыдущей строки с таким же id. Изменяется effective_to - ставиться дата предыдущего дня, предшествующего новой записи
# Если в результате предыдущего инсерта записи не вставились, новые записи вставляются в tgt.
mg_dwh_user_hist = """
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
    values (stg.id, stg.password, stg.last_login, stg.is_superuser, stg.username, stg.first_name, stg.last_name, stg.email, stg.is_staff, stg.is_active, stg.role, stg.date_joined, TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0)"""

mg_dwh_driver_step_route_hist = """
merge into INTERN_TEAM8.dwh_driver_step_route_hist tgt
using INTERN_TEAM8.stg_driver_step_route stg
on( stg.task_number = tgt.task_number )
when matched then 
    update set tgt.effective_to=TRUNC(stg.date_and_time_route_to )- INTERVAL '1' SECOND, deleted_flg = 0
    where effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
	and (1=0
	or (stg.date_and_time_route_from <> tgt.date_and_time_route_from or ( stg.date_and_time_route_from is null and tgt.date_and_time_route_from is not null ) or ( stg.date_and_time_route_from is not null and tgt.date_and_time_route_from is null ))
	or (stg.point_1 <> tgt.point_1 or ( stg.point_1 is null and tgt.point_1 is not null ) or ( stg.point_1 is not null and tgt.point_1 is null ))
	or (stg.point_2 <> tgt.point_2 or ( stg.point_2 is null and tgt.point_2 is not null ) or ( stg.point_2 is not null and tgt.point_2 is null ))
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
    values (stg.task_number, stg.date_and_time_route_from, stg.point_1, stg.point_2, stg.point_3, stg.point_4, stg.point_5, stg.point_6, stg.point_7, stg.point_8, stg.point_9, stg.point_10, stg.date_and_time_route_to, TRUNC(stg.date_and_time_route_to), TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0)"""

mg_dwh_driver_report_hist = """
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
    values (stg.id, stg.task_number, stg.odometr_from, stg.odometr_to, stg.check_number, stg.date_check, stg.sum_check, stg.image_check, stg.date_create_driver_report, TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0)"""

mg_dwh_catalog_route_url_hist = """    
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
    values (stg.number_route, stg.count_point_to_route, stg.url_route, stg.date_create_route, TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0)"""

mg_dwh_catalog_route_point_hist = """
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
    values (stg.number_route, stg.point_1, stg.point_2, stg.point_3, stg.point_4, stg.point_5, stg.point_6, stg.point_7, stg.point_8, stg.point_9, stg.point_10, stg.date_create_route , TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0)"""

mg_dwh_manager_task_hist = """
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
    values (stg.task_number, stg.phone_manager, stg.phone_driver, stg.number_route, stg.date_task, TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 0)"""

# 3. Обработка удалений.
# К таблице tgt присоединяется таблица из stg с id. Если в stg нет id, а в tgt такой id есть, запись активна и флага удаления нет, то в tgt вставляется(как бы дублируется) запись с этим id, но в effective_from записывается дата из методанных(еще не обновленная на сегодняшний день), запись ставится активной и ставиться флаг удаления
ind_dwh_user_hist = """
insert into INTERN_TEAM8.dwh_user_hist (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, role, effective_from, effective_to, deleted_flg)  
select tgt.id, tgt.password, tgt.last_login, tgt.is_superuser, tgt.username, tgt.first_name, tgt.last_name, tgt.email, tgt.is_staff, tgt.is_active, tgt.role, TO_DATE((SELECT DISTINCT  max(effective_from) from INTERN_TEAM8.dwh_user_hist), 'dd.mm.yyyy'), TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 1
from INTERN_TEAM8.dwh_user_hist tgt 
left join INTERN_TEAM8.stg_user_del stg
on tgt.id = stg.id
where stg.id is null 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy') 
and deleted_flg <> 1"""

ind_dwh_driver_step_route_hist = """
insert into INTERN_TEAM8.dwh_driver_step_route_hist ( task_number, date_and_time_route_from, point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9, point_10, date_and_time_route_to, effective_from, effective_to, deleted_flg) 
select tgt.task_number, tgt.date_and_time_route_from, tgt.point_1, tgt.point_2, tgt.point_3, tgt.point_4, tgt.point_5, tgt.point_6, tgt.point_7, tgt.point_8, tgt.point_9, tgt.point_10, tgt.date_and_time_route_to, TO_DATE((SELECT DISTINCT  max(effective_from) from INTERN_TEAM8.dwh_driver_step_route_hist), 'dd.mm.yyyy'), TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 1
from INTERN_TEAM8.dwh_driver_step_route_hist tgt 
left join INTERN_TEAM8.stg_driver_step_route_del stg
on tgt.task_number = stg.task_number
where stg.task_number is null 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy') 
and deleted_flg <> 1"""

ind_dwh_driver_report_hist = """
insert into INTERN_TEAM8.dwh_driver_report_hist ( id, task_number, odometr_from, odometr_to, check_number, date_check, sum_check, image_check, effective_from,  effective_to, deleted_flg)  
select tgt.id, tgt.task_number, tgt.odometr_from, tgt.odometr_to, tgt.check_number, tgt.date_check, tgt.sum_check, tgt.image_check, TO_DATE((SELECT DISTINCT  max(effective_from) from INTERN_TEAM8.dwh_driver_report_hist), 'dd.mm.yyyy'), TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 1
from INTERN_TEAM8.dwh_driver_report_hist  tgt 
left join INTERN_TEAM8.stg_driver_report_del stg
on tgt.id = stg.id
where stg.id is null 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy') 
and deleted_flg <> 1"""

ind_dwh_catalog_route_url_hist = """
insert into INTERN_TEAM8.dwh_catalog_route_url_hist ( number_route, count_point_to_route, url_route, effective_from, effective_to, deleted_flg)  
select tgt.number_route, tgt.count_point_to_route, tgt.url_route, TO_DATE((SELECT DISTINCT  max(effective_from) from INTERN_TEAM8.dwh_catalog_route_point_hist), 'dd.mm.yyyy'), TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 1
from INTERN_TEAM8.dwh_catalog_route_url_hist tgt 
left join INTERN_TEAM8.stg_catalog_route_url_del stg
on tgt.number_route = stg.number_route
where stg.number_route is null 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy') 
and deleted_flg <> 1"""

ind_dwh_catalog_route_point_hist = """
insert into INTERN_TEAM8.dwh_catalog_route_point_hist ( number_route, point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9, point_10, effective_from, effective_to, deleted_flg) 
select tgt.number_route, tgt.point_1, tgt.point_2, tgt.point_3, tgt.point_4, tgt.point_5, tgt.point_6, tgt.point_7, tgt.point_8, tgt.point_9, tgt.point_10, TO_DATE((SELECT DISTINCT  max(effective_from) from INTERN_TEAM8.dwh_catalog_route_point_hist), 'dd.mm.yyyy'), TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 1
from INTERN_TEAM8.dwh_catalog_route_point_hist tgt 
left join INTERN_TEAM8.stg_catalog_route_url_del stg
on tgt.number_route = stg.number_route
where stg.number_route is null 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy') 
and deleted_flg <> 1"""

ind_dwh_manager_task_hist = """
insert into INTERN_TEAM8.dwh_manager_task_hist ( task_number, phone_manager, phone_driver, number_route, effective_from, effective_to, deleted_flg) 
select tgt.task_number, tgt.phone_manager, tgt.phone_driver, tgt.number_route, TO_DATE((SELECT DISTINCT  max(effective_from) from INTERN_TEAM8.dwh_manager_task_hist), 'dd.mm.yyyy'), TO_DATE ('31.12.9999', 'dd.mm.yyyy'), 1
from INTERN_TEAM8.dwh_manager_task_hist tgt 
left join INTERN_TEAM8.stg_manager_task_del stg
on tgt.task_number = stg.task_number
where stg.task_number is null 
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy') 
and deleted_flg <> 1"""

# Далее обновляется предыдущая дата, где effective_to становится предыдущим днем, предшествующим удалению записи
upd_dwh_user_hist = """
update INTERN_TEAM8.dwh_user_hist
set effective_to = (select distinct effective_from  - INTERVAL '1' SECOND from INTERN_TEAM8.dwh_user_hist where deleted_flg = 1 and effective_from = TO_DATE((SELECT DISTINCT  max(effective_from) from INTERN_TEAM8.dwh_user_hist), 'dd.mm.yyyy'))
where id in(
    select tgt.id
    from INTERN_TEAM8.dwh_user_hist tgt 
    left join INTERN_TEAM8.stg_user_del stg
    on tgt.id = stg.id
    where stg.id is null )
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
and deleted_flg = 0"""

upd_dwh_driver_step_route_hist = """
update INTERN_TEAM8.dwh_driver_step_route_hist 
set effective_to = (select distinct effective_from  - INTERVAL '1' SECOND from INTERN_TEAM8.dwh_driver_step_route_hist where deleted_flg = 1 and effective_from = TO_DATE((SELECT DISTINCT  max(effective_from) from INTERN_TEAM8.dwh_driver_step_route_hist), 'dd.mm.yyyy'))
where task_number in(
    select tgt.task_number
    from INTERN_TEAM8.dwh_driver_step_route_hist tgt 
    left join INTERN_TEAM8.stg_driver_step_route_del stg
    on tgt.task_number = stg.task_number
    where stg.task_number is null )
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
and deleted_flg = 0"""

upd_dwh_driver_report_hist = """
update INTERN_TEAM8.dwh_driver_report_hist
set effective_to = (select distinct effective_from  - INTERVAL '1' SECOND from INTERN_TEAM8.dwh_driver_report_hist where deleted_flg = 1 and effective_from = TO_DATE((SELECT DISTINCT  max(effective_from) from INTERN_TEAM8.dwh_driver_report_hist), 'dd.mm.yyyy'))
where id in(
    select tgt.id
    from INTERN_TEAM8.dwh_driver_report_hist tgt 
    left join INTERN_TEAM8.stg_driver_report_del stg
    on tgt.id = stg.id
    where stg.id is null )
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
and deleted_flg = 0"""

upd_dwh_catalog_route_url_hist = """
update INTERN_TEAM8.dwh_catalog_route_url_hist
set effective_to = (select distinct effective_from  - INTERVAL '1' SECOND from INTERN_TEAM8.dwh_catalog_route_url_hist where deleted_flg = 1 and effective_from = TO_DATE((SELECT DISTINCT  max(effective_from) from INTERN_TEAM8.dwh_catalog_route_url_hist), 'dd.mm.yyyy'))
where number_route in(
    select tgt.number_route
    from INTERN_TEAM8.dwh_catalog_route_url_hist tgt 
    left join INTERN_TEAM8.stg_catalog_route_url_del stg
    on tgt.number_route = stg.number_route
    where stg.number_route is null )
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
and deleted_flg = 0"""

upd_dwh_catalog_route_point_hist = """ 
update INTERN_TEAM8.dwh_catalog_route_point_hist 
set effective_to = (select distinct effective_from  - INTERVAL '1' SECOND from INTERN_TEAM8.dwh_catalog_route_point_hist where deleted_flg = 1 and effective_from = TO_DATE((SELECT DISTINCT  max(effective_from) from INTERN_TEAM8.dwh_catalog_route_point_hist), 'dd.mm.yyyy'))
where number_route in(
    select tgt.number_route
    from INTERN_TEAM8.dwh_catalog_route_point_hist tgt 
    left join INTERN_TEAM8.stg_catalog_route_url_del stg
    on tgt.number_route = stg.number_route
    where stg.number_route is null )
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
and deleted_flg = 0"""

upd_dwh_manager_task_hist = """ 
update INTERN_TEAM8.dwh_manager_task_hist
set effective_to = (select distinct effective_from  - INTERVAL '1' SECOND from INTERN_TEAM8.dwh_manager_task_hist where deleted_flg = 1 and effective_from = TO_DATE((SELECT DISTINCT  max(effective_from) from INTERN_TEAM8.dwh_manager_task_hist), 'dd.mm.yyyy'))
where task_number in(
    select tgt.task_number
    from INTERN_TEAM8.dwh_manager_task_hist tgt 
    left join INTERN_TEAM8.stg_manager_task_del stg
    on tgt.task_number = stg.task_number
    where stg.task_number is null )
and effective_to = TO_DATE ('31.12.9999', 'dd.mm.yyyy')
and deleted_flg = 0"""

# Обновление метаданных.
# При первой записи идет запись очень маленькой даты(01.01.1800), далее дата будет обвовляться в зависимости от даты приходящей записи от источника

mg_meta = """
merge into INTERN_TEAM8.meta m1
USING ( select 'INTERN_TEAM8' schema_name, 'META' table_name, ( select max( date_task ) from INTERN_TEAM8.MAIN_MANAGER_TASK ) max_update_dt from dual ) m2
on (m1.schema_name = m2.schema_name and m1.table_name = m2.table_name)
when matched then 
	update set m1.max_update_dt = m2.max_update_dt
    where m2.max_update_dt is not null
WHEN NOT matched THEN 
	INSERT (schema_name, table_name, max_update_dt)
	VALUES ( 'INTERN_TEAM8','META', ( select max( date_task ) from INTERN_TEAM8.MAIN_MANAGER_TASK ))
"""