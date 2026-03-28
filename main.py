import cv2
import numpy as np
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Page Configuration (इसे सबसे ऊपर होना चाहिए)
st.set_page_config(page_title="AI Pro-Vision", layout="wide")

# 2. फोल्डर बनाना (Directory Creation)
for folder in ['records', 'registered_faces', 'config']:
    if not os.path.exists(folder): 
        os.makedirs(folder)

DB_FILE = "student_database.csv"
PASS_FILE = "config/pass.txt"

# 3. Session State (पेज नेविगेशन के लिए)
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Home"

# 4. Neon UI CSS (डिजाइन के लिए)
st.markdown("""
    <style>
    .stApp { background-color: #050a12; color: #00f2ff; }
    
    .neon-card {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid #00f2ff;
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 0 15px #00f2ff, inset 0 0 10px #00f2ff;
        height: 190px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-bottom: 10px;
    }
    
    h1, h2, h3 { text-shadow: 0 0 10px #00f2ff; color: #ffffff !important; }

    div.stButton > button {
        background-color: transparent;
        color: #00f2ff;
        border: 2px solid #00f2ff;
        box-shadow: 0 0 10px #00f2ff;
        border-radius: 0px 0px 15px 15px;
        height: 45px;  
        width: 100%;
        font-weight: bold;
        transition: 0.3s;
    }

    div.stButton > button:hover {
        background-color: #00f2ff;
        color: #000;
        box-shadow: 0 0 30px #00f2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# 5. Sidebar Navigation
st.sidebar.title("Quick Nav")
nav_options = ["🏠 Home", "📸 Live Scanner", "📝 Registration", "📊 Records"]
nav_selection = st.sidebar.selectbox("Go to", nav_options, index=nav_options.index(st.session_state.page))

if nav_selection != st.session_state.page:
    st.session_state.page = nav_selection
    st.rerun()

# 6. Home Page Content
if st.session_state.page == "🏠 Home":
    st.title("🌟 AUREX ATTEND - AI SYSTEM")
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="neon-card"><h3>📸 SCANNER</h3><p>Mark Daily Attendance</p></div>', unsafe_allow_html=True)
        if st.button("🚀 START SCANNING", key="home_scan"):
            st.session_state.page = "📸 Live Scanner"
            st.rerun()
            
    with col2:
        st.markdown('<div class="neon-card"><h3>📝 REGISTER</h3><p>Add New Student</p></div>', unsafe_allow_html=True)
        if st.button("➕ ADD NEW ENTRY", key="home_reg"):
            st.session_state.page = "📝 Registration"
            st.rerun()

    with col3:
        st.markdown('<div class="neon-card"><h3>📊 RECORDS</h3><p>Check Database</p></div>', unsafe_allow_html=True)
        if st.button("📂 VIEW RECORDS", key="home_rec"):
            st.session_state.page = "📊 Records"
            st.rerun()

# अन्य पेजों के लिए (Scanner, Registration आदि) यहाँ कोड जोड़ें...
