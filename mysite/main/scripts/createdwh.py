cr_meta = """create table INTERN_TEAM8.meta (
            schema_name varchar(30),
            table_name varchar(30),
            max_update_dt date
        )"""

cr_stg_user = """create table INTERN_TEAM8.stg_user as select * from INTERN_TEAM8.users_user  where 1=0"""

cr_stg_user_del = """create table INTERN_TEAM8.stg_user_del as select id from INTERN_TEAM8.users_user where 1=0"""

cr_dwh_user_hist = """
create table INTERN_TEAM8.dwh_user_hist (
	id INTEGER NOT NULL,
	password NVARCHAR2(128),
	last_login TIMESTAMP,
	is_superuser NUMBER(1,0),
	username NVARCHAR2(11),
	first_name NVARCHAR2(150),
	last_name NVARCHAR2(150),
	email NVARCHAR2(254),
	is_staff NUMBER(1,0),
	is_active NUMBER(1,0),
	role NVARCHAR2(8),
	effective_from DATE,
	effective_to DATE,
    deleted_flg CHAR(1)
)"""

cr_stg_driver_step_route = """create table INTERN_TEAM8.stg_driver_step_route as select * from INTERN_TEAM8.main_driver_step_route  where 1=0"""

cr_stg_driver_step_route_del = """create table INTERN_TEAM8.stg_driver_step_route_del as select task_number from INTERN_TEAM8.main_driver_step_route where 1=0"""

cr_dwh_driver_step_route_hist = """
create table INTERN_TEAM8.dwh_driver_step_route_hist (
	task_number INTEGER NOT NULL,
	date_and_time_route_from TIMESTAMP,
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
	date_and_time_route_to TIMESTAMP,
	effective_from DATE,
	effective_to DATE,
    deleted_flg CHAR(1)
)"""

cr_stg_driver_report = """create table INTERN_TEAM8.stg_driver_report as select * from INTERN_TEAM8.main_driver_report  where 1=0"""

cr_stg_driver_report_del = """create table INTERN_TEAM8.stg_driver_report_del as select ID from INTERN_TEAM8.main_driver_report where 1=0"""

cr_dwh_driver_report_hist = """
create table INTERN_TEAM8.dwh_driver_report_hist (
	id INTEGER NOT NULL, 
	task_number INTEGER NOT NULL , 
	odometr_from INTEGER, 
	odometr_to INTEGER, 
	check_number INTEGER, 
	date_check DATE, 
	sum_check FLOAT(126), 
	image_check NVARCHAR2(500),
	effective_from DATE,
	effective_to DATE,
    deleted_flg CHAR(1)
)"""

cr_stg_catalog_route_url = """create table INTERN_TEAM8.stg_catalog_route_url as select * from INTERN_TEAM8.main_catalog_route_url where 1=0"""

cr_stg_catalog_route_url_del = """create table INTERN_TEAM8.stg_catalog_route_url_del as select number_route from INTERN_TEAM8.main_catalog_route_url where 1=0"""

cr_dwh_catalog_route_url_hist = """create table INTERN_TEAM8.dwh_catalog_route_url_hist (
	number_route varchar2(7) NOT NULL,
	count_point_to_route integer,
	url_route varchar2(500),
	effective_from date,
	effective_to date,
    deleted_flg char(1)
)"""

cr_dwh_catalog_route_point_hist = """create table INTERN_TEAM8.dwh_catalog_route_point_hist (
	number_route varchar(7) NOT NULL,
	point_1 NVARCHAR2(20),
	point_2 NVARCHAR2(20),
	point_3 NVARCHAR2(20),
	point_4 NVARCHAR2(20),
	point_5 NVARCHAR2(20),
	point_6 NVARCHAR2(20),
	point_7 NVARCHAR2(20),
	point_8 NVARCHAR2(20),
	point_9 NVARCHAR2(20),
	point_10 NVARCHAR2(20),
	effective_from date,
	effective_to date,
    deleted_flg char(1)
)"""

cr_stg_manager_task = """create table INTERN_TEAM8.stg_manager_task as select * from INTERN_TEAM8.main_manager_task  where 1=0"""

cr_stg_manager_task_del = """create table INTERN_TEAM8.stg_manager_task_del as select task_number from INTERN_TEAM8.main_manager_task where 1=0"""

cr_dwh_manager_task_hist = """
create table INTERN_TEAM8.dwh_manager_task_hist (
	task_number INTEGER NOT NULL,
	phone_manager NVARCHAR2(11),
	phone_driver NVARCHAR2(11),
	number_route NVARCHAR2(7),
	effective_from DATE,
	effective_to DATE,
    deleted_flg CHAR(1)
)"""

cr_view_select_url_route = """
CREATE VIEW select_url_route AS
select number_route, url_route from INTERN_TEAM8.main_catalog_route_url
"""

cr_view_select_catalog_driver = """
CREATE VIEW select_catalog_driver as 
select first_name, 
       last_name, 
       username, 
       email 
from INTERN_TEAM8.users_user
where role='водитель'
"""

cr_view_select_report = """
CREATE VIEW select_report as
select '№'|| t1.task_number || ' от ' || to_char(t1.date_task, 'dd.mm.yyyy') as number_date__task,  
	   t5.first_name || ' ' ||  t5.last_name as FI, 
	   t5.username,
	   t2.date_and_time_route_to - t2.date_and_time_route_from as time_route,
	   t3.odometr_to - t3.odometr_from as distance_km,
	   30 * (t3.odometr_to - t3.odometr_from)/100 AS kol_vo_bens,
	   '№'|| t3.check_number || ' от ' || to_char(t3.date_check, 'dd.mm.yyyy') as number_date_and_time_check,
	   t3.sum_check, 
	   t3.image_check,
	   case 
	   	when (t2.point_1 + t2.point_2 + t2.point_3 + t2.point_4 + t2.point_5 + t2.point_6 + t2.point_7 + t2.point_8 + t2.point_9 + t2.point_10) = count_point_to_route then 'Пройден'
	   	when (t2.point_1 + t2.point_2 + t2.point_3 + t2.point_4 + t2.point_5 + t2.point_6 + t2.point_7 + t2.point_8 + t2.point_9 + t2.point_10) > count_point_to_route then 'Пройдено больше точек'
	   else 'Пройдено меньше точек'
	   end result,
	   t1.number_route,
	   t4.url_route
from INTERN_TEAM8.main_manager_task t1
left join INTERN_TEAM8.main_driver_step_route t2
on t1.task_number = t2.task_number
left join INTERN_TEAM8.main_driver_report t3
on t2.task_number = t3.task_number 
left join INTERN_TEAM8.main_catalog_route_url t4
on t1.number_route = t4.number_route 
left join INTERN_TEAM8.users_user t5
on t1.phone_driver = t5.username
"""