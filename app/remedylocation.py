import streamlit as st
import folium
import pandas as pd
import os
from streamlit_folium import folium_static

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

#Create sample CSV if it doesn't exist
def create_sample_csv(file_path):
    if not os.path.exists(file_path):
        data = [
            {"type": "pesticide", "name": "Active Pest Control", "latitude": 27.7172, "longitude": 85.3240, "rating": "⭐ 4.9", "hours": "Open 24h"},
            {"type": "pesticide", "name": "Pest Defence Service", "latitude": 27.7150, "longitude": 85.3200, "rating": "⭐ 4.9", "hours": "Open 24h"},
            {"type": "pesticide", "name": "Orange Ball Pvt. Ltd.", "latitude": 27.7200, "longitude": 85.3300, "rating": "⭐ 4.9", "hours": "Open 24h"},
            {"type": "pesticide", "name": "City Pest Control", "latitude": 27.7250, "longitude": 85.3350, "rating": "⭐ 5.0", "hours": "Open 24h"},
            {"type": "nursery", "name": "Kathmandu Nursery", "latitude": 27.7180, "longitude": 85.3260, "rating": "⭐ 4.0", "hours": "Opens 6 AM"},
            {"type": "nursery", "name": "Royal Nursery", "latitude": 27.7210, "longitude": 85.3280, "rating": "⭐ 4.5", "hours": "Opens 7 AM"},
            {"type": "nursery", "name": "Standard Nursery", "latitude": 27.7230, "longitude": 85.3300, "rating": "⭐ 4.1", "hours": "Opens 9 AM"},
            {"type": "nursery", "name": "Swoyambhu Garden Service", "latitude": 27.7260, "longitude": 85.3320, "rating": "⭐ 4.7", "hours": "Opens 7 AM"},
        ]
        df = pd.DataFrame(data)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)

# Main app
def remedylocation():
    st.markdown("""
        <style>
        .button-style {
            display: inline-block;
            padding: 0.75em 1.5em;
            margin: 1em 0;
            font-size: 1.1em;
            font-weight: bold;
            color: white;
            background: linear-gradient(135deg, #4CAF50, #2E7D32);
            border: none;
            border-radius: 8px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .button-style:hover {
            background: linear-gradient(135deg, #66BB6A, #388E3C);
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }
        .caption {
            font-size: 1.5em;
            font-weight: 600;
            margin-top: 1em;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Remedial Sites Nearby🌿🪴🐞📍")

    central_lat = 27.7172
    central_lon = 85.3240

    file_path = os.path.join(root_dir,"Component_datasets","locations.csv")
    create_sample_csv(file_path)

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error loading location data: {e}")
        return

    col1, col2 = st.columns(2)
    with col1:
        if st.markdown('<div class="button-style">🧪 Pesticide Stores Near Me</div>', unsafe_allow_html=True):
            show_map(df[df["type"] == "pesticide"], central_lat, central_lon, "red", "info-sign", "Pesticide Stores")

    with col2:
        if st.markdown('<div class="button-style">🌱 Plant Nurseries Near Me</div>', unsafe_allow_html=True):
            show_map(df[df["type"] == "nursery"], central_lat, central_lon, "green", "leaf", "Plant Nurseries")

#Map rendering
def show_map(data, lat, lon, color, icon, title):
    st.markdown(f"<h2 class='caption'>Nearby {title}</h2>", unsafe_allow_html=True)
    m = folium.Map(location=[lat, lon], zoom_start=13)

    for _, row in data.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=f"<b>{row['name']}</b><br>{row['rating']}<br>{row['hours']}",
            tooltip=f"{row['name']} ({row['rating']})",
            icon=folium.Icon(color=color, icon=icon)
        ).add_to(m)

    folium_static(m)

#Run the app
if __name__ == "__main__":
    remedylocation()