from flask import Flask
from flask import request, jsonify, json
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine

PATH_ENV= '/Users/martinjurado/Documents/prj/data_challenge/02_API/.env_db'
#PATH_ENV='/home/prj/.env_db'
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
            record = "Data iserted"
        else:
            record = cursor.fetchall()        
        connection.commit()
        cursor.close()
        connection.close()
        return record
        

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)


app = Flask(__name__)

@app.route("/")
def home():
    return "<p>Server is alive !!!</p>"




@app.route("/api/departments", methods=["GET", "POST","PUT","DELETE"])
def data_departments():
    
    if request.method == 'POST':
        data = json.loads(request.data)
        try:
        
            data = data['data']
            
            for d in data:
                dep_name= d["departments"]
                find_id_query=f"SELECT id from hired_employees.departments where departments = '{dep_name}'"
                rb = db_connection(find_id_query)
                if len(rb)==0:
                    query_dep_insert=f"""INSERT INTO hired_employees.departments (departments) VALUES ('{dep_name}')"""
                    db_connection(query_dep_insert,True)
                else:
                    print("The data is saved")
        except:

            return {"Error":"Data  does not have the required format"}
        
        return {"Task":"Inserted"}

    elif request.method == 'PUT':
        data = json.loads(request.data)
        
        try:
            data = data['data']
            for d in data:
                dep_id = int(d["id"])
                dep_name = d["departments"]
                up_query=f"UPDATE hired_employees.departments SET departments = '{dep_name}' WHERE id = {dep_id}"
                update_status = db_connection(up_query,True)
        except:
            return {"Error":"Data  does not have the required format"}


        return {"Task":"Updted"}

    elif request.method == 'DELETE':
        data = json.loads(request.data)
        try:
            data = data['data']
            for d in data:
                dep_id = int(d["id"])
                up_query=f"DELETE FROM hired_employees.departments WHERE id = {dep_id}"
                update_status = db_connection(up_query,True)
        except:
            return {"Error":"Data  does not have the required format"}

        return {"Task":"Deleted"}

    elif request.method == 'GET':
       
        
        up_query=f"SELECT * FROM hired_employees.departments"
        data = db_connection(up_query)


        return data

    else:
        return {"Task":"No"}

@app.route("/api/jobs", methods=["GET", "POST","PUT","DELETE"])
def data_jobs():
    
    if request.method == 'POST':
        
        data = json.loads(request.data)
        try:
            data = data['data']
            for d in data:
                job_name= d["job"]
                find_id_query=f"SELECT id from hired_employees.jobs where job = '{job_name}'"
                rb = db_connection(find_id_query)
                if len(rb)== 0:
                    query_dep_insert=f"""INSERT INTO hired_employees.jobs (job) VALUES ('{job_name}')"""
                    db_connection(query_dep_insert,True)
                else:
                    print("The data is saved")
        except:
            return {"Error":"Data  does not have the required format"}
        
        return {"Task":"Inserted"}

    elif request.method == 'PUT':
        data = json.loads(request.data)
        try:
            data = data["data"]
            for d in data:
                job_id = int(d["id"])
                job_name = d["job"]
                up_query=f"UPDATE hired_employees.jobs SET job = '{job_name}' WHERE id = {job_id}"
                update_status = db_connection(up_query,True)
        except:
            return {"Error":"Data  does not have the required format"}

        return {"Task":"Updted"}

    elif request.method == 'DELETE':
        data = json.loads(request.data)
        try:
            data = data["data"]        
            for d in data:
                dep_id = int(d["id"])
                up_query=f"DELETE FROM hired_employees.jobs WHERE id = {dep_id}"
                update_status = db_connection(up_query,True)
        except:
            return {"Error":"Data  does not have the required format"}

        return {"Task":"Deleted"}

    elif request.method == 'GET':
       
        
        up_query=f"SELECT * FROM hired_employees.jobs"
        data = db_connection(up_query)


        return data




    else:
        return {"Task":"No"}

@app.route("/api/employees", methods=["GET", "POST","PUT","DELETE"])
def data_employees():
    
    if request.method == 'POST':
        data = json.loads(request.data)
        try:
            data = data['data']
            for d in data:
                empl_named= d["employee_name"]
                hir_date=d["hired_date"]
                dep_id=int(d["department_id"])
                job_id=int(d["job_id"])

                find_id_query=f"SELECT id from hired_employees.hired_employees where employee_name = '{empl_named}'"
                rb = db_connection(find_id_query)
                if len(rb)== 0:
                    query_employee_insert=f"INSERT INTO hired_employees.hired_employees (employee_name,hired_date,department_id,job_id) VALUES ('{empl_named}','{hir_date}',{dep_id},{job_id})"
                    db_connection(query_employee_insert,True)
                else:
                    print("The data is saved")
        except:
            return {"Error":"Data  does not have the required format"}

        return {"Task":"Inserted"}

    elif request.method == 'PUT':
        data = json.loads(request.data)
        try:
            data = data['data']
            for d in data:
                empl_id =int(d["id"])
                empl_named= d["employee_name"]
                hir_date=d["hired_date"]
                dep_id=int(d["department_id"])
                job_id=int(d["job_id"])
                up_query=f"UPDATE hired_employees.hired_employees SET employee_name = '{empl_named}', hired_date='{hir_date}',department_id ={dep_id}, job_id ={job_id} WHERE id = {empl_id}"
                update_status = db_connection(up_query,True)
        except:
            return {"Error":"Data  does not have the required format"}
        return {"Task":"Updted"}

    elif request.method == 'DELETE':
        data = json.loads(request.data)
        try:
            data = data['data']
            for d in data:
                empl_id=int(d['id'])
                up_query=f"DELETE FROM hired_employees.hired_employees WHERE id = {empl_id}"
                update_status = db_connection(up_query,True)
        except:
            return {"Error":"Data  does not have the required format"}

        return {"Task":"Deleted"}
    elif request.method == 'GET':
       
        
        up_query=f"SELECT * FROM hired_employees.hired_employees"
        data = db_connection(up_query)


        return data


    else:
        return {"Task":"No"}






if __name__ == '__main__':
    app.run(debug = True ,host = '0.0.0.0',port=8887)