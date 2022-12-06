FROM ubuntu:20.04

RUN mkdir /home/prj
RUN mkdir /home/prj/airflow-environment
ENV AIRFLOW_HOME /home/prj/airflow-environment

RUN apt-get update



RUN apt-get install net-tools

RUN apt-get -y install apt-utils
RUN apt-get update &&  apt-get install -y python-setuptools python3-pip  python-dev  libffi-dev libssl-dev zip wget
RUN apt-get install -y libcairo2-dev pkg-config gcc python3-dev

RUN ["pip3", "install", "apache-airflow"]
RUN ["pip3", "install", "gcp"]
RUN ["pip3", "install", "statsd"]

RUN sudo apt-get install pkg-config libxml2-dev libxmlsec1-dev libxmlsec1-openssl


RUN ["pip3", "install", "sentry==2.1.2"]
RUN ["pip3", "install", "cryptography"]
RUN ["pip3", "install", "pyspark"]
RUN ["pip3", "install", "apache-airflow[kubernetes]"]

RUN ["pip3", "install", "Flask"]
RUN ["pip3", "install", "Flask-Compress"]
RUN ["pip3", "install", "numpy"]
RUN ["pip3", "install", "pandas"]
RUN ["pip3", "install", "python-dotenv"]
RUN ["pip3", "install", "pandocfilters"]
RUN ["pip3", "install", "parso"]
RUN ["pip3", "install", "patsy"]
RUN ["pip3", "install", "pickleshare"]
RUN ["pip3", "install", "Pillow"]
RUN ["pip3", "install", "plotly"]
RUN ["pip3", "install", "psycopg2-binary"]
RUN ["pip3", "install", "alchemy"]
RUN ["pip3", "install", "prompt-toolkit"]
RUN ["pip3", "install", "pyarrow"]
RUN ["pip3", "install", "Pygments"]
RUN ["pip3", "install", "pylint"]
RUN ["pip3", "install", "pyparsing"]
RUN ["pip3", "install", "pyrsistent"]
RUN ["pip3", "install", "python-dateutil"]
RUN ["pip3", "install", "pytz"]
RUN ["pip3", "install", "PyJWT==1.5.3"]
RUN ["pip3", "install", "qtconsole"]
RUN ["pip3", "install", "requests"]
RUN ["pip3", "install", "retrying"]
RUN ["pip3", "install", "scikit-learn"]
RUN ["pip3", "install", "scipy"]
RUN ["pip3", "install", "seaborn"]
RUN ["pip3", "install", "jupyterlab"]
RUN ["pip3","install","jupyterhub"]
RUN ["pip3", "install", "simplejson"]

RUN cd /home/prj/









