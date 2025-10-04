# multi_disease_prediction.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import accuracy_score
import shap
import joblib
import matplotlib.pyplot as plt
import os

# Simulated dataset for multiple morbid diseases
data = {
    'patient_id': ['P001', 'P002', 'P003', 'P004', 'P005', 'P006', 'P007', 'P008', 'P009', 'P010'],
    'age': [45, 60, 35, 50, 55, 62, 40, 58, 47, 53],
    'gender': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],  # 0: Male, 1: Female
    'bmi': [28, 32, 25, 30, 34, 29, 27, 33, 31, 26],
    'bp_systolic': [130, 150, 120, 140, 155, 145, 125, 160, 135, 128],
    'bp_diastolic': [80, 90, 75, 85, 95, 88, 78, 92, 82, 77],
    'glucose': [90, 140, 85, 110, 150, 130, 95, 145, 100, 88],
    'cholesterol': [180, 220, 170, 200, 230, 210, 175, 225, 190, 185],
    'egfr': [90, 60, 100, 85, 55, 70, 95, 50, 80, 88],  # eGFR for kidney function
    'family_history': [0, 1, 0, 1, 1, 0, 0, 1, 0, 1],
    'smoking': [0, 1, 0, 0, 1, 0, 1, 0, 0, 1],
    'diabetes': [0, 1, 0, 1, 1, 1, 0, 1, 0, 0],  # 1: High risk
    'hypertension': [0, 1, 0, 1, 1, 1, 0, 1, 0, 0],
    'cardiovascular': [0, 1, 0, 0, 1, 1, 0, 1, 0, 0],
    'ckd': [0, 1, 0, 0, 1, 0, 0, 1, 0, 0]  # Chronic kidney disease
}
df = pd.DataFrame(data)

# Data preprocessing
def preprocess_data(df, save_scaler=True):
    df.fillna(df.mean(numeric_only=True), inplace=True)
    features = ['age', 'gender', 'bmi', 'bp_systolic', 'bp_diastolic', 'glucose', 
                'cholesterol', 'egfr', 'family_history', 'smoking']
    targets = ['diabetes', 'hypertension', 'cardiovascular', 'ckd']
    X = df[features]
    y = df[targets]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    if save_scaler:
        joblib.dump(scaler, 'scaler.pkl')
    return X, y, X_scaled, scaler, features, targets

# Rule-based predictions for each disease
def rule_based_predictions(patient_data):
    rules = {
        'diabetes': 1 if patient_data['glucose'] > 126 or patient_data['bmi'] > 30 else 0,
        'hypertension': 1 if patient_data['bp_systolic'] > 140 or patient_data['bp_diastolic'] > 90 else 0,
        'cardiovascular': 1 if (patient_data['cholesterol'] > 200 or 
                               (patient_data['bp_systolic'] > 140 and patient_data['smoking'] == 1)) else 0,
        'ckd': 1 if patient_data['egfr'] < 60 else 0
    }
    return rules

# Hybrid prediction
def hybrid_prediction(ml_model, X_scaled, X_raw, ml_weight=0.5, rule_weight=0.5):
    ml_probs = ml_model.predict_proba(X_scaled)
    hybrid_preds = []
    hybrid_probs = []
    for i, disease in enumerate(['diabetes', 'hypertension', 'cardiovascular', 'ckd']):
        ml_prob = ml_probs[i][:, 1]  # Probability of high risk for disease i
        rule_preds = X_raw.apply(lambda row: rule_based_predictions(row)[disease], axis=1)
        combined_probs = ml_weight * ml_prob + rule_weight * rule_preds
        hybrid_preds.append((combined_probs > 0.5).astype(int))
        hybrid_probs.append(combined_probs)
    return np.array(hybrid_preds).T, np.array(hybrid_probs).T

# Explainability
def generate_explanation(patient_data, shap_values, feature_names, patient_id, disease):
    explanation = f"Patient {patient_id} risk for {disease} is {'high' if shap_values[1][0].sum() > 0 else 'low'} because: "
    for i, feature in enumerate(feature_names):
        if shap_values[1][0][i] > 0:
            explanation += f"{feature} ({patient_data[feature]}) contributes to higher risk. "
    return explanation if shap_values[1][0].sum() > 0 else f"Patient {patient_id} has low risk for {disease}."

# Main function
def main():
    # Preprocess data
    X, y, X_scaled, scaler, features, targets = preprocess_data(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train multi-output Random Forest
    rf_model = MultiOutputClassifier(RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42))
    rf_model.fit(X_train_scaled, y_train)
    joblib.dump(rf_model, 'rf_model.pkl')

    # Hybrid predictions
    hybrid_preds, hybrid_probs = hybrid_prediction(rf_model, X_test_scaled, X_test)

    # SHAP explanations
    explainer = shap.TreeExplainer(rf_model.estimators_[0])  # Use first estimator for visualization
    shap_values = explainer.shap_values(X_test_scaled)

    # Generate report
    report = []
    for i, idx in enumerate(X_test.index):
        patient_id = df.loc[idx, 'patient_id']
        for j, disease in enumerate(targets):
            explanation = generate_explanation(X_test.iloc[i], shap_values[j][i:i+1], features, patient_id, disease)
            report.append({
                'Patient_ID': patient_id,
                'Disease': disease,
                'Risk_Prediction': 'High' if hybrid_preds[i][j] == 1 else 'Low',
                'Risk_Score': hybrid_probs[i][j],
                'Explanation': explanation
            })

    # Save report to CSV
    report_df = pd.DataFrame(report)
    report_df.to_csv('multi_disease_risk_report.csv', index=False)
    print("Report generated: multi_disease_risk_report.csv")

    # Save visualization for first patient, first disease
    shap.initjs()
    shap.force_plot(explainer.expected_value[1], shap_values[0][0], X_test.iloc[0], matplotlib=True)
    plt.savefig('shap_plot_diabetes.png', bbox_inches='tight')
    print("Visualization saved: shap_plot_diabetes.png")

    # Evaluate
    for i, disease in enumerate(targets):
        print(f"{disease} Accuracy: {accuracy_score(y_test[disease], hybrid_preds[:, i]):.2f}")

if __name__ == "__main__":
    main()

# Function for new patient prediction
def predict_new_patient(patient_data, model_path='rf_model.pkl', scaler_path='scaler.pkl'):
    rf_model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    patient_df = pd.DataFrame([patient_data])
    patient_scaled = scaler.transform(patient_df)
    hybrid_preds, hybrid_probs = hybrid_prediction(rf_model, patient_scaled, patient_df)
    explainer = shap.TreeExplainer(rf_model.estimators_[0])
    shap_values = explainer.shap_values(patient_scaled)
    results = []
    for i, disease in enumerate(['diabetes', 'hypertension', 'cardiovascular', 'ckd']):
        explanation = generate_explanation(patient_df.iloc[0], shap_values[i], patient_df.columns, 'New', disease)
        results.append({
            'Disease': disease,
            'Risk_Prediction': 'High' if hybrid_preds[0][i] == 1 else 'Low',
            'Risk_Score': hybrid_probs[0][i],
            'Explanation': explanation
        })
    return pd.DataFrame(results)