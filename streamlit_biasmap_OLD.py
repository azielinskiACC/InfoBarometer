# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 19:06:12 2023

@author: https://github.com/arnaudmiribel/bias-map/blob/main/streamlit_app.py
"""

import json
#import re
#import urllib

import pandas as pd
import plotly.express as px
import streamlit as st
import random
import string
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer


st.set_page_config(layout="centered", page_title="Sentiment")

@st.experimental_singleton
def get_classifier():
    return pipeline("sentiment-analysis", model='oliverguhr/german-sentiment-bert', tokenizer='oliverguhr/german-sentiment-bert', top_k=3)

@st.experimental_memo(show_spinner=False)
def predict(reviews):
    return classifier(reviews)

def result_to_positive_class_probability(result):
        return result["score"] if result["label"] == "POSITIVE" else 1 - result["score"]

classifier = get_classifier()

st.write("""Discover the Sentiment""")

# =============================================================================
# text_input = st.text_input(
#     label="Type in a German news article. "
# )
# =============================================================================
text_input = st.text_area("Type in a German news article",max_chars = 500)
#st.write('Repeat:', text_input)



st.write("---")

if len(text_input) > 1 :
    st.caption("Output:")


    with st.spinner("Computing probabilities..."):
        reviews = []
        reviews.append(text_input)
        results = predict(reviews)

        st.write("Probability:", results)
        #st.dataframe(probas_df.sort_values(by="Positive class probability", ascending=True), height=350,)