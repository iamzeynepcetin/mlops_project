from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator


email_test_list = ['YOUR_MAIL_ADDRESS']

default_args = {
  'owner': 'zeynep',
  'start_date': datetime(2023, 7, 27, 21),
  'email': email_test_list,
  'email_on_failure': True,
  'email_on_retry': False,
  'retries': 0
}

dag = DAG('diabetes_pipeline',
        schedule_interval='24 4 * * *' ,
        catchup =False,
        default_args=default_args
    )

get_daily_predictions = BashOperator(
task_id='get_daily_predictions',
bash_command='/root/anaconda3/envs/project_env/bin/python /root/zeynep/mlops_zoomcamp_project/monitoring-and-workflow/send_predictions_to_db.py',
dag=dag)

get_daily_scores = BashOperator(
task_id='get_daily_scores',
bash_command='/root/anaconda3/envs/project_env/bin/python /root/zeynep/mlops_zoomcamp_project/monitoring-and-workflow/measure_model_scores.py',
dag=dag)

get_daily_predictions >> get_daily_scores

dag.doc_md = __doc__
dag.doc_md = """
 These tasks saves predictions to diabetes_prediction_table then measures daily model scores and saves to diabetes_scores_table.
"""