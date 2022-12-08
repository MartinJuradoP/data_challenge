FROM ubuntu:20.04

RUN mkdir /home/prj
WORKDIR /home/prj


RUN apt-get update



RUN apt-get install net-tools

RUN apt-get -y install apt-utils
RUN apt-get update &&  apt-get install -y python-setuptools python3-pip  python-dev 


RUN ["pip3", "install", "Flask"]
RUN ["pip3", "install", "Flask-Compress"]
RUN ["pip3", "install", "numpy"]
RUN ["pip3", "install", "pandas"]
RUN ["pip3", "install", "python-dotenv"]
RUN ["pip3", "install", "streamlit"]
RUN ["pip3", "install", "parso"]
RUN ["pip3", "install", "patsy"]
RUN ["pip3", "install", "pickleshare"]
RUN ["pip3", "install", "Pillow"]
RUN ["pip3", "install", "plotly"]
RUN ["pip3", "install", "alchemy"]
RUN ["pip3", "install", "prompt-toolkit"]
RUN ["pip3", "install", "plotly"]
RUN ["pip3", "install", "PyJWT==1.5.3"]
RUN ["pip3", "install", "requests"]
RUN ["pip3", "install", "retrying"]
RUN ["pip3", "install", "scikit-learn"]
RUN ["pip3", "install", "scipy"]
RUN ["pip3", "install", "seaborn"]
RUN ["pip3", "install", "simplejson"]

ENTRYPOINT [ "streamlit" ]

CMD ["run","visual_server.py" ]










