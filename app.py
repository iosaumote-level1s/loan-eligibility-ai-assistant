import streamlit as st
import pandas as pd
import google.generativeai as genai
import plotly.express as px
import numpy as np

# ==============================
# GEMINI API CONFIGURATION
# ==============================

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Load Gemini Model
model = genai.GenerativeModel("gemini-1.5-flash")

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="AI BFSI Credit Intelligence Platform",
    layout="wide"
)

# ==============================
# TITLE
# ==============================

st.title("🏦 AI BFSI Credit Intelligence Platform")

st.write(
    "AI-powered banking analytics dashboard for loan eligibility, risk analysis, fraud scoring, and customer segmentation."
)

# ==============================
# EMI CALCULATOR
# ==============================

st.subheader("💰 EMI Calculator")

col1, col2, col3 = st.columns(3)

with col1:
    loan_amount = st.number_input(
        "Loan Amount",
        value=500000
    )

with col2:
    interest_rate = st.number_input(
        "Interest Rate (%)",
        value=8.5
    )

with col3:
    loan_tenure = st.number_input(
        "Tenure (Years)",
        value=5
    )

monthly_rate = interest_rate / 12 / 100
months = loan_tenure * 12

emi = (
    loan_amount
    * monthly_rate
    * (1 + monthly_rate) ** months
) / (
    (1 + monthly_rate) ** months - 1
)

st.success(f"Estimated Monthly EMI: ₹{int(emi)}")

st.divider()

# ==============================
# FILE UPLOAD
# ==============================

uploaded_file = st.file_uploader(
    "📂 Upload CSV File",
    type=["csv"]
)

# ==============================
# PROCESS DATA
# ==============================

if uploaded_file is not None:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Uploaded Customer Data")

    st.dataframe(df)

    results = []

    # ==============================
    # ANALYSIS LOOP
    # ==============================

    for index, row in df.iterrows():

        name = row["Name"]
        income = row["Monthly_Income"]
        emi_existing = row["Existing_EMI"]
        credit = row["Credit_Score"]
        employment = row["Employment_Type"]
        expenses = row["Monthly_Expenses"]

        # ==============================
        # ELIGIBILITY LOGIC
        # ==============================

        disposable_income = income - emi_existing - expenses

        eligibility = disposable_income * 15

        # ==============================
        # RISK ANALYSIS
        # ==============================

        if credit >= 750:
            risk = "Low Risk"
            recommendation = "Eligible for Home Loan"
            product = "Premium Home Loan"

        elif credit >= 700:
            risk = "Medium Risk"
            recommendation = "Eligible for Personal Loan"
            product = "Standard Personal Loan"

        else:
            risk = "High Risk"
            recommendation = "Loan Approval Needs Review"
            product = "Secured Loan"

        # ==============================
        # APPROVAL PERCENTAGE
        # ==============================

        approval_percentage = min(
            95,
            max(
                40,
                int((credit / 900) * 100)
            )
        )

        # ==============================
        # CUSTOMER SEGMENTATION
        # ==============================

        if income >= 100000:
            segment = "Premium"

        elif income >= 60000:
            segment = "Standard"

        else:
            segment = "Basic"

        # ==============================
        # FRAUD SCORE
        # ==============================

        fraud_score = np.random.randint(5, 30)

        if credit < 650:
            fraud_score += 40

        # ==============================
        # GEMINI AI PROMPT
        # ==============================

        prompt = f"""
        You are a senior BFSI banking analyst.

        Analyze this customer:

        Name: {name}
        Monthly Income: {income}
        Existing EMI: {emi_existing}
        Credit Score: {credit}
        Employment Type: {employment}
        Monthly Expenses: {expenses}

        Give:
        1. Short banking recommendation
        2. Risk summary
        3. Best financial advice

        Keep response professional and short.
        """

        # ==============================
        # GEMINI RESPONSE
        # ==============================

        try:

            response = model.generate_content(prompt)

            ai_recommendation = response.text

        except Exception as e:

            ai_recommendation = "AI recommendation unavailable."

        # ==============================
        # STORE RESULTS
        # ==============================

        results.append({

            "Name": name,

            "Eligibility_Amount": eligibility,

            "Risk_Level": risk,

            "Recommendation": recommendation,

            "Suggested_Product": product,

            "Approval_Percentage": f"{approval_percentage}%",

            "Customer_Segment": segment,

            "Fraud_Score": fraud_score,

            "AI_Recommendation": ai_recommendation
        })

    # ==============================
    # RESULTS DATAFRAME
    # ==============================

    result_df = pd.DataFrame(results)

    # ==============================
    # KPI DASHBOARD
    # ==============================

    st.subheader("📊 Dashboard KPIs")

    total_customers = len(result_df)

    avg_eligibility = int(
        result_df["Eligibility_Amount"].mean()
    )

    total_loan_amount = int(
        result_df["Eligibility_Amount"].sum()
    )

    avg_fraud = int(
        result_df["Fraud_Score"].mean()
    )

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(
        "Customers",
        total_customers
    )

    kpi2.metric(
        "Avg Eligibility",
        f"₹{avg_eligibility}"
    )

    kpi3.metric(
        "Total Loan Amount",
        f"₹{total_loan_amount}"
    )

    kpi4.metric(
        "Avg Fraud Score",
        avg_fraud
    )

    # ==============================
    # RESULTS TABLE
    # ==============================

    st.subheader("🏦 Loan Eligibility Results")

    st.dataframe(result_df)

    # ==============================
    # CHARTS
    # ==============================

    st.subheader("📈 Loan Eligibility Analysis")

    # Bar Chart

    fig1 = px.bar(
        result_df,
        x="Name",
        y="Eligibility_Amount",
        color="Risk_Level",
        title="Loan Eligibility by Customer"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Pie Chart

    fig2 = px.pie(
        result_df,
        names="Customer_Segment",
        title="Customer Segmentation"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Fraud Histogram

    fig3 = px.histogram(
        result_df,
        x="Fraud_Score",
        color="Risk_Level",
        title="Fraud Score Distribution"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # Approval Percentage Chart

    fig4 = px.line(
        result_df,
        x="Name",
        y=[
            int(x.replace("%", ""))
            for x in result_df["Approval_Percentage"]
        ],
        markers=True,
        title="Approval Percentage"
    )

    st.plotly_chart(fig4, use_container_width=True)

    # ==============================
    # DOWNLOAD CSV
    # ==============================

    csv = result_df.to_csv(index=False)

    st.download_button(
        label="⬇ Download Results CSV",
        data=csv,
        file_name="loan_analysis_results.csv",
        mime="text/csv"
    )