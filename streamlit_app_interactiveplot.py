# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 16:27:27 2023

https://blog.streamlit.io/host-your-streamlit-app-for-free/

1. https://streamlit.io/cloud
https://github.com/patidarparas13/Sentiment-Analyzer-Tool/blob/master/sentiment_analyzer.py
https://discuss.streamlit.io/t/is-it-possible-to-display-an-html-file-in-streamlit/23594/5
https://www.youtube.com/watch?v=3f-j-PZ5N8A
"""

#Import the required Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import plotly.express as px

st.set_page_config(layout="wide")

# Functions for each of the pages
def home(uploaded_file):
    if uploaded_file:
        st.header('Begin exploring the data using the menu on the left')
    else:
        st.header('To begin please upload a file')

def data_summary():
    st.header('Statistics of Dataframe')
    st.write(df.describe())

def data_header():
    st.header('Header of Dataframe')
    st.write(df.head())

def displayplot():
    st.header('Plot of Data')

    fig, ax = plt.subplots(1,1)
    ax.scatter(x=df['Depth'], y=df['Magnitude'])
    ax.set_xlabel('Depth')
    ax.set_ylabel('Magnitude')

    st.pyplot(fig)

def interactive_plot():
    col1, col2 = st.columns(2)

    x_axis_val = col1.selectbox('Select the X-axis', options=df.columns)
    y_axis_val = col2.selectbox('Select the Y-axis', options=df.columns)

    plot = px.scatter(df, x=x_axis_val, y=y_axis_val)
    st.plotly_chart(plot, use_container_width=True)

# Add a title and intro text
st.title('Online News Data Explorer')
st.text('This is a web app to allow exploration of Automotive News')

# Sidebar setup
st.sidebar.title('Sidebar')
upload_file = 'stocks.csv'
#st.sidebar.file_uploader('Upload a file containing the data')
#Sidebar navigation
st.sidebar.title('Navigation')
options = st.sidebar.radio('Select what you want to display:', ['Home', 'Data Summary', 'Data Header', 'Scatter Plot', 'Fancy Plots'])

# Check if file has been uploaded
if upload_file is not None:
    df = pd.read_csv('stocks.csv')

# Navigation options
if options == 'Home':
    home(upload_file)
elif options == 'Data Summary':
    data_summary()
elif options == 'Data Header':
    data_header()
elif options == 'Scatter Plot':
    displayplot()
elif options == 'Interactive Plots':
    interactive_plot()