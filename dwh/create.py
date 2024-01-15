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
)"""


cr_stg_driver_step_route = """create table INTERN_TEAM8.stg_driver_step_route as select * from INTERN_TEAM8.main_driver_step_route  where 1=0"""

cr_stg_driver_step_route_del = """create table INTERN_TEAM8.stg_driver_step_route_del as select task_number from INTERN_TEAM8.main_driver_step_route where 1=0"""

cr_dwh_driver_step_route_hist = """
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
)"""

cr_stg_driver_report = """create table INTERN_TEAM8.stg_driver_report as select * from INTERN_TEAM8.main_driver_report  where 1=0"""

cr_stg_driver_report_del = """create table INTERN_TEAM8.stg_driver_report_del as select ID from INTERN_TEAM8.main_driver_report where 1=0"""


cr_dwh_driver_report_hist = """
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
)"""


cr_stg_catalog_route_url = """create table INTERN_TEAM8.stg_catalog_route_url as select * from INTERN_TEAM8.main_catalog_route_url where 1=0"""

cr_stg_catalog_route_url_del = """create table INTERN_TEAM8.stg_catalog_route_url_del as select number_route from INTERN_TEAM8.main_catalog_route_url where 1=0"""

cr_dwh_catalog_route_url_hist = 
"""create table INTERN_TEAM8.dwh_catalog_route_url_hist (
	number_route varchar2(7) NOT NULL,
	count_point_to_route integer NOT NULL,
	url_route varchar2(500) NOT null,
	effective_from date,
	effective_to date,
    deleted_flg char(1)
)"""

cr_dwh_catalog_route_point_hist =
"""create table INTERN_TEAM8.dwh_catalog_route_point_hist (
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
)"""


cr_stg_manager_task = """create table INTERN_TEAM8.stg_manager_task as select * from INTERN_TEAM8.main_manager_task  where 1=0"""

cr_stg_manager_task_del = """create table INTERN_TEAM8.stg_manager_task_del as select task_number from INTERN_TEAM8.main_manager_task where 1=0"""

cr_dwh_manager_task_hist = """
create table INTERN_TEAM8.dwh_manager_task_hist (
	task_number INTEGER NOT NULL,
	phone_manager NVARCHAR2(11) NOT NULL,
	phone_driver NVARCHAR2(11) NOT NULL,
	number_route NVARCHAR2(7) NOT NULL,
	effective_from DATE,
	effective_to DATE,
    deleted_flg CHAR(1)
)"""
