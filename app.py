import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

from config import PASSWORD, DATA_FILE, REPORT_FOLDER
from modules.analytics import compute_metrics
from modules.llm import generate_analysis
from modules.pdf_report import generate_pdf

st.set_page_config(page_title="Plato Capital System", layout="wide")

# ---------- Authentication ----------

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password_input = st.text_input("Access Key", type="password")
    if password_input == PASSWORD:
        st.session_state.authenticated = True
    else:
        st.stop()

st.title("Plato Capital System")
st.caption("Log. Analyze. Recalibrate.")

# ---------- Decision Input ----------

st.header("Log Capital Decision")

with st.form("decision_form"):
    decision = st.text_input("Decision Description")
    capital = st.number_input("Capital Allocated", value=0.0)
    expected_return = st.number_input("Expected Return (%)", value=0.0)
    actual_return = st.number_input("Actual Return (%)", value=0.0)
    confidence = st.slider("Confidence (1-10)", 1, 10, 5)
    time_spent = st.number_input("Time Spent (hours)", value=0.0)

    submitted = st.form_submit_button("Save Decision")

    if submitted:
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

        st.success("Decision Logged.")

# ---------- Load Data ----------

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)

    if not df.empty:
        st.header("Decision History")
        st.dataframe(df)

        st.header("Capital Analytics")

        metrics = compute_metrics(df)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Average Return", round(metrics["avg_return"], 2))
        col2.metric("Success Rate (%)", round(metrics["success_rate"], 2))
        col3.metric("Confidence Corr.", round(metrics["confidence_corr"], 2))
        col4.metric("Time Corr.", round(metrics["time_corr"], 2))

        st.subheader("Return Over Decisions")
        fig, ax = plt.subplots()
        ax.plot(df["actual_return"].values)
        ax.set_ylabel("Actual Return (%)")
        ax.set_xlabel("Decision Index")
        st.pyplot(fig)

        st.header("Structural Interpretation")

        if st.button("Generate AI Analysis"):
            analysis = generate_analysis(metrics)
            st.write(analysis)

        if st.button("Generate PDF Report"):
            file_path = generate_pdf(metrics, REPORT_FOLDER)
            with open(file_path, "rb") as f:
                st.download_button("Download Report", f, file_name=os.path.basename(file_path))


