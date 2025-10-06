# MULTI_DISEASE_PREDICTION.PY
# HYBRID XAI FRAMEWORK FOR EARLY MULTI-MORBID DISEASE PREDICTION
# AUTHOR: GROK (BUILT BY XAI)
# DATE: OCTOBER 4, 2025
# DESCRIPTION: PREDICTS RISK OF DIABETES, HYPERTENSION, CARDIOVASCULAR DISEASE, AND CKD
#              USING A HYBRID MODEL (RANDOM FOREST + RULE-BASED) WITH FEATURE IMPORTANCE EXPLANATIONS.
#              OPTIMIZED FOR LOW-RESOURCE DEVICES AND RUNNABLE IN JUPYTER NOTEBOOK.

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import accuracy_score
import joblib
import logging

# CONFIGURE LOGGING
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# SIMULATED DATASET
data = {
    'PATIENT_ID': ['P001', 'P002', 'P003', 'P004', 'P005', 'P006', 'P007', 'P008', 'P009', 'P010'],
    'AGE': [45, 60, 35, 50, 55, 62, 40, 58, 47, 53],
    'GENDER': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],  # 0: MALE, 1: FEMALE
    'BMI': [28, 32, 25, 30, 34, 29, 27, 33, 31, 26],
    'BP_SYSTOLIC': [130, 150, 120, 140, 155, 145, 125, 160, 135, 128],
    'BP_DIASTOLIC': [80, 90, 75, 85, 95, 88, 78, 92, 82, 77],
    'GLUCOSE': [90, 140, 85, 110, 150, 130, 95, 145, 100, 88],
    'CHOLESTEROL': [180, 220, 170, 200, 230, 210, 175, 225, 190, 185],
    'EGFR': [90, 60, 100, 85, 55, 70, 95, 50, 80, 88],
    'FAMILY_HISTORY': [0, 1, 0, 1, 1, 0, 0, 1, 0, 1],
    'SMOKING': [0, 1, 0, 0, 1, 0, 1, 0, 0, 1],
    'DIABETES': [0, 1, 0, 1, 1, 1, 0, 1, 0, 0],
    'HYPERTENSION': [0, 1, 0, 1, 1, 1, 0, 1, 0, 0],
    'CARDIOVASCULAR': [0, 1, 0, 0, 1, 1, 0, 1, 0, 0],
    'CKD': [0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
}
df = pd.DataFrame(data)

# PREPROCESS DATA
def preprocess_data(df, save_scaler=True):
    try:
        df.fillna(df.mean(numeric_only=True), inplace=True)
        features = ['AGE', 'GENDER', 'BMI', 'BP_SYSTOLIC', 'BP_DIASTOLIC', 'GLUCOSE', 
                    'CHOLESTEROL', 'EGFR', 'FAMILY_HISTORY', 'SMOKING']
        targets = ['DIABETES', 'HYPERTENSION', 'CARDIOVASCULAR', 'CKD']
        X = df[features]
        y = df[targets]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        if save_scaler:
            joblib.dump(scaler, 'scaler.pkl')
            logging.info('SCALER SAVED')
        return X, y, X_scaled, scaler, features, targets
    except Exception as e:
        logging.error(f'PREPROCESSING ERROR: {e}')
        raise

# RULE-BASED PREDICTIONS
def rule_based_predictions(patient_data):
    try:
        rules = {
            'DIABETES': 1 if patient_data['GLUCOSE'] > 126 or patient_data['BMI'] > 30 else 0,
            'HYPERTENSION': 1 if patient_data['BP_SYSTOLIC'] > 140 or patient_data['BP_DIASTOLIC'] > 90 else 0,
            'CARDIOVASCULAR': 1 if (patient_data['CHOLESTEROL'] > 200 or 
                                   (patient_data['BP_SYSTOLIC'] > 140 and patient_data['SMOKING'] == 1)) else 0,
            'CKD': 1 if patient_data['EGFR'] < 60 else 0
        }
        return rules
    except Exception as e:
        logging.error(f'RULE-BASED ERROR: {e}')
        raise

# HYBRID PREDICTION
def hybrid_prediction(ml_model, X_scaled, X_raw, ml_weight=0.5, rule_weight=0.5):
    try:
        ml_probs = ml_model.predict_proba(X_scaled)
        hybrid_preds = []
        hybrid_probs = []
        for i, disease in enumerate(['DIABETES', 'HYPERTENSION', 'CARDIOVASCULAR', 'CKD']):
            ml_prob = ml_probs[i][:, 1]
            rule_preds = X_raw.apply(lambda row: rule_based_predictions(row)[disease], axis=1)
            combined_probs = ml_weight * ml_prob + rule_weight * rule_preds
            hybrid_preds.append((combined_probs > 0.5).astype(int))
            hybrid_probs.append(combined_probs)
        return np.array(hybrid_preds).T, np.array(hybrid_probs).T
    except Exception as e:
        logging.error(f'HYBRID PREDICTION ERROR: {e}')
        raise

# EXPLAINABILITY USING FEATURE IMPORTANCE
def generate_explanation(patient_data, feature_importance, feature_names, patient_id, disease, prediction):
    try:
        explanation = f'PATIENT {patient_id} RISK FOR {disease} IS {"HIGH" if prediction == 1 else "LOW"} BECAUSE: '
        if prediction == 1:
            for i, feature in enumerate(feature_names):
                if feature_importance[i] > 0.1:  # THRESHOLD FOR IMPORTANT FEATURES
                    explanation += f'{feature} ({patient_data[feature]}) CONTRIBUTES TO HIGHER RISK. '
        else:
            explanation = f'PATIENT {patient_id} HAS LOW RISK FOR {disease}.'
        return explanation
    except Exception as e:
        logging.error(f'EXPLANATION ERROR: {e}')
        raise

# MAIN FUNCTION
def main():
    try:
        # PREPROCESS DATA
        X, y, X_scaled, scaler, features, targets = preprocess_data(df)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # TRAIN LIGHTWEIGHT MODEL
        rf_model = MultiOutputClassifier(RandomForestClassifier(n_estimators=20, max_depth=3, random_state=42))
        rf_model.fit(X_train_scaled, y_train)
        joblib.dump(rf_model, 'rf_model.pkl')
        logging.info('MODEL SAVED')

        # HYBRID PREDICTIONS
        hybrid_preds, hybrid_probs = hybrid_prediction(rf_model, X_test_scaled, X_test)

        # GENERATE REPORT
        report = []
        feature_importance = rf_model.estimators_[0].feature_importances_
        for i, idx in enumerate(X_test.index):
            patient_id = df.loc[idx, 'PATIENT_ID']
            for j, disease in enumerate(targets):
                explanation = generate_explanation(X_test.iloc[i], feature_importance, features, patient_id, disease, hybrid_preds[i][j])
                report.append({
                    'PATIENT_ID': patient_id,
                    'DISEASE': disease,
                    'RISK_PREDICTION': 'HIGH' if hybrid_preds[i][j] == 1 else 'LOW',
                    'RISK_SCORE': hybrid_probs[i][j],
                    'EXPLANATION': explanation
                })

        # SAVE REPORT
        report_df = pd.DataFrame(report)
        report_df.to_csv('multi_disease_risk_report.csv', index=False)
        logging.info('REPORT GENERATED: MULTI_DISEASE_RISK_REPORT.CSV')

        # EVALUATE
        for i, disease in enumerate(targets):
            logging.info(f'{disease} ACCURACY: {accuracy_score(y_test[disease], hybrid_preds[:, i]):.2f}')

    except Exception as e:
        logging.error(f'MAIN FUNCTION ERROR: {e}')
        raise

# NEW PATIENT PREDICTION
def predict_new_patient(patient_data, model_path='rf_model.pkl', scaler_path='scaler.pkl'):
    try:
        rf_model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        patient_df = pd.DataFrame([patient_data])
        patient_scaled = scaler.transform(patient_df)
        hybrid_preds, hybrid_probs = hybrid_prediction(rf_model, patient_scaled, patient_df)
        feature_importance = rf_model.estimators_[0].feature_importances_
        results = []
        for i, disease in enumerate(['DIABETES', 'HYPERTENSION', 'CARDIOVASCULAR', 'CKD']):
            explanation = generate_explanation(patient_df.iloc[0], feature_importance, patient_df.columns, 'NEW', disease, hybrid_preds[0][i])
            results.append({
                'DISEASE': disease,
                'RISK_PREDICTION': 'HIGH' if hybrid_preds[0][i] == 1 else 'LOW',
                'RISK_SCORE': hybrid_probs[0][i],
                'EXPLANATION': explanation
            })
        result_df = pd.DataFrame(results)
        result_df.to_csv('new_patient_risk_report.csv', index=False)
        logging.info('NEW PATIENT REPORT GENERATED: NEW_PATIENT_RISK_REPORT.CSV')
        return result_df
    except Exception as e:
        logging.error(f'NEW PATIENT PREDICTION ERROR: {e}')
        raise

if __name__ == '__main__':
    main()
    new_patient = {
        'AGE': 55, 'GENDER': 1, 'BMI': 32, 'BP_SYSTOLIC': 150, 'BP_DIASTOLIC': 90,
        'GLUCOSE': 140, 'CHOLESTEROL': 220, 'EGFR': 55, 'FAMILY_HISTORY': 1, 'SMOKING': 0
    }
    result = predict_new_patient(new_patient)
    print(result)

    # END OF FILE
