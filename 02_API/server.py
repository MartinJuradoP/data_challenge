from flask import Flask
from flask import request, jsonify, json
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os

PATH_ENV= '/Users/martinjurado/Documents/prj/data_challenge/01_csv_db/.env_db'
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
            record = "Datos Insertados"
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

"""Post body format to insert new data {
"dep":"New Dep"}"""


@app.route("/api/deparments", methods=["GET", "POST","PUT","DELETE"])
def data_deparments():
    
    if request.method == 'POST':
        data = json.loads(request.data)
        dep_name = data["dep"]
        print(dep_name)
        find_id_query=f"SELECT id from hired_employees.departments where departments = '{dep_name}'"
        rb = db_connection(find_id_query)
        if len(rb)==0:
            query_dep_insert=f"""INSERT INTO hired_employees.departments (departments) VALUES ('{dep_name}')"""
            db_connection(query_dep_insert,True)
        else:
            print("The data is saved")
        
        return {"Task":"Inserted"}

    elif request.method == 'PUT':
        data = json.loads(request.data)
        dep_id = int(data["id"])
        dep_name = data["dep"]
        up_query=f"UPDATE hired_employees.departments SET departments = '{dep_name}' WHERE id = {dep_id}"
        update_status = db_connection(up_query,True)
        return {"Task":"Updted"}

    elif request.method == 'DELETE':
        data = json.loads(request.data)
        dep_id = int(data["id"])
        up_query=f"DELETE FROM hired_employees.departments WHERE id = {dep_id}"
        update_status = db_connection(up_query,True)


        return {"Task":"Deleted"}

    else:
        return {"Task":"No"}

@app.route("/api/jobs", methods=["GET", "POST","PUT","DELETE"])
def data_jobs():
    
    if request.method == 'POST':
        data = json.loads(request.data)
        job_name = data["job"]
        
        find_id_query=f"SELECT id from hired_employees.jobs where job = '{job_name}'"
        rb = db_connection(find_id_query)
        if len(rb)== 0:
            query_dep_insert=f"""INSERT INTO hired_employees.jobs (job) VALUES ('{job_name}')"""
            db_connection(query_dep_insert,True)
        else:
            print("The data is saved")
        
        return {"Task":"Inserted"}

    elif request.method == 'PUT':
        data = json.loads(request.data)
        job_id = int(data["id"])
        job_name = data["job"]
        up_query=f"UPDATE hired_employees.jobs SET job = '{job_name}' WHERE id = {job_id}"
        update_status = db_connection(up_query,True)
        return {"Task":"Updted"}

    elif request.method == 'DELETE':
        data = json.loads(request.data)
        dep_id = int(data["id"])
        up_query=f"DELETE FROM hired_employees.jobs WHERE id = {dep_id}"
        update_status = db_connection(up_query,True)


        return {"Task":"Deleted"}




    else:
        return {"Task":"No"}

@app.route("/api/employees", methods=["GET", "POST","PUT","DELETE"])
def data_employees():
    
    if request.method == 'POST':
        data = json.loads(request.data)
        empl_named= data["emp"]
        hir_date=data["date"]
        dep_id=int(data["deb_id"])
        job_id=int(data["job_id"])

        find_id_query=f"SELECT id from hired_employees.hired_employees where employee_name = '{empl_named}'"
        rb = db_connection(find_id_query)
        if len(rb)== 0:
            query_employee_insert=f"INSERT INTO hired_employees.hired_employees (employee_name,hired_date,department_id,job_id) VALUES ('{empl_named}','{hir_date}',{dep_id},{job_id})"
            db_connection(query_employee_insert,True)
        else:
            print("The data is saved")
        
        return {"Task":"Inserted"}

    elif request.method == 'PUT':
        data = json.loads(request.data)
        empl_id = int(data["id"])
        empl_named= data["emp"]
        hir_date=data["date"]
        dep_id=int(data["deb_id"])
        job_id=int(data["job_id"])

        up_query=f"UPDATE hired_employees.hired_employees SET employee_name = '{empl_named}', hired_date='{hir_date}',department_id ={dep_id}, job_id ={job_id} WHERE id = {empl_id}"
        update_status = db_connection(up_query,True)
        return {"Task":"Updted"}

    elif request.method == 'DELETE':
        data = json.loads(request.data)
        empl_id = data["id"]
        up_query=f"DELETE FROM hired_employees.jobs WHERE id = {empl_id}"
        update_status = db_connection(up_query,True)


        return {"Task":"Deleted"}




    else:
        return {"Task":"No"}

if __name__ == '__main__':
    app.run(debug = True ,host = '0.0.0.0',port=8888)