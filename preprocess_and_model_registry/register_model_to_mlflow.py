import mlflow
from  mlflow.tracking import MlflowClient
import joblib

#model yüklenir

pkl_filename = f'diabetes_model.pkl'
loaded_model = joblib.load(pkl_filename)

PROJECT_NAME = "diabetes_prediction_project"
mlflow.set_tracking_uri("http://78.47.114.227:7060")
mlflow.create_experiment(name=PROJECT_NAME) #experiment creation
client = MlflowClient()
mlflow.set_experiment(PROJECT_NAME)
mlflow.lightgbm.log_model(loaded_model, artifact_path=r"artifact", registered_model_name=PROJECT_NAME)