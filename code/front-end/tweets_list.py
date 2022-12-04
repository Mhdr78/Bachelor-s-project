import streamlit as st
import pandas as pd 
import ftfy
import plotly.express as px
import re

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load data
def load_data():
    data = pd.read_csv('fake_sentiHir.csv')
    return data

# Process and Show tweets in text
def show_tweets(df):
    st.write("""#### Total number of tweets:""",len(df))
    for _, row in df.iterrows():
        with st.container():
            st.write("sentiment score: ", row["sentiment_scores"])
            st.markdown(f'<div class="temp">{ftfy.fix_encoding(row["text"])}</div>', unsafe_allow_html=True)


# First read data and then preprocess 'tags' column, then drop duplicates based on 'text' column
data = load_data()
data["tags"] = data["tags"].apply(lambda s: s.replace("{","")).apply(lambda s: s.replace("}","")).apply(lambda s: s.replace("'","")).apply(lambda s: s.strip()).apply(lambda s: s.replace(" ","")).apply(lambda s: s.split(","))
data.drop_duplicates(subset=["text"], keep='last', ignore_index=True, inplace=True)

# define this function to call it in app.py as overview page
def show_overview_page():
    # Sidebar
    st.sidebar.title("Configuration")
    select=st.sidebar.selectbox('Visualisation Of Tweets',['Histogram','Pie Chart'],key=1)
    sentiment = data['sentiment_scores'].value_counts()
    sentiment = pd.DataFrame({'Sentiment':sentiment.index,'Tweets':sentiment.values})
    st.markdown("###  Sentiment count")
    if select == "Histogram":
            fig = px.bar(sentiment, x='Sentiment', y='Tweets', color = 'Tweets', height= 500)
            st.plotly_chart(fig)
    else:
            fig = px.pie(sentiment, values='Tweets', names='Sentiment')
            st.plotly_chart(fig)

    #multiselect menu to show histogram for comparison operators
    choice = st.sidebar.multiselect("Operators", ('Hamrah_Aval', 'Irancell', 'Rightel'), key = '3')
    choice = [ch.lower() for ch in choice]
    if len(choice)>0:
        op_data = data[data["tags"].apply(lambda tag: len(tag) == 1)]
        op_data["tags"] = op_data.tags.apply(lambda x: "".join(x))
        op_data = op_data[op_data.tags.isin(choice)]
        fig1 = px.histogram(op_data, x='tags', y='sentiment_scores', histfunc='count', color='tags', labels={'sentiment_scores':'score'}, facet_col="sentiment_scores", height=600, width=800)
        st.plotly_chart(fig1)

    # Filtering tweets based on their operators, fake or real and their score
    operator = st.sidebar.multiselect("Operators", ('Hamrah_Aval', 'Irancell', 'Rightel'), key = '4')
    operator = [ch.lower() for ch in operator]
    is_real = st.sidebar.selectbox("Fake or Real", ("Fake", "Real", "Both"))
    fake_dict = {"Fake": 0, "Real": 1, "Both": -1}
    is_real = fake_dict[is_real]
    score = st.sidebar.selectbox("Specific score", (2,1,0,-1,-2, "all"))
    ok = st.sidebar.button("Show tweets")

    # if user click on show tweets button then this condition applies.
    if ok and len(operator) > 0:
        st.title("List of tweets")
        selected_data = data[data["tags"].apply(lambda tag: set(tag) == set(operator))]
        if is_real == 1 or is_real == 0:
            selected_data = selected_data[selected_data["is_real"] == is_real]
        if score == "all":
            pass
        else:
            selected_data = selected_data[selected_data["sentiment_scores"] == score]
        
        show_tweets(selected_data)
