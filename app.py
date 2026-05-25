import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Loan Eligibility Dashboard",
    layout="wide"
)

# =========================
# TITLE
# =========================

st.title("🏦 AI-Powered Loan Eligibility Dashboard")

st.write("Upload customer financial data for smart loan analysis.")

# =========================
# FILE UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# =========================
# PROCESS FILE
# =========================

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Uploaded Customer Data")
    st.dataframe(df)

    results = []

    # =========================
    # PROCESS EACH CUSTOMER
    # =========================

    for index, row in df.iterrows():

        name = row["Name"]
        income = row["Monthly_Income"]
        emi = row["Existing_EMI"]
        credit = row["Credit_Score"]
        employment = row["Employment_Type"]
        expenses = row["Monthly_Expenses"]

        # =========================
        # ELIGIBILITY LOGIC
        # =========================

        eligibility = (income - emi - expenses) * 5

        if eligibility < 0:
            eligibility = 0

        # =========================
        # RISK LOGIC
        # =========================

        if credit >= 750:
            risk = "Low Risk"
        elif credit >= 650:
            risk = "Medium Risk"
        else:
            risk = "High Risk"

        # =========================
        # RECOMMENDATION
        # =========================

        if risk == "Low Risk":
            recommendation = "Eligible for Home Loan"
            product = "Premium Home Loan"
            approval = "90%"
            segment = "Prime Customer"
            fraud_score = "Low"

            ai_recommendation = f"""
Customer {name} is financially stable.

Recommended Actions:
- Offer premium products
- Cross-sell insurance
- Increase credit limit
"""

        elif risk == "Medium Risk":
            recommendation = "Eligible for Personal Loan"
            product = "Standard Personal Loan"
            approval = "70%"
            segment = "Growth Customer"
            fraud_score = "Medium"

            ai_recommendation = f"""
Customer {name} has moderate repayment capability.

Recommended Actions:
- Monitor EMI ratio
- Offer medium-value loans
- Encourage savings products
"""

        else:
            recommendation = "Loan Requires Review"
            product = "Basic Banking Products"
            approval = "40%"
            segment = "Risky Customer"
            fraud_score = "High"

            ai_recommendation = f"""
Customer {name} has higher financial risk.

Recommended Actions:
- Verify income documents
- Reduce loan exposure
- Improve credit score first
"""

        # =========================
        # STORE RESULTS
        # =========================

        results.append({

            "Name": name,
            "Eligibility_Amount": eligibility,
            "Risk_Level": risk,
            "Recommendation": recommendation,
            "Suggested_Product": product,
            "Approval_Chance": approval,
            "Customer_Segment": segment,
            "Fraud_Score": fraud_score,
            "AI_Recommendation": ai_recommendation

        })

    # =========================
    # RESULTS DATAFRAME
    # =========================

    result_df = pd.DataFrame(results)

    st.subheader("✅ Loan Eligibility Results")
    st.dataframe(result_df)

    # =========================
    # KPI METRICS
    # =========================

    st.subheader("📊 Dashboard KPIs")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Customers",
        len(result_df)
    )

    col2.metric(
        "Average Eligibility",
        f"₹ {int(result_df['Eligibility_Amount'].mean())}"
    )

    low_risk_count = len(
        result_df[result_df["Risk_Level"] == "Low Risk"]
    )

    col3.metric(
        "Low Risk Customers",
        low_risk_count
    )

    avg_credit = int(df["Credit_Score"].mean())

    col4.metric(
        "Average Credit Score",
        avg_credit
    )

    # =========================
    # RISK DISTRIBUTION CHART
    # =========================

    st.subheader("📈 Risk Distribution")

    risk_chart = px.pie(
        result_df,
        names="Risk_Level",
        title="Customer Risk Distribution"
    )

    st.plotly_chart(risk_chart)

    # =========================
    # ELIGIBILITY CHART
    # =========================

    st.subheader("💰 Eligibility Amount Analysis")

    eligibility_chart = px.bar(
        result_df,
        x="Name",
        y="Eligibility_Amount",
        color="Risk_Level",
        title="Loan Eligibility by Customer"
    )

    st.plotly_chart(eligibility_chart)

    # =========================
    # CUSTOMER SEGMENTATION
    # =========================

    st.subheader("👥 Customer Segmentation")

    segment_chart = px.histogram(
        result_df,
        x="Customer_Segment",
        color="Risk_Level",
        title="Customer Segments"
    )

    st.plotly_chart(segment_chart)

    # =========================
    # EMI CALCULATOR
    # =========================

    st.subheader("🏠 EMI Calculator")

    loan_amount = st.number_input(
        "Loan Amount",
        value=500000
    )

    interest_rate = st.number_input(
        "Interest Rate (%)",
        value=8.5
    )

    tenure = st.number_input(
        "Loan Tenure (Years)",
        value=5
    )

    monthly_rate = interest_rate / 12 / 100

    months = tenure * 12

    emi_value = (
        loan_amount
        * monthly_rate
        * ((1 + monthly_rate) ** months)
    ) / (
        ((1 + monthly_rate) ** months) - 1
    )

    st.success(
        f"Estimated EMI: ₹ {int(emi_value)} per month"
    )

    # =========================
    # DOWNLOAD RESULTS
    # =========================

    csv = result_df.to_csv(index=False)

    st.download_button(
        label="📥 Download Results CSV",
        data=csv,
        file_name="loan_analysis_results.csv",
        mime="text/csv"
    )