import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page setup
# -----------------------------

st.set_page_config(
    page_title="Insurance Risk & Claim Trends Analysis",
    layout="wide"
)

# Remove sidebar
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Insurance Risk & Claim Trends Analysis")

# -----------------------------
# FORM (TOP) — No Default Values
# -----------------------------

st.header("🚗 Insurance Claim Submission")

col1, col2 = st.columns(2)

with col1:
    claim_amount = st.number_input(
        "Claim Amount",
        min_value=0,
        step=100,
        value=None,
        placeholder="Enter claim amount"
    )

    incident_type = st.selectbox(
        "Incident Type",
        ["Collision", "Vehicle Theft", "Fire", "Natural Disaster"],
        index=None,
        placeholder="Select incident type"
    )

    incident_severity = st.selectbox(
        "Incident Severity",
        ["Minor Damage", "Major Damage", "Total Loss"],
        index=None,
        placeholder="Select severity"
    )

with col2:
    witnesses = st.number_input(
        "Number of Witnesses",
        min_value=0,
        max_value=5,
        value=None,
        placeholder="Enter witnesses count"
    )

    police_report = st.selectbox(
        "Police Report Filed?",
        ["Yes", "No"],
        index=None,
        placeholder="Select option"
    )

    vehicle_involved = st.number_input(
        "Vehicles Involved",
        min_value=1,
        max_value=5,
        value=None,
        placeholder="Enter vehicle count"
    )

# -----------------------------
# Fraud Risk Calculation
# -----------------------------

if st.button("Check Fraud Risk"):

    # Validate inputs
    if (
        claim_amount is None or
        incident_type is None or
        incident_severity is None or
        witnesses is None or
        police_report is None or
        vehicle_involved is None
    ):
        st.warning("⚠️ Please fill all fields before checking risk.")

    else:

        risk = 0

        if claim_amount > 20000:
            risk += 2

        if incident_severity == "Total Loss":
            risk += 2

        if witnesses == 0:
            risk += 1

        if police_report == "No":
            risk += 1

        if vehicle_involved > 2:
            risk += 1

        if risk >= 4:
            st.error("⚠️ High Fraud Risk")

        elif risk >= 2:
            st.warning("⚠️ Medium Fraud Risk")

        else:
            st.success("✅ Low Fraud Risk")

st.divider()

# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv("fraud_insurance_claims.csv")

# -----------------------------
# Dashboard Title
# -----------------------------

st.header("📈 Insurance Claim Dashboard")

# Metrics
c1, c2, c3 = st.columns(3)

c1.metric("Total Claims", len(df))

c2.metric(
    "Average Claim Amount",
    int(df["total_claim_amount"].mean())
)

c3.metric(
    "Maximum Claim Amount",
    int(df["total_claim_amount"].max())
)

# -----------------------------
# Charts
# -----------------------------

col1, col2 = st.columns(2)

# Fraud Distribution
with col1:
    fig1 = px.histogram(
        df,
        x="fraud_reported",
        title="Fraud vs Non-Fraud Claims",
        color="fraud_reported"
    )

    st.plotly_chart(fig1, use_container_width=True)

# Claim Amount Distribution
with col2:
    fig2 = px.histogram(
        df,
        x="total_claim_amount",
        nbins=40,
        title="Claim Amount Distribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

# Claim Type Chart
fig3 = px.bar(
    df,
    x="incident_type",
    y="total_claim_amount",
    color="incident_type",
    title="Claim Amount by Incident Type"
)

st.plotly_chart(fig3, use_container_width=True)

# Fraud vs Amount
fig4 = px.box(
    df,
    x="fraud_reported",
    y="total_claim_amount",
    title="Fraud vs Claim Amount"
)

st.plotly_chart(fig4, use_container_width=True)