import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import streamlit.components.v1 as components
from Login import create_login_page
from SignUp import create_sign_up_page
from Continuous_Learning_and_Feedback import *
from remedylocation import *
from Login import *
from apiintegration import *
import os
import bcrypt
import json
from datetime import datetime

SESSION_FILE = "session.json"

# Function to load session state from JSON
def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    return {}

# Function to save session state to JSON
def save_session():
    session_data = {
        "isLoggedIn": st.session_state.isLoggedIn,
        "user": st.session_state.user,
        "selected": st.session_state.selected,
        "selectedIndex": st.session_state.selectedIndex,
        "users": st.session_state.users,
    }
    with open(SESSION_FILE, "w") as f:
        json.dump(session_data, f, indent=4)

# Load session state from JSON
session_data = load_session()

# Initialize session state variables
if "isLoggedIn" not in st.session_state:
    st.session_state.isLoggedIn = session_data.get("isLoggedIn", False)

if "user" not in st.session_state:
     hashed_password = bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
     st.session_state.user = session_data.get("user",  None)

if "users" not in st.session_state:
    st.session_state.users = session_data.get('users', [{
        "username": "admin",
        "password": hashed_password,
        "email": "admin@gmail.com",
        "phone_number": "98453354534"
    }])

if "selected" not in st.session_state:
    st.session_state.selected = session_data.get("selected", "Home")

if "selectedIndex" not in st.session_state:
    st.session_state.selectedIndex = session_data.get("selectedIndex", 0)

# Function to update session and save it
def update_session(key, value):
    st.session_state[key] = value
    save_session()  # Save updates immediately

save_session()

# Determine the root directory of the project
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Custom Styling for the Entire App
st.markdown(
    """
    <style>
        .stAppHeader {
            top: 0;
            left: 0;
            width: 100%;
            background: #DC143C;
            padding: 1rem;
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
            box-shadow: 0px -18px 20px 1px;
            z-index: 1000;
            transition: background 0.3s ease, opacity 0.3s ease;
        } 
        .stAppHeader.scrolled {
            background: rgba(255, 255, 255, 0.9); /* Slightly transparent */
            opacity: 0.9;
        }

        /* Adjust Main Content Padding to Avoid Overlap with Header */
        .main-content {
            padding-top: 6rem; /* Add space for the fixed header */
        }
        .stButton>button {
            background: linear-gradient(135deg, #1e3a5f, #2a5298);
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px 20px;
            border: none;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
        }
        .main-content {
            padding: 2rem;
            background: rgba(255, 255, 255, 0.1);
            background-image: url("{bg_image}");
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            margin: 1rem;
        }
        .stImage img {
            border-radius: 12px;
        }

        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: rgb(255, 255, 255)!important;
        }

        /* Sidebar Styling */
        .sidebar .sidebar-content {
            background: linear-gradient(135deg, #1e3a5f, #008080);
            color: white;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }
        .css-1d391kg {
            background: linear-gradient(135deg, #1e3a5f, #008080);
        }

        /* Home Page Styling */
        .hero {
            background: linear-gradient(135deg, #1e3a5f, #032030);
            padding: 4rem 2rem;
            border-radius: 20px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }
        .feature-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
        }
        .cta-button {
            background: linear-gradient(135deg, #1e3a5f, #008080);
            color: white !important;
            padding: 1rem 2rem !important;
            border-radius: 12px !important;
            font-size: 1.1rem !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            text-decoration:none !important;
        }
        .cta-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
        }
        .footer {
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
            color:rgb(39, 36, 36);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

url_mappings = [
    "Home",
    "Leaf Disease Identification",
    "Continuous Learning",
    "Import Data",
    "Remedial Sites"
]
icon_mappings = [
    "house-fill", "cpu-fill", "chat-right-text-fill",
    "cloud-download-fill","pin-map-fill", "shield-fill", "person-fill",
    "book-fill",  # Icon for Import Data 

]

# Ensure "Login" and "Sign Up" are added only when the user is not logged in
if not st.session_state.isLoggedIn:
    url_mappings.extend(["Login", "Sign Up"])
    icon_mappings.extend(['lock-fill', 'person-fill'])
else:
    url_mappings.extend(['Logout'])
    icon_mappings.extend(['lock-fill'])

# Always keep "Documentation" at the end
url_mappings.append("Documentation")
icon_mappings.append("file-earmark-text")

# Read query parameters and update session state only if it hasn't been set
query_params = st.query_params  # Get query parameters
if "page" in query_params:
    qPage = query_params["page"]
    if qPage != st.session_state.selected:
        update_session('selected', qPage)
        qPageIndex = url_mappings.index(qPage)
        update_session('selectedIndex', qPageIndex)

# Sidebar Menu
with st.sidebar:
    if st.session_state.isLoggedIn:
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <span style="font-size: 18px; margin-right: 10px;">👤</span>
            <span style="font-size: 16px; font-weight: bold;">{st.session_state.user['username']}</span>
        </div>
        """, unsafe_allow_html=True)

    page = option_menu(
        "AiDHUNIK KRISHI",
        options=url_mappings,
        icons=icon_mappings,
        default_index=st.session_state.selectedIndex,
        menu_icon="layout-text-window-reverse",
        orientation="vertical",
        styles={
            "container": {
                "padding": "10px",
                "background": "linear-gradient(135deg, #1e3a5f, #032030)",
                "box-shadow": "0px 4px 15px rgba(0, 0, 0, 0.3)",
                "border-radius": "12px"
            },
            "menu-title": {
                "font-size": "22px",
                "font-weight": "bold",
                "color": "#ffffff",
                "margin-left": "0px !important",
                "margin-right": "0px !important",
                "padding": "5px",
            },
            "nav-link": {
                "text-decoration": "none",
                "color": "#ffffff",
                "font-size": "16px",
                "padding": "10px",
                "border-radius": "8px",
                "transition": "all 0.3s ease-in-out"
            },
            "nav-link-selected": {
                "background": "rgba(255, 255, 255, 0.2)",
                "color": "#ffffff",
                "font-weight": "bold",
                "border-radius": "8px"
            },
            "icon": {
                "color": "#ffffff",
                "font-size": "20px"
            },
        }
    )

    # Update session state only if the user explicitly selects a page from the sidebar
    if page != st.session_state.selected:
        update_session('selected', page)

# Optional: Update URL to reflect selected page
st.query_params['page'] = st.session_state.selected

# Home Page Content
if st.session_state.selected == "Home":
    # Hero Section
    st.markdown("""
    <div class="hero">
        <h1 style="font-size: 2.8rem; margin-bottom: 1rem;">AiDHUNIK KRISHI:  An Advanced CNN Based Plant Leaf Disease Classification Platform</h1>
        <h3 style="font-weight: 300; margin-bottom: 2rem;">Empowering Stakeholders in Agricultural Sector</h3>
        <div style="display: flex; gap: 1rem; justify-content: center;">
            <a href="#features" class="cta-button">Explore Features</a>
            <a href="#learn-more" class="cta-button">Learn More</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Image + Text Section
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown("""
        ## About The Platform
        AiDHUNIK KRISHI is an advanced CNN-based plant leaf disease classification platform designed to enhance agricultural productivity and public health through advanced analytics. Our platform empowers farmers, researchers, and government agencies with accurate, real-time insights into plant health, aiding in early disease detection and mitigation strategies. This project aims to revolutionize agricultural practices by integrating cutting-edge machine learning to foster sustainable growth and improve crop yields globally. We combine deep learning models with extensive agricultural data to provide unparalleled precision in disease identification, offering a critical tool for informed decision-making in the agricultural sector.
        """)

    if st.button("Get Started →", key="hero_button"):
        st.session_state["selected_page"] = "Documentation"

    with col2:
        data_file_path = os.path.join(root_dir, 'assets', 'projectlogo1.png')
        if os.path.exists(data_file_path):
            st.image(data_file_path, use_container_width=True,
                     caption="AiDHUNIK KRISHI:  An Advanced CNN Based Plant Leaf Disease Classification Platform")
        else:
            st.warning("Image not found: projectlogo1.png")

    # Features Section
    st.markdown('<a name="features"></a>', unsafe_allow_html=True)
    st.markdown("""
    ## 🔍Our Key Features
    Integrated solutions tailored for Nepal's security landscape
    """)

    # Feature Cards
    features = [
        {
            "icon": "👨‍🌾",
            "title": "Companion Application",
            "desc": "An AI Based Companion for Stakeholders in the field of Agriculture"
        },
        {
            "icon": "🔮",
            "title": "CNN Based Plant Leaf Disease Classification",
            "desc": "CNN Powered Plant Leaf Disease Identification"
        },
        {
            "icon": "🔄",
            "title": "Continuous Learning",
            "desc": "Real-time feedback integration and adaptive learning systems"
        },
        {
            "icon": "🔗",
            "title": "Handling of API",
            "desc": "Integration Possibilities within preexisting system through API Endpoint Enablement"
        },
    ]

    cols = st.columns(2)
    for idx, feature in enumerate(features):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{feature['icon']}</div>
                <h3>{feature['title']}</h3>
                <p>{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    # Get the current year
    current_year = datetime.now().year
    # Footer HTML with dynamic year and theme-based text color
    st.markdown(f"""
    <div class="footer">
        <hr style="margin: 2rem 0; color:white;">
        <p style="font-size: 0.9rem;color:white;">
            © AiDHUNIK KRISHI by Utkrista Acharya {current_year} | 
            <a href="/" style="color:white;text-decoration: none;">Privacy Policy</a> | 
            <a href="/" style="color:white;text-decoration: none;">Contact</a>
        </p>
    </div>
    """, unsafe_allow_html=True)


if st.session_state.selected == "Continuous Learning":
    continuous_learning_and_feedback()

if st.session_state.selected == "Remedial Sites":
    remedylocation()

if st.session_state.selected == 'Login':
    create_login_page(update_session)

if st.session_state.selected == 'Sign Up':
    create_sign_up_page(update_session=update_session)

if st.session_state.selected == 'Logout':
    update_session('isLoggedIn', False)
    update_session('user', [])



if st.session_state.selected == "Import Data":
    # if not st.session_state.isLoggedIn:
    #     st.warning("Please login to access this page.")
    #     update_session('selected', 'Home')
    # else:  
    import_data_from_api(update_session)

if st.session_state.selected == "Documentation":
    # Set page header
    st.header("📚 Documentation & Resources", divider="rainbow")
    st.subheader("Access project materials and technical resources")




    # Main content container
    with st.container():
        # Documentation Card with enhanced styling
        st.markdown("""
        <div style='background-color: #f0f2f6; padding: 2rem; border-radius: 10px; margin: 1rem 0;'>
            <h4 style='color: #2c3e50; margin-bottom: 1rem;'>📘 Project Documentation</h4>
            <p style='color: #34495e; margin-bottom: 1.5rem;'>
                Access comprehensive documentation including system architecture, 
                API references, and user guides.
            </p>
            <a href='https://github.com/iamutkrista98/MScProject/blob/main/README.md' 
               target='_blank' 
               style='background-color: #4a90e2; 
                      color: white; 
                      padding: 0.5rem 1.5rem; 
                      border-radius: 5px; 
                      text-decoration: none;
                      transition: all 0.3s ease;'
               onmouseover="this.style.backgroundColor='#357abd'" 
               onmouseout="this.style.backgroundColor='#4a90e2'">
                View Documentation
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    # Optional Resources Toggle
    show_resources = st.checkbox("🚀 Show support options", value=False)
            
    if show_resources:
    # Support Section
        with st.expander("🆘 Application Support Center", expanded=False):
            st.markdown("""
            <div style='columns: 2; gap: 2rem; padding: 1rem;'>
                <div>
                    <h4 style='color: #ff4b4b; margin-bottom: 0.5rem;'>Emergency Support</h4>
                    <p style='margin: 0.5rem 0;'>
                        📞 <strong>24/7 Hotline:</strong> +977-1 xxxxxxx<br>
                        📧 <code>aidhunikkheti@gmail.com</code>
                    </p>
                </div>
                <div>
                    <h4 style='color: #4a90e2; margin-bottom: 0.5rem;'>Regular Support</h4>
                    <p style='margin: 0.5rem 0;'>
                        ⏰ Mon-Fri 9AM-5PM <br>
                        📞 +977-1 xxxxxxx<br>
                        📧 <code>aidhunikkheti@gmail.com</code>
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Version Info
    st.markdown("---")
    st.caption("Current Version: 1.0.1 | Last Updated: August 12, 2025")
