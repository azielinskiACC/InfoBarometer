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
#from tensorflow.keras.utils import get_file
#from transformers import pipeline
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer


st.set_page_config(layout="centered", page_icon="🗺️", page_title="Sentiment")


@st.experimental_memo


@st.experimental_singleton
def get_classifier():
    return pipeline("sentiment-analysis")
#    return pipeline("sentiment-analysis", model='oliverguhr/german-sentiment-bert', tokenizer='oliverguhr/german-sentiment-bert', top_k=3)



@st.experimental_memo(show_spinner=False)
def predict(reviews):
    return classifier(reviews)


def result_to_positive_class_probability(result):
        return result["score"] if result["label"] == "POSITIVE" else 1 - result["score"]


classifier = get_classifier()
#st.title("🗺️ Bias map")
st.write("""Discover the Sentiment""")

text_input = st.text_input(
    label="Type in a sentence. Use * as a country placeholder", value="This movie was filmed in *"
)

st.write("---")

if "*" not in text_input:
    st.error("Your input sentence must contain a `*` which will be used as the country placeholder.")
    st.stop()

if text_input:
    st.caption("Output:")

    st.write(f"""Input: _"{text_input}"_:""")
    with st.spinner("Computing probabilities..."):
        reviews = []
        reviews.append(text_input)

        results = predict(reviews)
        probas = map(result_to_positive_class_probability, results)

        probas_df = pd.DataFrame(
            {"Positive class probability": probas}
        )

        st.write("Data (sorted by ascending 'positive'-ness probability):")
        st.dataframe(probas_df.sort_values(by="Positive class probability", ascending=True), height=350,)