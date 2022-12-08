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

user@machine % mkdir dags logs plugins

user@machine % docker compose up airflow-init

user@machine % docker-compose up

```

Postgrest creation

```console
user@machine data_challenge % docker run --name postgresql -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=passw0rd -p 5433:5432 -v /Users/martinjurado/Documents/prj/data_challenge/environments/volume/data_db:/var/lib/postgresql/data -d postgres


```













