from flask import Flask
from flask import request, jsonify, json
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine



#PATH_ENV= '/Users/martinjurado/Documents/prj/data_challenge/02_API/.env_db'
PATH_ENV='/home/prj/.env_db'
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




@app.route("/api/departments", methods=["GET","POST","PUT","DELETE"])
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
        
        #logging.basicConfig(format='%(asctime)s %(message)s')
        #logging.warning(query_dep_insert)
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

        #logging.basicConfig(format='%(asctime)s %(message)s')
        #logging.warning(up_query)
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
        #logging.basicConfig(format='%(asctime)s %(message)s')
        #logging.warning(update_status)
        return {"Task":"Deleted"}

    elif request.method == 'GET':
       
        
        up_query=f"SELECT * FROM hired_employees.departments"
        data = db_connection(up_query)
        dict_data =[]
        for d in data:
            id=d[0]
            departments=d[1]
            dict_data.append({'id':id,'departments':departments})

        

        return {"data":dict_data}

    else:
        return {"Task":"No"}

@app.route("/api/jobs", methods=["POST","PUT","DELETE","GET"])
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
        #logging.basicConfig(format='%(asctime)s %(message)s')
        #logging.warning(query_dep_insert)
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
        #logging.basicConfig(format='%(asctime)s %(message)s')
        #logging.warning(up_query)
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
        #logging.basicConfig(format='%(asctime)s %(message)s')
        #logging.warning(up_query)
        return {"Task":"Deleted"}

       

    elif request.method == 'GET':
        up_query=f"SELECT * FROM hired_employees.jobs"
        data = db_connection(up_query)
        dict_data =[]
        for d in data:
            id=d[0]
            job=d[1]
            dict_data.append({'id':id,'job':job})
        return {"data":dict_data}

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
        
        #logging.basicConfig(format='%(asctime)s %(message)s')
        #logging.warning(query_employee_insert)        
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

        #logging.basicConfig(format='%(asctime)s %(message)s')
        #logging.warning(up_query)
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
        #logging.basicConfig(format='%(asctime)s %(message)s')
        #logging.warning(up_query)
        return {"Task":"Deleted"}
    elif request.method == 'GET':
       
        
        up_query=f"SELECT * FROM hired_employees.hired_employees"
        data = db_connection(up_query)
        dict_data=[]
        for d in data:
            id=d[0]
            employee_name=d[1]
            hired_date=d[2]
            department_id=d[3]
            job_id=d[4]

            dict_data.append({'id':id,'employee_name':employee_name,'hired_date':hired_date,'department_id':department_id,'job_id':job_id})
        



        return {"data":dict_data}


    else:
        return {"Task":"No"}


@app.route("/api/2021/quarters", methods=["GET"])
def data_quarters():
    if request.method == 'GET':
        query_2021_quarter="""
            select departments, job, sum (case quarter when 'Q1'then 1 else 0 end) as Q1, sum (case quarter when 'Q2'then 1 else 0 end) as Q2,
sum (case quarter when 'Q3'then 1 else 0 end) as Q3, sum (case quarter when 'Q4'then 1 else 0 end) as Q4
       from (select departments, job ,'Q1' as quarter
            from hired_employees.hired_employees as employee
                     LEFT JOIN hired_employees.departments as departments
                               on employee.department_id = departments.id
                     LEFT JOIN hired_employees.jobs job on employee.job_id = job.id
            where hired_date > '2020-12-31'
              and hired_date < '2021-04-01' and departments is not null and job is not null

            union all

            select departments, job ,'Q2' as quarter
            from hired_employees.hired_employees as employee
                     LEFT JOIN hired_employees.departments as departments
                               on employee.department_id = departments.id
                     LEFT JOIN hired_employees.jobs job on employee.job_id = job.id
            where hired_date >= '2021-04-01'
              and hired_date < '2021-07-01' and departments is not null and job is not null
            union all

            select departments, job ,'Q3' as quarter
            from hired_employees.hired_employees as employee
                     LEFT JOIN hired_employees.departments as departments
                               on employee.department_id = departments.id
                     LEFT JOIN hired_employees.jobs job on employee.job_id = job.id
            where hired_date >= '2021-07-01'
              and hired_date < '2021-10-01' and departments is not null and job is not null
            union all

            select departments, job ,'Q4' as quarter
            from hired_employees.hired_employees as employee
                     LEFT JOIN hired_employees.departments as departments
                               on employee.department_id = departments.id
                     LEFT JOIN hired_employees.jobs job on employee.job_id = job.id
            where hired_date >= '2021-10-01'
              and hired_date < '2022-01-01' and departments is not null and job is not null
            ) as quarter group by departments, job order by departments ASC, job     
        
        """
        data = db_connection(query_2021_quarter)
        dict_data=[]
        for d in data:
            departments=d[0]
            job=d[1]
            q1=d[2]
            q2=d[3]
            q3=d[4]
            q4=d[5]
            dict_data.append({'departments':departments,'job':job,'Q1':q1,'Q2':q2,'Q3':q3,'Q4':q4})

            
        return {"data":dict_data}
    else:
        return {"Error":"Something is wrong"}

@app.route("/api/2021/departments", methods=["GET"])
def data_2021_departments():
    if request.method == 'GET':
        query_2021_departments="""
                                                select department_id, departments, hired
                from (select employee.department_id,
                            departments,
                            count(departments)                                                 as hired,

                            (select AVG(hired) as avg
                            from (select employee.department_id, departments, count(departments) as hired

                                    from hired_employees.hired_employees as employee
                                            LEFT JOIN hired_employees.departments as departments
                                                    on employee.department_id = departments.id
                                    where hired_date > '2020-12-31'
                                    and hired_date < '2022-01-01'
                                    and departments is not null
                                    group by employee.department_id, departments) as query_avg) as const_avr

                    from hired_employees.hired_employees as employee
                            LEFT JOIN hired_employees.departments as departments
                                        on employee.department_id = departments.id
                    where hired_date > '2020-12-31'
                        and hired_date < '2022-01-01'
                        and departments is not null
                    group by employee.department_id, departments) as query
                where query.hired > query.const_avr
                order by query.hired DESC        
        """
        data = db_connection(query_2021_departments)
        dict_data=[]
        for d in data:
            department_id=d[0]
            departments=d[1]
            hired=d[2]
            
            dict_data.append({'department_id':department_id,'departments':departments,'hired':hired})

            
        return {"data":dict_data}
    else:
        return {"Error":"Something is wrong"}



if __name__ == '__main__':
    app.run(debug = True ,host = '0.0.0.0',port=8887)