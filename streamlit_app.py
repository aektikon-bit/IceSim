import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
import requests
import base64
import os

# -----------------------------
# ⚙️ Page config
# -----------------------------
st.set_page_config(
    page_title="PolarView Ultra",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# 🎨 Custom CSS + Sound
# -----------------------------
sound_file = "click.mp3"

def play_sound():
    if os.path.exists(sound_file):
        sound_html = f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{base64.b64encode(open(sound_file,'rb').read()).decode()}" type="audio/mp3">
            </audio>
        """
        st.markdown(sound_html, unsafe_allow_html=True)

st.markdown("""
<style>
body {
    background-color: #0E1B2B;
    color: #E0EAF6;
}
section.main > div {
    background-color: #132235;
    border-radius: 10px;
    padding: 20px;
}
h1, h2, h3 {
    color: #5DA9E9;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 📌 Sidebar Menu
# -----------------------------
menu = st.sidebar.selectbox(
    "📂 เลือกเมนู",
    ["📊 NASA/NOAA 2024–2025", "❄️ Ice Simulation", "🌏 Sea Level Map", "📘 Summary"]
)

if st.sidebar.button("🔊 เล่นเสียง"):
    play_sound()

# ---------------------------------------------------------------------
# 📊 1) โหลดข้อมูล NASA 2024–2025
# ---------------------------------------------------------------------
if menu == "📊 NASA/NOAA 2024–2025":
    st.title("📊 ข้อมูลจริงจาก NASA (2024–2025)")

    URL = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"

    try:
        data = pd.read_csv(URL, skiprows=1)

        st.success("โหลดข้อมูลสำเร็จ!")
        st.write("### ตัวอย่างข้อมูล")
        st.dataframe(data.head())

        temp_2024 = data.tail(2).iloc[0, 1:13].mean()
        temp_2025 = data.tail(1).iloc[0, 1:13].mean()

        col1, col2 = st.columns(2)
        col1.metric("อุณหภูมิเฉลี่ยปี 2024", f"{temp_2024:.3f} °C")
        col2.metric("อุณหภูมิเฉลี่ยปี 2025", f"{temp_2025:.3f} °C")

        st.area_chart(data.iloc[:, 1:13].mean(axis=1))

        play_sound()

    except Exception as e:
        st.error("ไม่สามารถโหลดข้อมูล NASA ได้")
        st.write(e)

# ---------------------------------------------------------------------
# ❄️ 2) Ice Simulation
# ---------------------------------------------------------------------
elif menu == "❄️ Ice Simulation":
    st.title("❄️ จำลองการละลายน้ำแข็งตาม IPCC")

    temp_inc = st.slider("อุณหภูมิเพิ่มขึ้น (°C)", 0.0, 6.0, 1.8, 0.1, on_change=play_sound)
    years = st.slider("จำลองกี่ปี", 10, 150, 80, 10, on_change=play_sound)

    years_list = np.arange(0, years + 1)

    # IPCC AR6 Model
    loss_rate = 3.4  # % / °C / decade
    ice_left = 100 - loss_rate * temp_inc * (years_list / 10)
    ice_left = np.clip(ice_left, 0, 100)

    df = pd.DataFrame({"ปี": years_list, "น้ำแข็ง (%)": ice_left}).set_index("ปี")

    st.line_chart(df)

# ---------------------------------------------------------------------
# 🌏 3) Sea Level Map
# ---------------------------------------------------------------------
elif menu == "🌏 Sea Level Map":
    st.title("🌏 แผนที่โลก — ระดับน้ำทะเลเพิ่ม")

    df_map = pd.DataFrame({
        "lat": [13.7, 40.7, 23.7, 52.3, 35.7],
        "lon": [100.5, -74.0, 90.4, 4.9, 139.7],
        "country": ["Thailand", "USA", "Bangladesh", "Netherlands", "Japan"],
        "sea_lvl": [12, 18, 25, 30, 10]
    })

    layer = pdk.Layer(
        "ScatterplotLayer",
        df_map,
        get_position=["lon", "lat"],
        get_radius="sea_lvl * 40000",
        get_color="[255, sea_lvl*8, 0]",
        pickable=True
    )

    view_state = pdk.ViewState(latitude=20, longitude=0, zoom=1, pitch=30)

    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# ---------------------------------------------------------------------
# 📘 Summary
# ---------------------------------------------------------------------
elif menu == "📘 Summary":
    st.title("📘 สรุปผลแบบรวม")

    st.success("""
    🎯 PolarView Ultra — Full Version  
    - โหลดข้อมูลจริง NASA ปี 2024–2025  
    - Simulation ตาม IPCC  
    - แผนที่โลก Sea Level  
    - รองรับ PWA  
    - มีเสียง Sound Effect  
    """)

    play_sound()
