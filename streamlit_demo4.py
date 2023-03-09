# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 12:48:22 2023
https://blog.streamlit.io/host-your-streamlit-app-for-free/
https://github.com/streamlit/example-app-zero-shot-text-classifier
@author: zia
"""

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly_express as px


#create a canvas for each item
interactive =  st.beta_container()


st.set_page_config(
    page_title="Time series Infobarometer",  layout="centered"
)


gitcsv = 'Testset_Vincent_E.csv'
# types      dates      count
# Diesel         2016-01-31      1
df = pd.read_csv(gitcsv, encoding = "utf-8", sep="\t") 

df['dates'] = pd.to_datetime(df['dates'])

freq='M' # or D or Y

df = df.groupby(['Sentiment', pd.Grouper(key='dates', freq=freq)])['Sentiment'].agg(['count']).reset_index()
df = df.sort_values(by=['dates', 'count']).reset_index(drop=True)

# group the dataframe
group = df.groupby('Sentiment')


with interactive:
    fig = go.Figure
    for group_name, df in group:
        fig.add_trace( go.Scatter(
              x=df['dates']
            , y=df['count']
            , fill='tozeroy'
            , name=group_name
        ))

#    fig = px.scatter(df, x=df['dates'], y=df['count'], trendline="lowess")
    fig.show()
        

#st.pyplot(fig)






