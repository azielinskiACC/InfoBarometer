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
#from tensorflow.keras.utils import get_file
#from transformers import pipeline
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer


st.set_page_config(layout="centered", page_icon="🗺️", page_title="Sentiment")


@st.experimental_memo


@st.experimental_singleton
def get_classifier():
#    return pipeline("sentiment-analysis")
    return pipeline("sentiment-analysis", model='oliverguhr/german-sentiment-bert', tokenizer='oliverguhr/german-sentiment-bert', top_k=3)



@st.experimental_memo(show_spinner=False)
def predict(reviews):
    return classifier(reviews)


def result_to_positive_class_probability(result):
        return result["score"] if result["label"] == "POSITIVE" else 1 - result["score"]

#def result_to_negative_class_probability(result):
  #     return result["score"] if result["label"] == "NEGATIVE" else 1 - result["score"]

#def result_to_neutral_class_probability(result):
  #      return result["score"] if result["label"] == "NEUTRAL" else 1 - result["score"]


classifier = get_classifier()
#st.title("🗺️ Bias map")
st.write("""Discover the Sentiment""")

#text_input = st.text_input(
#    label="Type in a German news article. "
#)
if 'input_keys' not in st.session_state:
    st.session_state.input_keys= []

if st.button("Add new row"):
    st.session_state.input_keys.append(random.choice(string.ascii_uppercase)+str(random.randint(0,999999)))

input_values = []
for input_key in st.session_state.input_keys:
    input_value = st.text_input("Please input something", key=input_key)
    input_values.append(input_value)

st.write("---")

##if "*" not in text_input:
 #   st.error("Your input sentence must contain a German news article.")
 #   st.stop()

#if text_input:
 #   st.caption("Output:")
if input_values :
    st.caption("Output:")

   # st.write(f"""Input: _"{text_input}"_:""")
   # st.write(f"""Input: _"{text_input}"_:""")
    
    with st.spinner("Computing probabilities..."):
        reviews = []
        #reviews.append(text_input)
        reviews.append(input_values)

        results = predict(reviews)
        probas_pos = map(result_to_positive_class_probability, results)
 #       probas_neg = map(result_to_negative_class_probability, results)
  #      probas_neu = map(result_to_neutral_class_probability, results)

        probas_df = pd.DataFrame(
            {"Positive class probability": probas_pos}
        )

        st.write("Data (sorted by ascending 'positive' probability):")
        st.dataframe(probas_df.sort_values(by="Positive class probability", ascending=True), height=350,)