import psycopg2

conn = psycopg2.connect(database = "postgres", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "example",
                        port = 5432)

# Open a cursor to perform database operations
cur = conn.cursor()
# Execute a command: create diabetes_prediction_table table
cur.execute("""CREATE TABLE diabetes_prediction_table(
            patient_id VARCHAR (50) UNIQUE NOT NULL,
            y_true BOOLEAN,
            prediction BOOLEAN);
            """)
# Make the changes to the database persistent
conn.commit()

# Execute a command: create diabetes_scores_table table
cur.execute("""CREATE TABLE diabetes_scores_table(
            insert_time TIMESTAMP,
            accuracy_score FLOAT4,
            f1_score FLOAT4,
            precision FLOAT4,
            recall FLOAT4);
            """)
conn.commit()

# Close cursor and communication with the database
cur.close()
conn.close()