import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from fpdf import FPDF
import io

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(
    page_title="EHS Risk Calculator",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------
# Title
# ------------------------------
st.title("⚠️ EHS Risk Calculator")
st.markdown("A simple tool for Environment, Health & Safety risk assessment.")

# ------------------------------
# Sidebar Inputs
# ------------------------------
st.sidebar.header("Enter Risk Parameters")

likelihood = st.sidebar.slider("Likelihood (1=Rare, 5=Almost Certain)", 1, 5, 3)
severity = st.sidebar.slider("Severity (1=Minor, 5=Catastrophic)", 1, 5, 3)

# ------------------------------
# Risk Calculation
# ------------------------------
risk_score = likelihood * severity

if risk_score <= 4:
    risk_level = "Low"
    color = "green"
elif risk_score <= 9:
    risk_level = "Medium"
    color = "orange"
else:
    risk_level = "High"
    color = "red"

# ------------------------------
# Output
# ------------------------------
st.subheader("📊 Risk Assessment Result")
st.markdown(f"**Risk Score:** {risk_score}")
st.markdown(f"**Risk Level:** <span style='color:{color}; font-weight:bold'>{risk_level}</span>", unsafe_allow_html=True)

# ------------------------------
# Heatmap (Risk Matrix)
# ------------------------------
st.subheader("📈 Risk Matrix Heatmap")

matrix = pd.DataFrame(
    [[i*j for j in range(1,6)] for i in range(1,6)],
    index=[1,2,3,4,5],
    columns=[1,2,3,4,5]
)

fig, ax = plt.subplots()
sns.heatmap(matrix, annot=True, fmt="d", cmap="RdYlGn_r", cbar=False, ax=ax)
ax.set_xlabel("Severity")
ax.set_ylabel("Likelihood")
st.pyplot(fig)

# ------------------------------
# Export Options
# ------------------------------
st.sidebar.header("Export Options")

export_choice = st.sidebar.radio("Export Report As:", ["None", "PDF", "Excel"])

if export_choice == "PDF":
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="EHS Risk Calculator Report", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Likelihood: {likelihood}", ln=True)
    pdf.cell(200, 10, txt=f"Severity: {severity}", ln=True)
    pdf.cell(200, 10, txt=f"Risk Score: {risk_score}", ln=True)
    pdf.cell(200, 10, txt=f"Risk Level: {risk_level}", ln=True)
    pdf_output = pdf.output(dest="S").encode("latin1")
    st.download_button("📥 Download PDF", data=pdf_output, file_name="EHS_Risk_Report.pdf", mime="application/pdf")

elif export_choice == "Excel":
    df = pd.DataFrame({"Likelihood":[likelihood],"Severity":[severity],"Risk Score":[risk_score],"Risk Level":[risk_level]})
    towrite = io.BytesIO()
    df.to_excel(towrite, index=False, engine="openpyxl")
    towrite.seek(0)
    st.download_button("📥 Download Excel", data=towrite, file_name="EHS_Risk_Report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
