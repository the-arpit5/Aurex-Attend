import cv2
import numpy as np
import streamlit as st
import pandas as pd
import os
import face_recognition
from datetime import datetime
from PIL import Image

# Page Configuration
st.set_page_config(page_title="Aurex Attend AI", layout="wide")

# Directory creation (Zaroori folders)
for folder in ['records', 'img']: 
    if not os.path.exists(folder): os.makedirs(folder)

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
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 15px #00f2ff;
        margin-bottom: 10px;
    }
    h1, h2, h3 { text-shadow: 0 0 10px #00f2ff; color: #ffffff !important; }
    div.stButton > button {
        background-color: transparent; color: #00f2ff;
        border: 2px solid #00f2ff; width: 100%;
        border-radius: 10px; transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #00f2ff; color: #000;
        box-shadow: 0 0 20px #00f2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def load_known_faces():
    path = 'img'
    images = []
    classNames = []
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList, classNames

# --- PAGE CONTENT ---

if st.session_state.page == "🏠 Home":
    st.title("🌟 AUREX ATTEND - AI SYSTEM")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="neon-card"><h3>📸 SCANNER</h3></div>', unsafe_allow_html=True)
        if st.button("🚀 START SCANNING"): st.session_state.page = "📸 Live Scanner"; st.rerun()
    with col2:
        st.markdown('<div class="neon-card"><h3>📝 REGISTER</h3></div>', unsafe_allow_html=True)
        if st.button("➕ ADD NEW ENTRY"): st.session_state.page = "📝 Registration"; st.rerun()
    with col3:
        st.markdown('<div class="neon-card"><h3>📊 RECORDS</h3></div>', unsafe_allow_html=True)
        if st.button("📂 VIEW RECORDS"): st.session_state.page = "📊 Records"; st.rerun()

elif st.session_state.page == "📝 Registration":
    st.title("📝 Student Registration")
    if st.button("⬅️ BACK"): st.session_state.page = "🏠 Home"; st.rerun()
    
    name = st.text_input("Enter Full Name")
    uploaded_file = st.file_uploader("Upload Student Photo", type=['jpg', 'png', 'jpeg'])
    
    if st.button("SAVE REGISTRATION"):
        if name and uploaded_file:
            img = Image.open(uploaded_file)
            img.save(f"img/{name}.jpg") # Photo save ho gayi
            st.success(f"✅ {name} registered! Ab scanner aapko pehchan lega.")
            st.balloons()
        else:
            st.error("Name aur Photo dono zaroori hain!")

elif st.session_state.page == "📸 Live Scanner":
    st.title("📸 AI Face Scanner")
    if st.button("⬅️ BACK"): st.session_state.page = "🏠 Home"; st.rerun()
    
    img_file = st.camera_input("Apna chehra dikhayein")
    
    if img_file:
        # Load database
        known_encodings, known_names = load_known_faces()
        
        # Current Photo process karein
        img = Image.open(img_file)
        img_array = np.array(img)
        img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        
        faces_cur_frame = face_recognition.face_locations(img_rgb)
        encodes_cur_frame = face_recognition.face_encodings(img_rgb, faces_cur_frame)
        
        found = False
        for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
            matches = face_recognition.compare_faces(known_encodings, encodeFace)
            faceDis = face_recognition.face_distance(known_encodings, encodeFace)
            matchIndex = np.argmin(faceDis)
            
            if matches[matchIndex]:
                name = known_names[matchIndex].upper()
                st.success(f"🎯 Match Found: {name}")
                # Attendance record save karna
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                df = pd.DataFrame([[name, dtString]], columns=['Name', 'Time'])
                df.to_csv(f"records/attendance.csv", mode='a', header=False, index=False)
                found = True
        
        if not found:
            st.error("❌ Face not recognized. Please Register first.")

elif st.session_state.page == "📊 Records":
    st.title("📊 Attendance Records")
    if st.button("⬅️ BACK"): st.session_state.page = "🏠 Home"; st.rerun()
    if os.path.exists("records/attendance.csv"):
        df = pd.read_csv("records/attendance.csv", names=['Name', 'Time'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Abhi koi attendance record nahi hai.")
