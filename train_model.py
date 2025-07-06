import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# 1. Generate a realistic but fake dataset
print("Generating training data...")
np.random.seed(42)
num_records = 2000
data = {
    'monthly_salary': np.random.randint(2000, 15000, num_records),
    'loan_amount': np.random.randint(5000, 50000, num_records),
    'loan_term': np.random.choice([12, 24, 36, 48, 60], num_records),
    'past_loans': np.random.randint(0, 10, num_records),
    'job_years': np.random.randint(0, 25, num_records),
    'monthly_expenses': np.random.randint(1000, 8000, num_records),
}
df = pd.DataFrame(data)

# 2. Engineer features and create a target variable ('default')
# Create a risk score to determine the probability of default
risk_factor = (
    (df['loan_amount'] / (df['monthly_salary'] * df['loan_term'])) * 5 +
    (df['monthly_expenses'] / df['monthly_salary']) * 2 -
    (df['job_years'] / 10) +
    (df['past_loans'] / 5)
)

# Create the 'default' target variable based on the risk factor
# We add some noise to make it more realistic
prob_default = 1 / (1 + np.exp(-risk_factor + np.random.normal(0, 1, num_records)))
df['default'] = (prob_default > 0.6).astype(int) # A threshold of 60% probability

# 3. Train the Machine Learning Model
print("Training the model...")
X = df.drop('default', axis=1)
y = df['default']

# Split data (optional for this demo, but good practice)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# We'll use a simple Logistic Regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 4. Save the trained model to a file
print("Saving the model...")
joblib.dump(model, 'credit_risk_model.joblib')

print("\nModel trained and saved as 'credit_risk_model.joblib'")
print(f"Sample of generated data:\n{df.head()}")
print(f"\nDefault rate in generated data: {df['default'].mean():.2%}")
