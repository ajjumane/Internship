import streamlit as st
from PIL import Image
import base64
import io
import json
import os

# 1. Page Configuration
st.set_page_config(page_title="Ajinkya - Login form", page_icon="👤", layout="centered")

# --- DATABASE LOGIC (PERMANENT STORAGE) ---
DB_FILE = "users_db.json"

def load_users():
    """Loads users from a JSON file. Creates one if it doesn't exist."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"admin": "admin123"}  # Initial default user

def save_user(username, password):
    """Appends a new user to the JSON file."""
    users = load_users()
    users[username] = password
    with open(DB_FILE, "w") as f:
        json.dump(users, f)

# Load existing users at startup
users = load_users()

# --- HELPER: IMAGE PROCESSING ---
def get_base64_image(img_path):
    try:
        img = Image.open(img_path)
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()
    except:
        return ""

# 2. CSS STYLING (Blue Sidebar + Black/Blue UI + Animated BG)
st.markdown(f"""
    <style>
    /* Animated Gradient Background */
    .stApp {{
        background: linear-gradient(-45deg, #000000, #0E1117, #1b2735, #000000);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }}
    @keyframes gradient {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: #1F538D !important;
    }}
    
    /* Main Content Headers */
    h2 {{ color: white !important; font-family: 'Segoe UI', sans-serif; }}
    
    /* Input & Button Styling */
    .stButton>button {{
        background-color: #1F538D !important;
        color: white !important;
        width: 100%;
        border-radius: 5px;
        border: none;
        height: 45px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR: Branding and Mode Selection
with st.sidebar:
    pfp_data = get_base64_image("pfp.jpg")
    if pfp_data:
        st.markdown(f"""
            <div style="text-align: center;">
                <img src="data:image/jpeg;base64,{pfp_data}" 
                style="width: 120px; height: 120px; border-radius: 15px; border: 2px solid white; margin-bottom: 15px;">
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; color: white;'>Ajinkya - Login form</h3>", unsafe_allow_html=True)
    st.markdown("---")
    mode = st.sidebar.radio("CHOOSE ACTION", ["LOGIN", "REGISTER"])
    st.markdown("---")
    st.caption("Permanent Database Enabled")

# 4. MAIN CONTENT AREA: Fields Only
if mode == "LOGIN":
    st.markdown("## Account Login")
    user_input = st.text_input("USERNAME")
    pass_input = st.text_input("PASSWORD", type="password")
    
    if st.button("SIGN IN"):
        if user_input in users and users[user_input] == pass_input:
            st.success(f"Welcome back, {user_input}!")
            st.balloons()
        else:
            st.error("Invalid Username or Password")

elif mode == "REGISTER":
    st.markdown("## Create Account")
    new_user = st.text_input("NEW USERNAME")
    new_pass = st.text_input("NEW PASSWORD", type="password")
    confirm_pass = st.text_input("CONFIRM PASSWORD", type="password")
    
    if st.button("REGISTER"):
        if new_user in users:
            st.warning("Username already taken.")
        elif new_pass != confirm_pass:
            st.error("Passwords do not match.")
        elif new_user and new_pass:
            save_user(new_user, new_pass)
            st.success("Registration Successful! You can now login.")
        else:
            st.error("Fields cannot be empty.")