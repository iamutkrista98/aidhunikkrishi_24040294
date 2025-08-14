import streamlit as st
import folium
import pandas as pd
import os
from folium.plugins import MarkerCluster
import streamlit.components.v1 as components
from branca.element import Template, MacroElement

# Root directory
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Create sample CSV if it doesn't exist
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

# Map rendering with geolocation
def show_map(data, lat, lon, color, icon, title):
    m = folium.Map(location=[lat, lon], zoom_start=14, tiles="CartoDB positron")
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in data.iterrows():
        popup_html = f"""
        <b>{row['name']}</b><br>
        {row['rating']}<br>
        <i>{row['hours']}</i>
        """
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=popup_html,
            tooltip=f"{row['name']} ({row['rating']})",
            icon=folium.Icon(color=color, icon=icon, prefix='glyphicon')
        ).add_to(marker_cluster)

    # Inject geolocation JS
    geolocation_js = """
    {% macro script(this, kwargs) %}
    navigator.geolocation.getCurrentPosition(function(location) {
        var latlng = L.latLng(location.coords.latitude, location.coords.longitude);
        L.marker(latlng, {
            icon: L.icon({
                iconUrl: 'https://cdn-icons-png.flaticon.com/512/64/64113.png',
                iconSize: [30, 30],
                iconAnchor: [15, 30],
                popupAnchor: [0, -30]
            }),
            title: "Your Location"
        }).bindPopup("📍 You are here").addTo({{this._parent.get_name()}});
    });
    {% endmacro %}
    """
    macro = MacroElement()
    macro._template = Template(geolocation_js)
    m.get_root().add_child(macro)

    folium.LayerControl().add_to(m)

    # Render map as raw HTML
    map_html = m.get_root().render()
    components.html(map_html, height=600, width=1200)

# Main app
def remedylocation():
    st.set_page_config(layout="centered")
    st.title("Remedial Sites Nearby 🌿🐞📍")

    central_lat = 27.7172
    central_lon = 85.3240

    file_path = os.path.join(root_dir, "Component_datasets", "locations.csv")
    create_sample_csv(file_path)

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error loading location data: {e}")
        return

    # Section 1: Pesticide Stores
    st.markdown("## 🧪 Pesticide Stores Nearby")
    show_map(df[df["type"] == "pesticide"], central_lat, central_lon, "red", "info-sign", "Pesticide Stores")

    st.markdown("---")

    # Section 2: Plant Nurseries
    st.markdown("## 🌱 Plant Nurseries Nearby")
    show_map(df[df["type"] == "nursery"], central_lat, central_lon, "green", "leaf", "Plant Nurseries")

# Run the app
if __name__ == "__main__":
    remedylocation()