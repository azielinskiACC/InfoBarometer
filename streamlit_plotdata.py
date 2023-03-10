# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 12:48:22 2023
https://blog.streamlit.io/host-your-streamlit-app-for-free/
https://github.com/streamlit/example-app-zero-shot-text-classifier
@author: zia
"""

import pandas as pd
import plotly.graph_objects as go
import plotly_express as px
import streamlit as st


gitcsv = 'C:/Users/zia/Downloads/Testset_Vincent_E.csv'

df = pd.read_csv(gitcsv, encoding = "utf-8", sep="\t") 


print(df[:5])
df['dates'] = pd.to_datetime(df['dates'])

freq='M' 
df = df.groupby(['Sentiment', pd.Grouper(key='dates', freq=freq)])['Sentiment'].agg(['count']).reset_index()
df = df.sort_values(by=['dates', 'count']).reset_index(drop=True)

# group the dataframe
group = df.groupby('Sentiment')

# create a blank canvas
fig = go.Figure()


for group_name, df in group:
    fig.add_trace(
        go.Scatter(
              x=df['dates']
            , y=df['count']
            , fill='tozeroy'
            , name=group_name
        ))

    # generate a regression line with px
    plot = px.scatter(df, x=df['dates'], y=df['count']
                          , trendline="lowess")
    st.plotly_chart(plot, use_container_width=True)    

    # extract points as plain x and y
# =============================================================================
#     x_trend = help_fig["data"][1]['x']
#     y_trend = help_fig["data"][1]['y']
# 
#     # add the x,y data as a scatter graph object
#     fig.add_trace(
#         go.Scatter(x=x_trend, y=y_trend
#                    , name=str('trend ' + group_name)
#                    , line = dict(width=4, dash='dash')))
# 
#     transparent = 'rgba(0,0,0,0)'
# 
#     fig.update_layout(
#         hovermode='x',
#         showlegend=True
#         # , title_text=str('Court Data for ' + str(year))
#         , paper_bgcolor=transparent
#         , plot_bgcolor=transparent
#         , title=#'Monthly Time Series of News Articles from automobilwoche for innovation-related keywords with Regression'
#         'Monthly Time Series of News Articles from automobil-industrie-Vogel for innovation-related keywords with Regression'
#     )
# 
# =============================================================================
  
    #st.pyplot(fig)
    # plot = px.scatter(df, x=x_axis_val, y=y_axis_val)

    
