import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Insurance Claims EDA", layout="wide")

st.title("📊 Insurance Claims EDA")

# Load data
df = pd.read_csv("C:\\Users\\Tharshana\\Desktop\\EDA\\fraud_insurance_claims.csv")

# Key metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Claims", len(df))
col2.metric("Average Claim", f"${df['total_claim_amount'].mean():,.0f}")
col3.metric("Fraud Rate", f"{(df['fraud_reported'].value_counts()['Y']/len(df)*100):.1f}%")

# Main charts
st.header("Fraud Analysis")
col1, col2 = st.columns(2)

with col1:
    fig1 = px.histogram(df, x="fraud_reported", color="fraud_reported", 
                       title="Fraud vs Legitimate Claims")
    st.plotly_chart(fig1, width='stretch')

with col2:
    fig2 = px.box(df, x="fraud_reported", y="total_claim_amount", 
                 title="Claim Amounts by Fraud Status")
    st.plotly_chart(fig2, width='stretch')

st.header("Claim Distributions")
col1, col2 = st.columns(2)

with col1:
    fig3 = px.histogram(df, x="total_claim_amount", nbins=30, 
                       title="Claim Amount Distribution")
    st.plotly_chart(fig3, width='stretch')

with col2:
    fig4 = px.bar(df['incident_type'].value_counts().reset_index(), 
                 x='incident_type', y='count', title="Incidents by Type")
    st.plotly_chart(fig4, width='stretch')

st.header("Relationships")
fig5 = px.scatter(df, x="age", y="total_claim_amount", color="fraud_reported",
                 title="Age vs Claim Amount")
st.plotly_chart(fig5, width='stretch')