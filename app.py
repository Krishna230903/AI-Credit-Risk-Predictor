import streamlit as st
import pandas as pd
import joblib

# --- Page Configuration ---
st.set_page_config(
    page_title="Accurate AI Credit Risk Predictor",
    page_icon="🧠",
    layout="centered"
)

# --- Load The Trained Model ---
# Use st.cache_resource to load the model only once and store it in cache
@st.cache_resource
def load_model():
    try:
        model = joblib.load('credit_risk_model.joblib')
        return model
    except FileNotFoundError:
        return None

model = load_model()

# --- Main App Interface ---
st.title("🧠 Accurate AI Credit Risk Predictor")

if model is None:
    st.error(
        "**Model not found!** Please run the `train_model.py` script first to train and save the model."
    )
else:
    st.write(
        "This app uses a Machine Learning model to predict credit risk with higher accuracy."
    )

    # --- Input Form ---
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

    # --- Prediction Logic ---
    if st.button("Predict Risk", type="primary"):
        # 1. Create a DataFrame from the user's input
        # The column order must exactly match the training data
        input_data = pd.DataFrame(
            {
                'monthly_salary': [monthly_salary],
                'loan_amount': [loan_amount],
                'loan_term': [loan_term],
                'past_loans': [past_loans],
                'job_years': [job_years],
                'monthly_expenses': [monthly_expenses],
            }
        )

        # 2. Use the model to predict the probability of default
        # model.predict_proba returns probabilities for [class_0, class_1]
        # We need the probability of default (class 1)
        probability = model.predict_proba(input_data)[0][1]
        prediction = "HIGH RISK" if probability > 0.5 else "LOW RISK"

        # 3. Map probability to a credit score for display
        # This is a simple linear mapping for a better user experience
        credit_score = int(300 + (1 - probability) * 600)

        # --- Display Results ---
        st.header("Prediction Result")
        if prediction == "HIGH RISK":
            st.error(f"**Risk Assessment: {prediction}**")
        else:
            st.success(f"**Risk Assessment: {prediction}**")

        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric(label="Probability of Default", value=f"{probability:.1%}")
        with res_col2:
            st.metric(label="AI Credit Score", value=str(credit_score))

        st.write("Credit Score Gauge (300-900)")
        gauge_percent = (credit_score - 300) / 600
        st.progress(gauge_percent)
