# OBJECTIVE

The goal of the project is to apply what has been learned during the MLOps Zoomcamp course to build a MLOps pipeline for diabetes prediction. 

# DATASET
I have used diabetes dataset from Kaggle. It can be found from this [link](https://www.kaggle.com/datasets/akshaydattatraykhare/diabetes-dataset?select=diabetes.csv).

The target value is Outcome also for the purpose of using in web services and preprocessing steps, dummy values were generated as new_feature_1 and new_feature_2. Additionally, a patient_id variable was created using uuid.

In addition, I separated the test dataset under the [dataset_folder](https://github.com/iamzeynepcetin/mlops_project/tree/main/dataset) to use it in the web service and workflow orchestration. 

# DEPLOYMENT
The project is implemented on virtual machine Ubuntu 22.04 using AWS. The steps for each section for reproducibility are based on specific AWS configuration and may be different for different platforms (GCP, Azure). To reproduce the project without running into issues, I recommend to use conda environment as shown here. Using any different platform may cause bugs.

You need to create new conda env with this commands:

```python
conda create --name project_env python=3.9
pip install -r project_env_requirements.txt 
```
You need to create .aws folder in the root folder and then you need to fill this file with your aws credentials. After this you need to create bucket named mlflowrunss3 and a folder named mlflow under this bucket. There is a sample [.aws folder](https://github.com/iamzeynepcetin/mlops_project/tree/main/.aws)  Then there are 2 service files running mlflow server and ui. There are supposed to be under etc/systemd/system path. You can copy from [here](https://github.com/iamzeynepcetin/mlops_project/tree/main/service_files) . For the MLflow service files and scripts, you need to change the IP with your own. And please make sure you have project_env and .aws folder.

There is commands for building necessary tools and services.
1. MLflow service files
```bash
mkdir /root/.aws
cd etc/systemd/system
sudo vim mlflow_server.service
sudo vim mlflow_ui.service

sudo systemctl daemon-reload 
sudo systemctl enable mlflow_server.service
sudo systemctl start mlflow_server.service
sudo systemctl status mlflow_server.service 

sudo systemctl daemon-reload 
sudo systemctl enable mlflow_ui.service
sudo systemctl start mlflow_ui.service
sudo systemctl status mlflow_ui.service 
```

1. grafana, postgres, adminer [docker-compose.yml](https://github.com/iamzeynepcetin/mlops_project/blob/main/docker-compose.yml)
```bash
docker-compose up
```

1. airflow (Place it under the /root directory.)
```bash
mkdir airflow
cd airflow
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
mkdir ./dags ./plugins ./logs
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
docker-compose up airflow-init
docker-compose up

Airflow ui default login information
username: airflow
pass: airflow
```
Once ready, the following services will be available:

| Service       | Port         |
| ------------- |:-------------:|
| Airflow UI     | 8080      | 
| Grafana | 3000     |  
| Postgres | 5432     |   
| Adminer     | 8082      |  

# PROJECT STRUCTURE AND EXPLANATION
1. experiment_tracking_and_model_registry:
    1. preprocess_data_and_dump_model.ipynb -> Creates new features and dumps the model with joblib.
    2. register_model_to_mlflow.py -> Registers the local model to MLflow.
    3. hyperparameter_tune.ipynb -> Performs hyperparameter tuning to find the best model.
    4. register_model_after_hyperparametertune.py -> Registers the best model to MLflow after hyperparameter tuning.

2. web-services:
    1. web-service-without-mlflow.py -> flask application that predicts diabetes with local model.
    2. web-service-with-mlflow.py -> flask application that predicts diabetes with registered model from mlflow.
    3. requirements.txt -> Necessary for the dockerfile.
    4. Dockerfile -> The containerized version of the Flask application that predicts diabetes based on the model registered in MLflow.
        There is commands for run the dockerfile.
        ```bash
        docker build --tag diabetes_image .
        sudo docker run --name diabetes_container --restart=on-failure:10 -d -p 9696:9696 diabetes_image
        ```
    **Please don't forget to change the IP with your own.**

3. monitoring_and_workflow:
    1. create_tables_on_postgres.py -> This script creates 2 tables named diabetes_prediction_table, diabetes_scores_table. 
    2. send_predictions_to_db.py -> This script saves predictions to the diabetes_prediction_table. These results are displayed on the Grafana dashboard.
    3. measure_model_scores.py -> This script measures the model scores based on the diabetes_prediction_table and saves them to the diabetes_scores_table. These scores are used for model monitoring on the Grafana dashboard.
    4. diabetes_pipeline_dag -> This script contains an Airflow DAG and consists of 2 tasks. The first task sends daily requests to the Flask application and saves the results to a table. The second task calculates the model score based on the saved results and saves it to another table for daily monitoring on the Grafana dashboard. The script should be located in the /root/airflow/dags path to be visible in the Airflow interface.
4. service_files:
    1. mlflow_ui.service ->  service file that includes MLflow UI
    2. mlflow_server.service -> service file that includes MLflow Server.
    
    Your system should have the project environment installed, and there should be an "mlflowruns" bucket under the "s3" with an "mlflow" folder. Additionally, you need to specify your own machine's IP address after "--host" flag.
5. .aws -> You should fill the example AWS file with your own information and place it under the /root directory. There is one more under web-services path for docker container.