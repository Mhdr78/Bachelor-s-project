import streamlit as st
from streamlit_option_menu import option_menu
from tweets_list import show_overview_page
from search import show_search_page

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# We design three different theme for navigation between pages, 
# in order to show each theme you must uncomment that theme's code and comment the others.
# Theme 1 for Navigation
tab1, tab2 = st.tabs(["Overview", "Search"])

with tab1:
    show_overview_page()

with tab2:
    show_search_page()

###########################################################################

# Theme 2 as an option_menu in the sidebar
# selected = option_menu(None, ["Overview", "Search", "About"], 
#     icons=['house', 'search', "cast"], 
#     default_index=0, orientation="horizontal")
# 
# if selected == "Overview":
#     show_overview_page()
# elif selected == "Search":
#     show_search_page()

###########################################################################

# Theme 3 as a sidebar
# page = st.sidebar.selectbox("Overview or Search",("Overview", "Search"))
# 
# if page.lower() == "search":
#     show_search_page()
# else:
#     show_overview_page()

