import mlflow
from  mlflow.tracking import MlflowClient

PROJECT_NAME = "diabetes_prediction_project"
mlflow.set_tracking_uri("http://78.47.114.227:7060")
client = MlflowClient()
mlflow.set_experiment(PROJECT_NAME)

# get experiment id num
experiment_project_id = client.get_experiment_by_name(PROJECT_NAME).experiment_id 

# get all runs as dataframe
df_runs = mlflow.search_runs([experiment_project_id])
best_model_run_id = df_runs.sort_values(by = 'metrics.rmse', ascending= False).iloc[0].run_id 
artifact_path = 'artifact'

URI= f"runs:/{best_model_run_id}/artifacts/{artifact_path}" # URI= "runs:/unid/artifact_path"
print(URI)

registered_version = mlflow.register_model(model_uri=URI, name=PROJECT_NAME) 
registered_version_number = registered_version.version

# Leave short description for registered model
client.update_model_version(
    name=PROJECT_NAME,
    version=registered_version_number,
    description="Best model after hyperparameter tune"
)

# Label Model Stage as Production
client.transition_model_version_stage( name=PROJECT_NAME, version=registered_version_number, stage="Production")

