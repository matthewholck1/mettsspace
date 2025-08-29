import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import time
import base64
from io import StringIO
from dd_functions import *

# pages
if 'initiate' not in st.session_state:
    st.session_state.initiate = True
if 'main_page' not in st.session_state:
    st.session_state.main_page = False
if 'cursor' not in st.session_state:
    st.session_state.cursor = 0
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()

st.set_page_config(
    page_title="metts space",     # optional
    page_icon="67.png",          # optional
    layout="wide",           # this makes it wide
)

token = st.secrets["GITHUB_TOKEN"]
owner = st.secrets["OWNER"]
repo = st.secrets["REPO"]

if st.session_state.initiate:

    
    # Private repo info
    path = "calendar.csv"  # path to your CSV inside the repo

    content = call_git(owner, repo, path, token)

    decoded = base64.b64decode(content).decode("utf-8")
    
    # Load CSV into pandas DataFrame
    df = pd.read_csv(StringIO(decoded))
    df.set_index("date_index", inplace=True)
    st.session_state.df = df

    #st.session_state.main_page = True
    st.session_state.initiate = False
    st.rerun()

# if st.session_state.main_page:
else:
    
    cursor = st.session_state.cursor
    df = st.session_state.df
    
    st.header("Semester of doom and despair")
    
    # Target datetime
    end_date = datetime(2025, 12, 6, 0, 0, 0)
    start_date = datetime(2025, 8, 24, 0, 0 ,0)
    now = datetime.now() 
    search_date =  now + timedelta(days=cursor)
    time_left = end_date - now
    days = time_left.days

    # Days until max_date
    days_to_max = (now - search_date).days
    
    # Days since min_date
    days_to_min = (search_date - start_date).days
    
    search_date_index = str(search_date.date())
    text = df.loc[search_date_index].description

    media = df.loc[search_date_index].media
    
    st.subheader(f'{days} days left...')
    
    if media:
        file_name = f'{search_date.strftime("%Y%m%d")}.png'
        content = call_git(owner, repo, file_name, token)
        # b64 = base64.b64encode(content).decode()
        
        # with open(media, "rb") as f:
            # data = f.read()
            # b64 = base64.b64encode(data).decode()

        img_src = f"data:image/png;base64,{content}"
        
    else:
        img_src = None
    
    st.write('______________________________________________')
    # <br><img src="{img_src}" width="200" onerror="this.style.display='none'; this.parentElement.innerHTML='No image';">
    st.markdown(
        f"""
        <div style="border:2px solid #E6E6FA; padding:10px; margin:5px;">
            <h3><u>{search_date.strftime('%A, %B %d %Y')}</u></h3>
            {text}
            <br><img src="{img_src}" width="200" onerror="this.style.display='none'; this.parentElement.innerHTML='No image';">
            <br>&nbsp;
        </div>
        <br>
        """,
        unsafe_allow_html=True
    )
    spacer, col1, col2, col3, col4 = st.columns([0.5,1,1,1,1])
    # col1, col2, col3, col4 = st.columns([0.05, 1, 0.05, 1])
    
    with col1:
        
        back_all = st.button('⏪')
        
        if search_date.date() != start_date.date():
            if back_all:
                st.session_state.cursor -= days_to_min
                st.rerun()
                
    with col2:
        back = st.button('◀️')
        
        if search_date.date() != start_date.date():
            if back:
                st.session_state.cursor -= 1
                st.rerun()
    with col3:
        
        next = st.button('▶️')
        if search_date.date() != now.date():
            if next:
                st.session_state.cursor += 1
                st.rerun()

    with col4:
        
        next_all = st.button('⏩')
        if search_date.date() != now.date():
            if next_all:
                st.session_state.cursor += days_to_max
                st.rerun()

