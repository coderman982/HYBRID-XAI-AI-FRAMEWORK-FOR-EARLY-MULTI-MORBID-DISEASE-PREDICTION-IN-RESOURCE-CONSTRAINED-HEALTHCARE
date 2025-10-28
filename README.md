# Hybrid XAI — Multi‑Disease Prediction (Lightweight)

Hybrid XAI is a lightweight framework for early multi‑morbidity disease risk prediction optimized for resource‑constrained healthcare settings. It combines a small Random Forest multi‑output model with simple clinical rule‑based checks and generates human‑readable explanations.


Files:
- [HYBRID XAI AI FRAMEWORK FOR EARLY MULTI-MORBID DISEASE PREDICTION IN RESOURCE-CONSTRAINED HEALTHCARE SETTINGS/multi_disease_prediction.py](HYBRID XAI AI FRAMEWORK FOR EARLY MULTI-MORBID DISEASE PREDICTION IN RESOURCE-CONSTRAINED HEALTHCARE SETTINGS/multi_disease_prediction.py) — main script implementing preprocessing, training, hybrid inference and explanations.

  - Key symbols:

    - [`multi_disease_prediction.preprocess_data`](HYBRID XAI AI FRAMEWORK FOR EARLY MULTI-MORBID DISEASE PREDICTION IN RESOURCE-CONSTRAINED HEALTHCARE SETTINGS/multi_disease_prediction.py)

    - [`multi_disease_prediction.hybrid_prediction`](HYBRID XAI AI FRAMEWORK FOR EARLY MULTI-MORBID DISEASE PREDICTION IN RESOURCE-CONSTRAINED HEALTHCARE SETTINGS/multi_disease_prediction.py)

    - [`multi_disease_prediction.generate_explanation`](HYBRID XAI AI FRAMEWORK FOR EARLY MULTI-MORBID DISEASE PREDICTION IN RESOURCE-CONSTRAINED HEALTHCARE SETTINGS/multi_disease_prediction.py)

    - [`multi_disease_prediction.predict_new_patient`](HYBRID XAI AI FRAMEWORK FOR EARLY MULTI-MORBID DISEASE PREDICTION IN RESOURCE-CONSTRAINED HEALTHCARE SETTINGS/multi_disease_prediction.py)

    - [`multi_disease_prediction.main`](HYBRID XAI AI FRAMEWORK FOR EARLY MULTI-MORBID DISEASE PREDICTION IN RESOURCE-CONSTRAINED HEALTHCARE SETTINGS/multi_disease_prediction.py)

- [HYBRID XAI AI FRAMEWORK FOR EARLY MULTI-MORBID DISEASE PREDICTION IN RESOURCE-CONSTRAINED HEALTHCARE SETTINGS/DISEASES](HYBRID XAI AI FRAMEWORK FOR EARLY MULTI-MORBID DISEASE PREDICTION IN RESOURCE-CONSTRAINED HEALTHCARE SETTINGS/DISEASES) — short human readable note about chronic diseases.


Quick start

1. Create a Python environment and install dependencies:
```sh
pip install pandas numpy scikit-learn joblib


What the script produces

rf_model.pkl — trained Random Forest multi‑output model
scaler.pkl — StandardScaler used for features
multi_disease_risk_report.csv — per‑patient risk predictions and explanations for the test set
new_patient_risk_report.csv — example output for the provided new patient

python "HYBRID XAI AI FRAMEWORK FOR EARLY MULTI-MORBID DISEASE PREDICTION IN RESOURCE-CONSTRAINED HEALTHCARE SETTINGS/multi_disease_prediction.py"


What the script produces

rf_model.pkl — trained Random Forest multi‑output model
scaler.pkl — StandardScaler used for features
multi_disease_risk_report.csv — per‑patient risk predictions and explanations for the test set
new_patient_risk_report.csv — example output for the provided new patient



How to use programmatically

Call the [multi_disease_prediction.predict_new_patient](HYBRID XAI AI FRAMEWORK FOR EARLY MULTI-MORBID DISEASE PREDICTION IN RESOURCE-CONSTRAINED HEALTHCARE SETTINGS/multi_disease_prediction.py) function to get predictions for a single patient record (pass a dict with fields AGE, GENDER, BMI, BP_SYSTOLIC, BP_DIASTOLIC, GLUCOSE, CHOLESTEROL, EGFR, FAMILY_HISTORY, SMOKING).


Notes and limitations

The current dataset is synthetic and tiny — replace with real clinical data for production use.
The rule set is intentionally simple for interpretability; clinical validation is required before deployment.
The Random Forest is small (n_estimators=20, max_depth=3) to keep it lightweight; adjust for accuracy/resource tradeoffs.


License

Add an appropriate license file as needed.
