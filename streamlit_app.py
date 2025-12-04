import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import time

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="PolarView Ultra Ultimate",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
body { background-color:#0E1B2B; color:#E0EAF6; }
section.main > div { background-color:#132235; border-radius:10px; padding:20px; }
h1,h2,h3 { color:#5DA9E9; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar menu
# -----------------------------
menu = st.sidebar.selectbox(
    "📂 เลือกเมนู",
    ["📊 NASA/NOAA 2024–2025", "❄️ Ice Simulation", "🌏 Sea Level Map", "🌍 3D Globe Ultimate", "📘 Summary"]
)

# -----------------------------
# 1) NASA/NOAA 2024–2025
# -----------------------------
if menu == "📊 NASA/NOAA 2024–2025":
    st.title("📊 ข้อมูลจริง NASA 2024–2025")
    try:
        URL = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
        data = pd.read_csv(URL, skiprows=1)
        temp_2024 = data.tail(2).iloc[0, 1:13].mean()
        temp_2025 = data.tail(1).iloc[0, 1:13].mean()
        col1, col2 = st.columns(2)
        col1.metric("🌡️ 2024", f"{temp_2024:.3f} °C")
        col2.metric("🌡️ 2025", f"{temp_2025:.3f} °C")
        st.dataframe(data.tail(5))
        st.line_chart(data.iloc[:, 1:13].mean(axis=1))
    except Exception as e:
        st.error("❌ โหลดข้อมูล NASA ไม่สำเร็จ")
        st.write(e)

# -----------------------------
# 2) Ice Simulation
# -----------------------------
elif menu == "❄️ Ice Simulation":
    st.title("❄️ จำลองการละลายน้ำแข็ง IPCC")
    temp_inc = st.slider("อุณหภูมิเพิ่มขึ้น (°C)",0.0,6.0,1.8,0.1)
    years = st.slider("จำลองกี่ปี",10,150,80,10)
    years_list = np.arange(0,years+1)
    loss_rate = 3.4
    ice_left = 100 - loss_rate*temp_inc*(years_list/10)
    ice_left = np.clip(ice_left,0,100)
    df = pd.DataFrame({"ปี":years_list,"น้ำแข็ง (%)":ice_left}).set_index("ปี")
    st.line_chart(df)

# -----------------------------
# 3) Sea Level Map
# -----------------------------
elif menu == "🌏 Sea Level Map":
    st.title("🌏 แผนที่โลก — ระดับน้ำทะเลเพิ่ม")
    df_map = pd.DataFrame({
        "lat": [13.7, 40.7, 23.7, 52.3, 35.7],
        "lon": [100.5, -74.0, 90.4, 4.9, 139.7],
        "country": ["Thailand","USA","Bangladesh","Netherlands","Japan"],
        "sea_lvl": [12,18,25,30,10]
    })
    layer = pdk.Layer(
        "ScatterplotLayer", df_map,
        get_position=["lon","lat"],
        get_radius="sea_lvl*40000",
        get_color="[255, sea_lvl*8, 0]",
        pickable=True
    )
    view_state = pdk.ViewState(latitude=20, longitude=0, zoom=1, pitch=30)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# -----------------------------
# 4) 3D Globe Ultimate
# -----------------------------
elif menu == "🌍 3D Globe Ultimate":
    st.title("🌍 3D โลกหมุนได้ — Ultimate View")
    st.write("🌐 จุดเมือง 1000+ + Ice Dome + Slider หมุน Globe + NASA 2024–2025")

    # สุ่ม 1000 จุดเมือง
    np.random.seed(42)
    lats = np.random.uniform(-60,80,1000)
    lons = np.random.uniform(-180,180,1000)
    temps = np.random.uniform(-2,5,1000)
    df_points = pd.DataFrame({"lat":lats,"lon":lons,"temp":temps})

    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        df_points,
        get_position=["lon","lat"],
        get_radius=20000,
        get_fill_color="[255, int((temp+2)*25), 50]",
        pickable=True
    )

    ice_layer = pdk.Layer(
        "PolygonLayer",
        [
            {"polygon":[[-180,80],[180,80],[180,90],[-180,90]]},   # North Pole
            {"polygon":[[-180,-90],[180,-90],[180,-80],[-180,-80]]} # South Pole
        ],
        get_fill_color=[173,216,230,150],
        stroked=False
    )

    # Slider ให้หมุน Globe
    lon = st.slider("หมุน Globe (Longitude)", -180, 180, 0)
    view_state = pdk.ViewState(latitude=0, longitude=lon, zoom=0.5, pitch=45)

    deck = pdk.Deck(
        layers=[scatter_layer, ice_layer],
        initial_view_state=view_state,
        map_style=None
    )
    st.pydeck_chart(deck)

# -----------------------------
# 5) Summary
# -----------------------------
elif menu == "📘 Summary":
    st.title("📘 สรุป PolarView Ultra Ultimate")
    st.success("""
    🎯 ฟีเจอร์ครบ:
    - NASA 2024–2025
    - Ice Simulation
    - Sea Level Map
    - 3D Globe Ultimate (หมุนด้วย Slider)
    - Sidebar + Custom Theme
    """)
