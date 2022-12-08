import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json
import numpy as np
import plotly.figure_factory as ff

st.write('# Data Challenges')  
st.markdown('''
This is the result of challenge #2, which was to visualize queries 2.1 and 22.''')
st.header('2.1 Number of employees hired for each job and department')

data_quarterm = requests.get("http://host.docker.internal:8887/api/2021/quarters")
data_quarterm = data_quarterm.json()
dataset_onep = pd.DataFrame.from_dict(data_quarterm['data'])
dataset_one =(dataset_onep[['Q1','Q2','Q3','Q4']].sum())
dataset_one_sum=pd.DataFrame(dataset_one,columns=['Sum'])
dataset_one_sum['Quarter']=dataset_one_sum.index


st.dataframe(dataset_onep.reindex(['departments','job','Q1','Q2','Q3','Q4'], axis=1))
st.header('Quarter distribution')

fig1 = px.histogram(dataset_one_sum, x="Quarter", y="Sum",  marginal="rug", hover_data=dataset_one_sum.columns)

st.plotly_chart(fig1)

st.header('2.2 List of departments that hired the most employees in 2021')
data_departments = requests.get("http://host.docker.internal:8887/api/2021/departments")
data_departments = data_departments.json()
dataset_two = pd.DataFrame.from_dict(data_departments['data'])
    



st.dataframe(dataset_two)

st.header('Bar chart by deparments')


    
fig2 = px.bar(dataset_two, x='departments', y='hired',
                    title=f'Departments with more people hired than the average in 2021')

    
st.plotly_chart(fig2)

with st.sidebar:
    st.subheader('Martin Jurado')
    st.markdown('You can follow me in my medium https://medium.com/@martin.jurado.p')
st.sidebar.image('https://miro.medium.com/fit/c/96/96/1*lkTciXpKUapoa7umuE0sDQ.jpeg', width=50)