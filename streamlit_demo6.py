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
#from vega_datasets import data

st.set_page_config(
    page_title="Time series ",  layout="centered"
)


@st.experimental_memo
#symbol,date,price
#MSFT,Jan 1 2000,39.81
#url	dates	Title	Sentiment	category
def get_data():
    #source = data.stocks()
    #source = pd.read_csv("c:/Download/stocks.csv", delimiter=',')
    source = pd.read_csv("Testset_Vincent_E.csv", delimiter='\t')
    source = source[source.dates.gt("2004-01-01")]
    return source


@st.experimental_memo(ttl=60 * 60 * 24)
def get_chart(data):
    hover = alt.selection_single(
        fields=["dates"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, height=500, title="Evolution of News Articles")
        .mark_line()
        .encode(
            x=alt.X("dates", title="Date"),
            y=alt.Y("number", title="Number of Articles"),
            color="symbol",
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(date)",
            y="price",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("dates", title="Date"),
                alt.Tooltip("price", title="Number"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()


st.title("⬇ Time series annotations")

st.write("Give more context to your time series using annotations!")


# Original time series chart. Omitted `get_chart` for clarity
source = get_data()
chart = get_chart(source)

# Input annotations
ANNOTATIONS = [
    ("Mar 01, 2008", "Pretty good day for GOOG"),
    ("Dec 01, 2007", "Something's going wrong for GOOG & AAPL"),
    ("Nov 01, 2008", "Market starts again thanks to..."),
    ("Dec 01, 2009", "Small crash for GOOG after..."),
]

# Create a chart with annotations
annotations_df = pd.DataFrame(ANNOTATIONS, columns=["date", "event"])
annotations_df.date = pd.to_datetime(annotations_df.date)
annotations_df["y"] = 0
annotation_layer = (
    alt.Chart(annotations_df)
    .encode(
        x="date:T",
        y=alt.Y("y:Q"),
        tooltip=["event"],
    )
    .interactive()
)

# Display both charts together
st.altair_chart((chart + annotation_layer).interactive(), use_container_width=True)

