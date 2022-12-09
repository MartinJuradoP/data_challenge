from datetime import datetime, timedelta, date
from airflow import DAG
from airflow.operators.python import PythonOperator
#Postgres
import os
import pandas as pd
import numpy as np
import psycopg2
from psycopg2 import Error
import re
from dotenv import load_dotenv
#Avro libraries
import copy
import json
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
from dotenv import load_dotenv
import requests
import sys


#Environment Variables
PATH_ENV= '/opt/airflow/env/.env_db'
folder_path = "/opt/airflow/backup/hired_employees_jobs.avro"
folder_path_copy = "/opt/airflow/backup/hired_employees_jobs_copy.avro"

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

def create_back_up():
    schema_jobs = {
        'name': 'avro.hired_employees.jobs',
        'type': 'record',
        'fields': [
            {'name': 'id', 'type': 'int'},
            {'name': 'job', 'type': 'string'}
        ]
    }


    schema_jobs_parsed = avro.schema.parse(json.dumps(schema_jobs))
    query_employees= 'select * from hired_employees.jobs'
    rb =db_connection(query_employees)
    try:
        
        isFile_copy = os.path.isfile(folder_path_copy)
        if isFile_copy == True:
            r=os.remove(folder_path_copy)
            with open(folder_path_copy, 'wb') as f:
                writer = DataFileWriter(f, DatumWriter(), schema_jobs_parsed)
                for r in rb:
                    id = int(r[0])
                    job = str(r[1])        
                    writer.append({'id': id, 'job': job})    
                writer.close()
            isFile = os.path.isfile(folder_path)
            if isFile == True:
                os.remove(folder_path)
                os.system('cp '+folder_path_copy+' '+folder_path)
            else:
                os.system('cp '+folder_path_copy+' '+folder_path)

        else:

            with open(folder_path_copy, 'wb') as f:
                writer = DataFileWriter(f, DatumWriter(), schema_jobs_parsed)
                for r in rb:
                    id = int(r[0])
                    job = str(r[1])        
                    writer.append({'id': id, 'job': job})    
                writer.close()
            isFile = os.path.isfile(folder_path)
            if isFile == True:
                os.remove(folder_path)
                os.system('cp '+folder_path_copy+' '+folder_path)
            else:
                os.system('cp '+folder_path_copy+' '+folder_path)

    except:

        print("Error to write the file")

def insert_back_up():
    try:
        with open(folder_path, 'rb') as f:
            reader = DataFileReader(f, DatumReader())
            metadata = copy.deepcopy(reader.meta)
            schema_from_file = json.loads(metadata['avro.schema'])
            data_jobs = [job for job in reader]
            reader.close()
            url="http://host.docker.internal:8887/api/jobs"
            paidload = {"data":data_jobs}
            print(data_jobs)
            try:
                response = requests.post(url, json = paidload)
            except:
                print("Error to reach API")
    except:

        print("Error to read the file")





      
def jobs_back_up():   
    

    

    isFile = os.path.isfile(folder_path)
    

    #query_back_up ="select * from backup_status.backup_status order by id desc limit 1"
    query_jobs="select * from hired_employees.jobs order by id desc limit 1"
    rb =db_connection(query_jobs)
    if len(rb) > 0:
        print("There is information in the database")
        create_back_up()
        
    else:
        print("There is not information in the database")
        if isFile == True:
            insert_back_up()
            query_rows = "select id, (select count(*) as number_rows from hired_employees.jobs) as number_rows from hired_employees.jobs order by id desc limit 1"
            rows = db_connection(query_rows)
            for dt in rows:
                table_name = "hired_employees.jobs"
                number_rows = dt[0]
                last_id = dt[1]

                insert_data = f"INSERT INTO backup_status.backup_status (table_name, number_rows, last_id) VALUES ('{table_name}',{number_rows},{last_id})"
                db_connection(insert_data,True)  

        else:
            print("Sorry we do not have back up")
        

####### Dag Configuration ################
##########################################
default_args = {

    'owner':'Martin_Jurado',
    'retries':5,
    'retry_delay':timedelta(minutes=2)

}


with DAG(

    dag_id='back_in_avro',
    default_args = default_args,
    description = 'Creates a back-up of the data bases of postgres',
    start_date= datetime(2022,11,5,9),
    schedule_interval = "@hourly",
    catchup=False


) as dag:


    t1 = PythonOperator(

        task_id='First_task_backup',
        python_callable=jobs_back_up,
        op_kwargs={'path':folder_path},
    )
    
    

    t1