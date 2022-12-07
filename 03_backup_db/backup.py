import os
import copy
import json
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
from dotenv import load_dotenv
import requests


import psycopg2
from psycopg2 import Error
import sys


PATH_ENV= '.env_db'
load_dotenv(PATH_ENV)



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




def jobs_back_up(n=True):
    
    if n == True:
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
            with open('hired_employees_jobs.avro', 'wb') as f:
                writer = DataFileWriter(f, DatumWriter(), schema_jobs_parsed)
                for r in rb:
                    id = int(r[0])
                    job = str(r[1])        
                    writer.append({'id': id, 'job': job})    
                writer.close()
        except:

            print("Error to write the file")

    else:
        try:
            with open('hired_employees_jobs.avro', 'rb') as f:
                reader = DataFileReader(f, DatumReader())
                metadata = copy.deepcopy(reader.meta)
                schema_from_file = json.loads(metadata['avro.schema'])
                data_jobs = [job for job in reader]
                reader.close()
                url="http://localhost:8887/api/massive/jobs"
                paidload = {"data":data_jobs}
                print(data_jobs)
                try:
                    response = requests.post(url, json = paidload)
                except:
                    print("Error to reach API")
        except:

            print("Error to read the file")
            


jobs_back_up(False)