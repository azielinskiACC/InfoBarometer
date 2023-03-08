# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 12:48:22 2023
https://blog.streamlit.io/host-your-streamlit-app-for-free/
https://github.com/streamlit/example-app-zero-shot-text-classifier
@author: zia
"""

import altair as alt
import pandas as pd
import streamlit as st
import plotly
import plotly.graph_objects as go
import plotly_express as px

st.set_page_config(
    page_title="Time series Infobarometer",  layout="centered"
)


gitcsv = 'Testset_vincent_E.csv'
# types      dates      count
# Diesel         2016-01-31      1
df = pd.read_csv(gitcsv, encoding = "utf-8", sep="\t") 

df['dates'] = pd.to_datetime(df['dates'])

freq='M' # or D or Y

df = df.groupby(['Sentiment', pd.Grouper(key='dates', freq=freq)])['Sentiment'].agg(['count']).reset_index()
df = df.sort_values(by=['dates', 'count']).reset_index(drop=True)

# group the dataframe
group = df.groupby('Sentiment')

# create a blank canvas
fig = go.Figure()

# each group iteration returns a tuple
# (group name, dataframe)
for group_name, df in group:
    fig.add_trace(
        go.Scatter(
              x=df['dates']
            , y=df['count']
            , fill='tozeroy'
            , name=group_name
        ))

    # generate a regression line with px
    help_fig = px.scatter(df, x=df['dates'], y=df['count']
                          , trendline="lowess")
    # extract points as plain x and y
    x_trend = help_fig["data"][1]['x']
    y_trend = help_fig["data"][1]['y']

    # add the x,y data as a scatter graph object
    fig.add_trace(
        go.Scatter(x=x_trend, y=y_trend
                   , name=str('trend ' + group_name)
                   , line = dict(width=4, dash='dash')))

    transparent = 'rgba(0,0,0,0)'

    fig.update_layout(
        hovermode='x',
        showlegend=True
        # , title_text=str('Court Data for ' + str(year))
        , paper_bgcolor=transparent
        , plot_bgcolor=transparent
        , title=#'Monthly Time Series of News Articles from automobilwoche for innovation-related keywords with Regression'
        'Monthly Time Series of News Articles from automobil-industrie-Vogel for innovation-related keywords with Regression'
    )


st.pyplot(fig)






