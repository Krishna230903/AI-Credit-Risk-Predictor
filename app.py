import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Credit Risk Predictor",
    page_icon="🤖",
    layout="centered"
)


# --- Main App Interface ---
st.title("🤖 AI Credit Risk Predictor")
st.write("Enter applicant details to get an instant credit risk assessment. This tool uses a rule-based model to simulate an AI prediction.")

# --- Input Form using Columns for Layout ---
st.header("Applicant Information")
col1, col2 = st.columns(2)

with col1:
    monthly_salary = st.number_input("Monthly Salary ($)", min_value=0, value=5000)
    loan_amount = st.number_input("Loan Amount ($)", min_value=0, value=10000)
    loan_term = st.number_input("Loan Term (Months)", min_value=1, value=24)

with col2:
    past_loans = st.number_input("Number of Past Loans", min_value=0, value=2)
    job_years = st.number_input("Years at Current Job", min_value=0, value=3)
    monthly_expenses = st.number_input("Monthly Expenses ($)", min_value=0, value=2500)


# --- Prediction Logic on Button Click ---
if st.button("Predict Risk", type="primary"):
    # 1. Refined Risk Calculation
    risk_score = 0
    reasons = []

    # Financial metrics
    # Avoid division by zero if loan_term is 0, though min_value is 1
    monthly_loan_payment = loan_amount / loan_term if loan_term > 0 else 0
    # Avoid division by zero if salary is 0
    debt_to_income_ratio = monthly_loan_payment / monthly_salary if monthly_salary > 0 else 1
    disposable_income = monthly_salary - monthly_expenses - monthly_loan_payment

    # Rule 1: Debt-to-Income Ratio
    if debt_to_income_ratio > 0.45:
        risk_score += 4
        reasons.append("a high loan-to-income ratio")
    elif debt_to_income_ratio > 0.3:
        risk_score += 2

    # Rule 2: Job Stability
    if job_years < 1:
        risk_score += 4
        reasons.append("a short time at the current job")
    elif job_years < 3:
        risk_score += 2

    # Rule 3: Disposable Income
    if disposable_income < 250:
        risk_score += 5
        reasons.append("a very low cash buffer after expenses")
    elif disposable_income < 750:
        risk_score += 2
        reasons.append("a modest cash buffer")

    # Rule 4: Past Loan History
    if past_loans > 5:
        risk_score += 2
        reasons.append("a high number of previous loans")

    # 2. Determine Final Prediction and Results
    if risk_score > 6:
        prediction = "HIGH RISK"
        probability = min(0.25 + (risk_score * 0.05), 0.95)
        credit_score = max(300, 700 - (risk_score * 25))
        explanation = f"The risk is elevated due to factors like {', '.join(reasons)}."
    else:
        prediction = "LOW RISK"
        probability = max(0.02, 0.20 - (risk_score * 0.03))
        credit_score = min(900, 720 + ((6 - risk_score) * 30))
        explanation = "Strong financial indicators suggest a low risk profile."

    credit_score = int(max(300, min(900, credit_score)))

    # --- Display Results ---
    st.header("Prediction Result")
    
    if prediction == "HIGH RISK":
        st.error(f"**Risk Assessment: {prediction}**")
    else:
        st.success(f"**Risk Assessment: {prediction}**")

    # Display metrics in columns
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric(label="Probability of Default", value=f"{probability:.1%}")
    with res_col2:
        st.metric(label="AI Credit Score", value=str(credit_score))

    # Visual Score Gauge
    st.write("Credit Score Gauge (300-900)")
    gauge_percent = (credit_score - 300) / 600
    st.progress(gauge_percent)

    # Explanation Snippet
    st.info(f"**Justification:** {explanation}")
