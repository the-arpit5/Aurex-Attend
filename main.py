import cv2
import numpy as np
import streamlit as st
import pandas as pd
import os
import face_recognition
from datetime import datetime
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="AI Pro-Vision", layout="wide")

# 2. Directory Creation (Yahan humne 'img' folder add kiya hai database ke liye)
for folder in ['records', 'img', 'config']:
    if not os.path.exists(folder): 
        os.makedirs(folder)

# --- Helper Functions (Face Recognition Logic) ---

def load_known_faces():
    """Database folder (img) se saari photos load karke unke encodings banata hai"""
    path = 'img'
    images = []
    classNames = []
    myList = os.listdir(path)
    
    encodeList = []
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        if curImg is not None:
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
            # BGR to RGB conversion for face_recognition
            img_rgb = cv2.cvtColor(curImg, cv2.COLOR_BGR2RGB)
            try:
                encode = face_recognition.face_encodings(img_rgb)[0]
                encodeList.append(encode)
            except IndexError:
                continue # Agar photo mein face na mile toh skip karein
    return encodeList, classNames

def mark_attendance(name):
    """Attendance ko CSV file mein save karta hai"""
    file_path = 'records/attendance.csv'
    now = datetime.now()
    dtString = now.strftime('%Y-%m-%d %H:%M:%S')
    
    # Agar file nahi hai toh header ke saath banayein
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=['Name', 'Timestamp'])
        df.to_csv(file_path, index=False)
        
    df = pd.read_csv(file_path)
    # Check karein ki kya aaj ye banda pehle hi aa chuka hai? (Optional logic)
    new_entry = pd.DataFrame([[name, dtString]], columns=['Name', 'Timestamp'])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(file_path, index=False)

# --- 3. Session State ---
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Home"

# --- 4. Neon UI CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050a12; color: #00f2ff; }
    .neon-card {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid #00f2ff;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 15px #00f2ff, inset 0 0 10px #00f2ff;
        margin-bottom: 10px;
    }
    h1, h2, h3 { text-shadow: 0 0 10px #00f2ff; color: #ffffff !important; }
    div.stButton > button {
        background-color: transparent; color: #00f2ff;
        border: 2px solid #00f2ff; box-shadow: 0 0 10px #00f2ff;
        border-radius: 0px 0px 15px 15px; height: 45px; width: 100%;
        font-weight: bold; transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #00f2ff; color: #000; box-shadow: 0 0 30px #00f2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. Navigation ---
st.sidebar.title("Aurex Menu")
nav_options = ["🏠 Home", "📸 Live Scanner", "📝 Registration", "📊 Records"]
nav_selection = st.sidebar.selectbox("Navigate", nav_options, index=nav_options.index(st.session_state.page))

if nav_selection != st.session_state.page:
    st.session_state.page = nav_selection
    st.rerun()

# --- 6. Page Content ---

if st.session_state.page == "🏠 Home":
    st.title("🌟 AUREX ATTEND - AI SYSTEM")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="neon-card"><h3>📸 SCANNER</h3><p>Mark Attendance</p></div>', unsafe_allow_html=True)
        if st.button("🚀 START SCANNING"):
            st.session_state.page = "📸 Live Scanner"; st.rerun()
    with col2:
        st.markdown('<div class="neon-card"><h3>📝 REGISTER</h3><p>Add Student</p></div>', unsafe_allow_html=True)
        if st.button("➕ ADD NEW ENTRY"):
            st.session_state.page = "📝 Registration"; st.rerun()
    with col3:
        st.markdown('<div class="neon-card"><h3>📊 RECORDS</h3><p>View Database</p></div>', unsafe_allow_html=True)
        if st.button("📂 VIEW RECORDS"):
            st.session_state.page = "📊 Records"; st.rerun()

elif st.session_state.page == "📝 Registration":
    st.title("📝 Student Registration")
    if st.button("⬅️ Back to Home"): st.session_state.page = "🏠 Home"; st.rerun()
    
    name = st.text_input("Enter Student Full Name")
    uploaded_file = st.file_uploader("Upload Profile Photo", type=['jpg', 'png', 'jpeg'])
    
    if st.button("✅ SAVE REGISTRATION"):
        if name and uploaded_file:
            img = Image.open(uploaded_file)
            img.save(f"img/{name}.jpg") # Image save logic
            st.success(f"Student '{name}' has been registered successfully!")
            st.balloons()
        else:
            st.error("Please provide both Name and Photo.")

elif st.session_state.page == "📸 Live Scanner":
    st.title("📸 AI Facial Recognition")
    if st.button("⬅️ Back to Home"): st.session_state.page = "🏠 Home"; st.rerun()
    
    # Check if database is empty
    if not os.listdir('img'):
        st.warning("⚠️ Database is empty. Please register a student first.")
    else:
        img_file = st.camera_input("Scanner Active - Look at the camera")
        
        if img_file:
            with st.spinner("Processing face..."):
                # 1. Load database encodings
                known_encodings, known_names = load_known_faces()
                
                # 2. Process captured image
                test_img = Image.open(img_file)
                test_img = np.array(test_img)
                test_img_rgb = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)
                
                # 3. Find faces in current frame
                faces_cur_frame = face_recognition.face_locations(test_img_rgb)
                encodes_cur_frame = face_recognition.face_encodings(test_img_rgb, faces_cur_frame)
                
                found = False
                for encodeFace in encodes_cur_frame:
                    matches = face_recognition.compare_faces(known_encodings, encodeFace)
                    faceDis = face_recognition.face_distance(known_encodings, encodeFace)
                    
                    if len(faceDis) >
