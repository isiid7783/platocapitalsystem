import streamlit as st
import pandas as pd
import os
from datetime import datetime
from config import PASSWORD, DATA_FILE, REPORT_FOLDER
from modules.analytics import compute_metrics
from modules.llm import generate_analysis
from modules.pdf_report import generate_pdf

st.set_page_config(page_title="Plato Capital System", layout="wide")

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    pwd = st.text_input("Access Key", type="password")
    if pwd == PASSWORD:
        st.session_state.auth = True
    else:
        st.stop()

st.title("Plato Capital System")
st.caption("Log. Analyze. Recalibrate.")

with st.form("decision_form"):
    decision = st.text_input("Decision")
    capital = st.number_input("Capital", value=0.0)
    expected_return = st.number_input("Expected Return (%)", value=0.0)
    actual_return = st.number_input("Actual Return (%)", value=0.0)
    confidence = st.slider("Confidence", 1, 10, 5)
    time_spent = st.number_input("Time Spent (hours)", value=0.0)

    if st.form_submit_button("Save"):
        new_row = pd.DataFrame([{
            "timestamp": datetime.now(),
            "decision": decision,
            "capital": capital,
            "expected_return": expected_return,
            "actual_return": actual_return,
            "confidence": confidence,
            "time_spent": time_spent
        }])

        if os.path.exists(DATA_FILE):
            new_row.to_csv(DATA_FILE, mode='a', header=False, index=False)
        else:
            new_row.to_csv(DATA_FILE, index=False)

        st.success("Logged.")

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    st.dataframe(df)

    metrics = compute_metrics(df)

    st.metric("Average Return", round(metrics["avg_return"], 2))
    st.metric("Success Rate (%)", round(metrics["success_rate"], 2))
    st.metric("Confidence Corr.", round(metrics["confidence_corr"], 2))
    st.metric("Time Corr.", round(metrics["time_corr"], 2))

    if st.button("Generate AI Analysis"):
        analysis = generate_analysis(metrics)
        st.write(analysis)

    if st.button("Generate PDF Report"):
        if not os.path.exists(REPORT_FOLDER):
            os.makedirs(REPORT_FOLDER)
        file_path = generate_pdf(metrics, REPORT_FOLDER)
        with open(file_path, "rb") as f:
            st.download_button("Download Report", f, file_name=file_path)

