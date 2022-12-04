import streamlit as st
import re
import ftfy
import pandas as pd

# Load data
def load_data():
    data = pd.read_csv('fake_sentiHir.csv')
    return data
# Search a query within a specific column in a dataframe
def search(word, col, df):
    ids = df[col].str.contains(word, flags= re.IGNORECASE, regex=True, na=False)
    return df[ids]

# Process and Show tweets in text
def show_tweets(df):
    st.write("""#### Total number of tweets:""",len(df))
    for _, row in df.iterrows():
        with st.container():
            tags = [" ".join(tag.capitalize().split("_")) for tag in row["tags"]]
            tags = " + ".join(tags)
            st.write("Sentiment score: ", row["sentiment_scores"])
            st.markdown(f"Operator(s): **_{tags}_**")
            st.markdown(f'<div class="temp">{ftfy.fix_encoding(row["text"])}</div>', unsafe_allow_html=True)

# First read data and then preprocess 'tags' column, then drop duplicates based on 'text' column
data = load_data()
data["tags"] = data["tags"].apply(lambda s: s.replace("{","")).apply(lambda s: s.replace("}","")).apply(lambda s: s.replace("'","")).apply(lambda s: s.strip()).apply(lambda s: s.replace(" ","")).apply(lambda s: s.split(","))
data.drop_duplicates(subset=["text"], keep='last', ignore_index=True, inplace=True)

# define this function to call it in app.py as search page
def show_search_page():
    query = st.text_input('Search Bar', placeholder="Search here ...")
    if query:
        res = search(query, "text", data)
        show_tweets(res)