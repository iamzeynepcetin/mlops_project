import joblib
import pandas as pd
from flask import Flask, request, jsonify
import mlflow
from  mlflow.tracking import MlflowClient


PROJECT_NAME = f"diabetes_prediction_project"
mlflow.set_tracking_uri("http://78.47.114.227:7060")
mlflow.set_experiment(experiment_name=PROJECT_NAME)
# Get registered(production) model from mlflow 
client = MlflowClient()
registered_model_name=f"name='{PROJECT_NAME}'"
registered_model_uri = client.search_model_versions(registered_model_name)[-1].source
loaded_model = mlflow.lightgbm.load_model(model_uri=registered_model_uri)
print(loaded_model.get_params())

def preprocess_for_new_features(test):
    new_feature_1 = test['BMI'] / test['DiabetesPedigreeFunction']
    new_feature_2 = test['Glucose'] + test['BloodPressure']

    test["new_feature_1"] = new_feature_1
    test["new_feature_2"] = new_feature_2
    test.pop("Patient_id")
    return test

def predict(X):
    preds = loaded_model.predict([pd.Series(X)])
    return bool(preds[0])


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