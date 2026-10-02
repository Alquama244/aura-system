import streamlit as st
import sqlite3
import json
import pandas as pd
from PIL import Image
from detector import ObjectDetector
from ai_engine import AIEngine
from report_generator import generate_excel, generate_pdf

st.set_page_config(page_title="AURA - Visual Automation & Inventory", layout="wide")

# Main Header Title
st.title("AURA: Autonomous Unified Reasoning & Automation")
st.caption("Transforming visual information into structured inventory data using YOLO Computer Vision & Gemini AI.")
st.markdown("---")

@st.cache_resource
def load_detector():
    return ObjectDetector()

@st.cache_resource
def load_ai_engine():
    return AIEngine()

detector = load_detector()
ai_engine = load_ai_engine()

# Sidebar Control Panel
st.sidebar.title("Control Panel")
uploaded_file = st.sidebar.file_uploader("Upload an Image for Analysis", type=["jpg", "jpeg", "png"])

st.sidebar.markdown("---")
navigation = st.sidebar.radio("Navigation", ["Live Analysis", "Analysis History"])

if navigation == "Live Analysis":
    if uploaded_file is not None:
        raw_image = Image.open(uploaded_file)
        
        # 1. Computer Vision Detection
        annotated_img, object_counts = detector.detect_and_count(raw_image)
        
        # 2. Generative AI Narrative Generation
        with st.spinner("Generating Gemini AI Inventory Analysis..."):
            ai_analysis = ai_engine.generate_inventory_analysis(object_counts)

        # 3. Two-column layout
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("YOLO Bounding Box Detection")
            st.image(annotated_img, use_container_width=True)

        with col2:
            st.subheader("Structured Object Counts")
            st.json(object_counts)

            st.subheader("AI Narrative Analysis")
            st.markdown(ai_analysis)

            # 4. Save to Database
            conn = sqlite3.connect("aura_inventory.db")
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    object_counts TEXT,
                    ai_analysis TEXT
                )
            """)
            cursor.execute(
                "INSERT INTO scans (object_counts, ai_analysis) VALUES (?, ?)",
                (json.dumps(object_counts), ai_analysis)
            )
            conn.commit()
            scan_id = cursor.lastrowid
            conn.close()

            # 5. Export Buttons
            excel_bytes = generate_excel(object_counts, ai_analysis)
            pdf_bytes = generate_pdf(object_counts, ai_analysis)

            dcol1, dcol2 = st.columns(2)
            with dcol1:
                st.download_button("📥 Download Excel Report", data=excel_bytes, file_name=f"aura_report_{scan_id}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            with dcol2:
                st.download_button("📥 Download PDF Report", data=pdf_bytes, file_name=f"aura_report_{scan_id}.pdf", mime="application/pdf")
    else:
        st.info("👈 Please upload an image using the sidebar Control Panel to begin analysis.")

elif navigation == "Analysis History":
    st.subheader("Scan History & Logs")
    conn = sqlite3.connect("aura_inventory.db")
    df = pd.read_sql_query("SELECT * FROM scans ORDER BY id DESC", conn)
    conn.close()

    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No scans found in database yet.")
