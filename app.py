import streamlit as st
import pandas as pd
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyAptlT0QpnfIjBmbNQCmFX0gORe-STCTW0")

# Load Gemini model
model = genai.GenerativeModel("gemini-flash-latest")

# Page Config
st.set_page_config(page_title="Loan Eligibility AI Assistant")

# Title
st.title("🏦 Loan Eligibility AI Assistant")

st.write("Upload customer financial data for loan analysis.")

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# Process CSV
if uploaded_file is not None:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Show uploaded data
    st.subheader("Uploaded Customer Data")
    st.dataframe(df)

    results = []

    # Process rows
    for index, row in df.iterrows():

        income = int(row["Monthly_Income"])
        emi = int(row["Existing_EMI"])
        credit = int(row["Credit_Score"])
        expenses = int(row["Monthly_Expenses"])

        eligibility = income - emi - expenses

        # AI Prompt
        prompt = f"""
        Customer Name: {row['Name']}
        Monthly Income: {income}
        Existing EMI: {emi}
        Credit Score: {credit}
        Monthly Expenses: {expenses}

        Give a short professional banking recommendation.
        """

        # Gemini Response
        response = model.generate_content(prompt)

        ai_recommendation = response.text

        # Risk Analysis
        if credit >= 750:
            risk = "Low Risk"

        elif credit >= 700:
            risk = "Medium Risk"

        else:
            risk = "High Risk"

        # Loan Recommendation
        if eligibility > 40000:
            recommendation = "Eligible for Home Loan"
            product = "Premium Home Loan"

        elif eligibility > 20000:
            recommendation = "Eligible for Personal Loan"
            product = "Standard Personal Loan"

        else:
            recommendation = "Loan Approval Difficult"
            product = "Secured Loan"

        # Store Results
        results.append({
            "Name": row["Name"],
            "Eligibility_Amount": eligibility,
            "Risk_Level": risk,
            "Recommendation": recommendation,
            "Suggested_Product": product,
            "AI_Recommendation": ai_recommendation
        })

    # Result DataFrame
    result_df = pd.DataFrame(results)

    # Show Results
    st.subheader("Loan Eligibility Results")
    st.dataframe(result_df)

    # Download CSV
    csv = result_df.to_csv(index=False)

    st.download_button(
        label="Download Results CSV",
        data=csv,
        file_name="loan_analysis_results.csv",
        mime="text/csv"
    )