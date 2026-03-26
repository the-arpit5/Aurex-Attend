import cv2
import numpy as np
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image

# Page Configuration
st.set_page_config(page_title="AUREX ATTEND", layout="wide")

# Directory creation
for folder in ['records', 'registered_faces', 'config']:
    if not os.path.exists(folder): os.makedirs(folder)

DB_FILE = "student_database.csv"
PASS_FILE = "config/pass.txt"

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Home"

# --- NEON UI CUSTOM CSS ---
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
        border-radius: 15px;
        height:45px;  
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

# --- SIDEBAR & ADMIN ACCESS ---
st.sidebar.title("🛡️ Control Panel")
admin_pass = st.sidebar.text_input("Admin Password", type="password", help="Enter password to see registered face photos")

st.sidebar.markdown("---")
nav_selection = st.sidebar.selectbox("Go to", ["🏠 Home", "📸 Live Scanner", "📝 Registration", "📊 Records"], 
                                     index=["🏠 Home", "📸 Live Scanner", "📝 Registration", "📊 Records"].index(st.session_state.page))

if nav_selection != st.session_state.page:
    st.session_state.page = nav_selection
    st.rerun()

# --- PAGE CONTENT ---

if st.session_state.page == "🏠 Home":
    st.title("🌟 AUREX ATTEND - AI SYSTEM")
    st.write("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="neon-card"><h3>📸 SCANNER</h3><p>Mark Daily Attendance</p></div>', unsafe_allow_html=True)
        if st.button("🚀 START SCANNING", key="home_scan"):
            st.session_state.page = "📸 Live Scanner"; st.rerun()
    with col2:
        st.markdown('<div class="neon-card"><h3>📝 REGISTER</h3><p>Add New Student</p></div>', unsafe_allow_html=True)
        if st.button("➕ ADD NEW ENTRY", key="home_reg"):
            st.session_state.page = "📝 Registration"; st.rerun()
    with col3:
        st.markdown('<div class="neon-card"><h3>📊 RECORDS</h3><p>Check Database</p></div>', unsafe_allow_html=True)
        if st.button("📂 VIEW RECORDS", key="home_rec"):
            st.session_state.page = "📊 Records"; st.rerun()

elif st.session_state.page == "📸 Live Scanner":
    st.title("📸 Recognition Terminal")
    if st.button("⬅️ DASHBOARD"): st.session_state.page = "🏠 Home"; st.rerun()
    st.camera_input("Scanner Active...")

elif st.session_state.page == "📝 Registration":
    st.title("📝 Student Enrollment")
    if st.button("⬅️ DASHBOARD"): st.session_state.page = "🏠 Home"; st.rerun()
    
    name = st.text_input("Full Name")
    roll = st.text_input("Roll Number")
    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
    
    if st.button("SAVE REGISTRATION"):
        if name and roll and uploaded_file:
            # Save Image to Server
            img = Image.open(uploaded_file)
            img_path = os.path.join("registered_faces", f"{name}_{roll}.jpg")
            img.save(img_path)
            st.success(f"✅ {name} registered successfully and photo saved on server!")
        else:
            st.error("Please fill all details and upload a photo.")

elif st.session_state.page == "📊 Records":
    st.title("📊 Attendance History")
    if st.button("⬅️ DASHBOARD"): st.session_state.page = "🏠 Home"; st.rerun()
    
    # Section 1: Public Attendance Table
    st.subheader("Recent Attendance")
    df = pd.DataFrame({'Name': ['Student 1'], 'Status': ['Present'], 'Time': ['10:00 AM']})
    st.table(df)

    # Section 2: ADMIN ONLY PHOTO VIEW
    st.markdown("---")
    if admin_pass == "admin123": # <--- Apna Password yahan change karein
        st.subheader("📁 Registered Face Database (Admin Only)")
        
        photo_folder = "registered_faces"
        photos = [f for f in os.listdir(photo_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
        
        if photos:
            cols = st.columns(4)
            for idx, photo_name in enumerate(photos):
                with cols[idx % 4]:
                    img = Image.open(os.path.join(photo_folder, photo_name))
                    st.image(img, caption=photo_name, use_column_width=True)
        else:
            st.info("Abhi tak koi registration nahi hui hai.")
    else:
        st.warning("🔒 Enter Admin Password in Sidebar to see registered photos.")
