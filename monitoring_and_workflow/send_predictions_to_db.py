import psycopg2
import pandas as pd
import requests


conn = psycopg2.connect(database = "postgres", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "example",
                        port = 5432)

cur = conn.cursor()

test_data = pd.read_csv('/root/mlops_project/dataset/test.csv')

for i in range(len(test_data)):
    y_true = test_data.iloc[i]['Outcome']
    test_req = test_data.iloc[i].to_dict()
    del test_req['Outcome']

    url= 'http://localhost:9696/predict'
    response= requests.post(url, json = test_req)
    response = response.json()

    patient_id = response['Patient_id']
    prediction = response['is_diabet']

    cur.execute(f"INSERT INTO diabetes_prediction_table(patient_id, y_true, prediction) VALUES('{patient_id}','{y_true}','{prediction}')");
    conn.commit()

cur.close()
conn.close()
