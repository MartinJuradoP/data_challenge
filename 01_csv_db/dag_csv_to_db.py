from datetime import datetime, timedelta, date
from airflow import DAG
from airflow.operators.python import PythonOperator
#Code Info
import bmw_connect_plants as bmw
import pandas as pd
import numpy as np
import time
import psycopg2
import warnings
warnings.filterwarnings("ignore")
import logging

import os

from dotenv import load_dotenv

PATH_ENV= '/opt/airflow/env'
folder_path = "/opt/airflow/code_data"

load_dotenv(PATH_ENV)

######### CODE            ################
##########################################



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
    start_date= datetime(2022,10,25,9),
    schedule_interval = "@hourly",
    catchup=False


) as dag:


    t1 = PythonOperator(

        task_id='First_task_update',
        python_callable=main_func,
    )
    
    

    t1