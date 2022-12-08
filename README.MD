# Data Challenge 🚀🚀

This documentation regarding the Data Challenge Data migration POC that covers 2 challenges.

The challenge info is in the following link:

[file.pdf](./challenge_information/Ejercicio Data Arch.pdf)

## Check prerequisites 📋

Docker is used to run all the tasks in this challenge.

To run the environments it is necessary to have docker installed and a computer with a capacity greater than (**8 GB**) in memory.

For this we use three environments created to cover parts of the challenge in the folder (**./environments**)

The project structure has 8 folders, 4 for the challenges and 4 for supporting them.

# Challenge No. 1

### Move historic data from files in CSV format to the new database.
For this challenge it is necessary to migrate csv files to a relational database, these files are located in the (**./raw_data**) folder.
To address the problem it was decided to use the following technologies:
- Python (Data processing).
- Airflow (Task automation)
- Postgres (Storage and structuring of information)

It is necessary to run the following lines to create the environments.

In the project folder:

Airflow creation

```console
user@machine data_challenge % cd environments/airflow_enviroment/

user@machine data_challenge % mkdir dags logs plugins

user@machine data_challenge % docker compose up airflow-init

user@machine data_challenge % docker-compose up

```

Postgrest creation

```console
user@machine data_challenge % docker run --name postgresql -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=passw0rd -p 5433:5432 -v /Users/martinjurado/Documents/prj/data_challenge/environments/volume/data_db:/var/lib/postgresql/data -d postgres

```

To start with the requirements, the following structure was created in the database.

```sql
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


```
Data base schema employees

![Schema](data_challenge/database_schemas/hired_employees.png)



Airflow runs the following Dag:


```python
from datetime import datetime, timedelta, date
from airflow import DAG
from airflow.operators.python import PythonOperator
#Code Info
import os
import pandas as pd
import numpy as np
import psycopg2
from psycopg2 import Error
import re
from dotenv import load_dotenv

#Environment Variables
PATH_ENV= '/opt/airflow/env/.env_db'
folder_path = "/opt/airflow/code_data/"

load_dotenv(PATH_ENV)

############ Data migration code #########
##########################################

#Database Connection method
def db_connection(query,insert = False):
    try:
        connection = psycopg2.connect(user=os.getenv('user'),
                                    password=os.getenv('password'),
                                    host=os.getenv('host'),
                                    port=os.getenv('port'),
                                    database=os.getenv('database'))

        cursor = connection.cursor()
    
        cursor.execute(query)
        if insert == True:
            record = "Inserted data"
        else:
            record = cursor.fetchall()        
        connection.commit()
        cursor.close()
        connection.close()
        return record
        

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)  


#Files into the folder
def list_dir(folder_path, traversed = [], results = []): 
    dirs = os.listdir(folder_path)
    if dirs:
        for f in dirs:
            new_dir = folder_path + f + '/'
            if os.path.isdir(new_dir) and new_dir not in traversed:
                traversed.append(new_dir)
                list_dir(new_dir, traversed, results)
            else:
                results.append([new_dir[:-1], os.stat(new_dir[:-1])])  
    return results


#Data Update
def new_data_insert(file_name):
    reg_dep = bool(re.search('depar', file_name, re.IGNORECASE))
    reg_job = bool(re.search('job', file_name, re.IGNORECASE))
    reg_emp = bool(re.search('emplo', file_name, re.IGNORECASE))
    print(reg_dep,reg_emp,reg_job)
    if reg_dep == True:
        query_dep ="select id from hired_employees.departments order by id desc limit 1"
        rb =db_connection(query_dep)
        df = pd.read_csv(file_name, header=None)
            #Checking nan values and replace them by null
        df = df.replace(np.nan, 'null', regex=True)
        #Inserting only new data base id condition
        if len(rb)>0:
            print("Applying conditions")
            db_last_id = rb[0][0]
            csv_last_id = df[df.columns[0]].iloc[-1]
            if csv_last_id > db_last_id:
                df = df[(int(db_last_id)):]
                for index, row in df.iterrows():
                    dep_name=row[1] 
                    query_dep_insert=f"""INSERT INTO hired_employees.departments (departments) VALUES ('{dep_name}')"""
                    db_connection(query_dep_insert,True)
            else:
                print("Error in the file")

        else:
            
            for index, row in df.iterrows():
                dep_name=row[1] 
                query_dep_insert=f"""INSERT INTO hired_employees.departments (departments) VALUES ('{dep_name}')"""
                db_connection(query_dep_insert,True)
        
    elif reg_job == True:
        query_job ="select id from hired_employees.jobs order by id desc limit 1"
        rb =db_connection(query_job)
        df = pd.read_csv(file_name, header=None)
            #Checking nan values and replace them by null
        df = df.replace(np.nan, 'null', regex=True)
        #Inserting only new data base id condition
        if len(rb)>0:
            print("Applying conditions")
            db_last_id = rb[0][0]
            csv_last_id = df[df.columns[0]].iloc[-1]
            if csv_last_id > db_last_id:
                df = df[(int(db_last_id)):]
                for index, row in df.iterrows():
                    job_name=row[1] 
                    query_job_insert=f"""INSERT INTO hired_employees.jobs (job) VALUES ('{job_name}')"""
                    db_connection(query_job_insert,True)
            else:
                print("Error in the file")
        else:
            
            for index, row in df.iterrows():
                job_name=row[1] 
                query_job_insert=f"""INSERT INTO hired_employees.jobs (job) VALUES ('{job_name}')"""
                db_connection(query_job_insert,True)
        
    elif reg_emp == True:
        query_emp ="select id from hired_employees.hired_employees order by id desc limit 1"
        rb =db_connection(query_emp)
        df = pd.read_csv(file_name, header=None)
            #Checking nan values and replace them by null
        df = df.replace(np.nan, 'null', regex=True)
        #Inserting only new data base id condition
        if len(rb)>0:
            print("Applying conditions")
            db_last_id = rb[0][0]
            csv_last_id = df[df.columns[0]].iloc[-1]
            if csv_last_id > db_last_id:
                df = df[(int(db_last_id)):]
                for index, row in df.iterrows():
                    empl_name=row[1]
                    empl_named = empl_name.replace("'", "''" )
                    hir_date=row[2]
                    dep_id=row[3]
                    job_id=row[4]
                    query_job_insert=f"INSERT INTO hired_employees.hired_employees (employee_name,hired_date,department_id,job_id) VALUES ('{empl_named}','{hir_date}',{dep_id},{job_id})"
                    db_connection(query_job_insert,True)
            else:
                print("error in the file")
            
        else:
            
            for index, row in df.iterrows():
                empl_name=row[1]
                empl_named = empl_name.replace("'", "''" )
                hir_date=row[2]
                dep_id=row[3]
                job_id=row[4]
                query_job_insert=f"INSERT INTO hired_employees.hired_employees (employee_name,hired_date,department_id,job_id) VALUES ('{empl_named}','{hir_date}',{dep_id},{job_id})"
                db_connection(query_job_insert,True)
    
    else:
        print("Unclassified file")

#Data Status
def data_status(path):
    for file_name, stat in list_dir(path):
        df = pd.read_csv(file_name)
        last_id = df[df.columns[0]].iloc[-1]
        file_size= stat.st_size
 
        query_file =f"select * from ingest_status.ingest_status where file_name = '{file_name}' limit 1"
        file_name_exists = db_connection(query_file)
        print(file_name_exists, len(file_name_exists))

        if len(file_name_exists) > 0:
            print("Applying conditions")
            if file_size != file_name_exists[0][2]:
                print("The file resized")
                new_data_insert(file_name)
                find_id_query=f"SELECT id from ingest_status.ingest_status where file_name = '{file_name}'"
                id_changed = db_connection(find_id_query)[0][0]
                up_query=f"UPDATE ingest_status.ingest_status SET file_size = {file_size},last_id= {last_id} WHERE id = {id_changed}"
                update_status = db_connection(up_query,True)

            else:
                print("There were no changes")    
                

        else:
            new_data_insert(file_name)
            insert_data = f"INSERT INTO ingest_status.ingest_status (file_name, file_size, last_id) VALUES ('{file_name}',{file_size},{last_id})"
            db_connection(insert_data,True)
            print("inserto todo")

      
#Main function


####### Dag Configuration ################
##########################################
default_args = {

    'owner':'Martin_Jurado',
    'retries':5,
    'retry_delay':timedelta(minutes=2)

}


with DAG(

    dag_id='CSV_2_DB',
    default_args = default_args,
    description = 'Archive DataBase Updating',
    start_date= datetime(2022,11,5,9),
    schedule_interval = "@hourly",
    catchup=False


) as dag:


    t1 = PythonOperator(

        task_id='First_task_update',
        python_callable=data_status,
        op_kwargs={'path':folder_path},
    )
    
    

    t1
```

![Airflow](data_challenge/resources/airflow.png)














