import cv2
import numpy as np
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="AI Pro-Vision", layout="wide")

# Directory creation
for folder in ['records', 'registered_faces', 'config']:
    if not os.path.exists(folder): os.makedirs(folder)

DB_FILE = "student_database.csv"
PASS_FILE = "config/pass.txt"

# --- SESSION STATE (Navigation Control) ---
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Home"

# --- NEON UI CUSTOM CSS ---
st.markdown("""
   <style>
    .stApp { background-color: #050a12; color: #00f2ff; }
    
    /* Card Design */
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
        position: relative;
            mergine-booton: 9px;
    }
    
    h1, h2, h3 { text-shadow: 0 0 10px #00f2ff; color: #ffffff !important; }

    /* Button styling to look like a full clickable card */
    div.stButton > button {
        background-color: transparent;
        color: #00f2ff;
        border: 2px solid #00f2ff;
        box-shadow: 0 0 10px #00f2ff;
        border-bottom-left-radius: 15px;
        border-bottom-right-radius: 15px;
        border-bottom-left-radius: 15px;
        border-top-left-radius: 0px
        height:40px;  
        width: 100%;
        font-size: 16px;
        font-weight: bold;
        transition: 0.3s;
        margin-top: 0px;
    }

    div.stButton > button:hover {
        background-color: #00f2ff;
        color: #000;
        box-shadow: 0 0 30px #00f2ff;
        transform: translateY(2px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION SYNC ---
st.sidebar.title("Quick Nav")
nav_selection = st.sidebar.selectbox("Go to", ["🏠 Home", "📸 Live Scanner", "📝 Registration", "📊 Records"], 
                                     index=["🏠 Home", "📸 Live Scanner", "📝 Registration", "📊 Records"].index(st.session_state.page))

if nav_selection != st.session_state.page:
    st.session_state.page = nav_selection
    st.rerun()

# --- HELPER FUNCTIONS ---
def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE, "r") as f: return f.read().strip()
    return None

# --- PAGE CONTENT ---

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

elif st.session_state.page == "📸 Live Scanner":
    st.title("📸 Face Recognition Terminal")
    if st.button("⬅️ BACK TO DASHBOARD"):
        st.session_state.page = "🏠 Home"
        st.rerun()
    st.camera_input("Scanner Active...")
    st.info("System is ready to recognize faces.")

elif st.session_state.page == "📝 Registration":
    st.title("📝 Student Enrollment")
    if st.button("⬅️ BACK TO DASHBOARD"):
        st.session_state.page = "🏠 Home"
        st.rerun()
    
    with st.container():
        st.subheader("Enter Details")
        name = st.text_input("Full Name")
        roll = st.text_input("Roll Number")
        file = st.file_uploader("Upload Image", type=['jpg', 'png'])
        if st.button("SAVE REGISTRATION"):
            st.success(f"Student {name} registered!")

elif st.session_state.page == "📊 Records":
    st.title("📊 Attendance History")
    if st.button("⬅️ BACK TO DASHBOARD"):
        st.session_state.page = "🏠 Home"
        st.rerun()
    
    st.write("Current Session Attendance Data:")
    # Dummy data for demo
    df = pd.DataFrame({'Name': ['Student 1'], 'Status': ['Present'], 'Time': ['10:00 AM']})
    st.table(df)