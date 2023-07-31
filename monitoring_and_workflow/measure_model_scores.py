import psycopg2
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
import datetime

conn = psycopg2.connect(database = "postgres", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "example",
                        port = 5432)
cur = conn.cursor()


data = pd.read_sql("""SELECT * FROM diabetes_prediction_table;
            """, conn)

accuracy_score = accuracy_score(data['y_true'], data['prediction'])
f1_score = f1_score(data['y_true'], data['prediction'])
precision = precision_score(data['y_true'], data['prediction'])
recall = recall_score(data['y_true'], data['prediction'])

# datetime object containing current date and time
insert_date =datetime.datetime.now()

cur.execute(f"INSERT INTO diabetes_scores_table(insert_time, accuracy_score, f1_score, precision, recall) VALUES('{insert_date}', '{accuracy_score}','{f1_score}','{precision}','{recall}')");
conn.commit()

cur.close()
conn.close()