-- Data base creation
create database employee_data_db;
-- Schema creation
create schema hired_employees;
-- Tables Creation
--independent tables (Catalogs)
-- Departments
create table hired_employees.departments
(
	id serial
		constraint departments_pk
			primary key,
	departments text not null
);
-- Jobs
create table hired_employees.jobs
(
	id serial
        constraint jobs_pk
                primary key,
	job text not null
);

-- Table Hired employes
create table hired_employees.hired_employees
(
    id            serial
        constraint hired_employees_pk
            primary key,
    employee_name text,
    hired_date    text,
    department_id int
        constraint hired_employees_departments_id_fk
            references hired_employees.departments
            on delete cascade,
    job_id        int
        constraint hired_employees_jobs_id_fk
            references hired_employees.jobs
            on delete cascade
);


-- For the ingest is important to create a status table

-- Schema creation
create schema ingest_status;

-- Table  Creation

create table ingest_status.ingest_status
(
    id        serial
        constraint ingest_status_pk
            primary key,
    file_name text,
    file_size bigint,
    last_id   int
);
