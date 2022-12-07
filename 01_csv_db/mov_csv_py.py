import os
import pandas as pd
import numpy as np
import psycopg2
from psycopg2 import Error
import re
from dotenv import load_dotenv




#Environment Variables

PATH_ENV= '/Users/martinjurado/Documents/prj/data_challenge/01_csv_db/.env_db'
load_dotenv(PATH_ENV)
folder_path = "/Users/martinjurado/Documents/prj/data_challenge/raw_data/"

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
data_status(folder_path)