import joblib
import pandas as pd
from flask import Flask, request, jsonify


model = joblib.load('/root/mlops_project/preprocess_data_and_save_pickle/diabetes_model.pkl')

def preprocess_for_new_features(test):
    new_feature_1 = test['BMI'] / test['DiabetesPedigreeFunction']
    new_feature_2 = test['Glucose'] + test['BloodPressure']

    test["new_feature_1"] = new_feature_1
    test["new_feature_2"] = new_feature_2
    test.pop("Patient_id")
    return test

def predict(X):
    preds = model.predict([pd.Series(X)])
    return float(preds[0])


app = Flask('diabet-prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    test = request.get_json()
    patient_id = test['Patient_id']
    preprocessed= preprocess_for_new_features(test)
    pred= predict(preprocessed)

    result = {
        'Patient_id' : patient_id,
        'is_diabet': pred
    }
    print(result)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0', port=9696)

"""
It can run from terminal with this command: gunicorn --bind= 0.0.0.0:9696 predict:app
"""
