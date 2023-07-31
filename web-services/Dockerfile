FROM python:3.9.7

WORKDIR /code
#You need to run this command for get packages from env that you work: pip list --format=freeze > requirements.txt
COPY ./requirements.txt /code/requirements.txt 

COPY ./.aws /root/.aws

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY web-service-with-mlflow.py /code/web-service-with-mlflow.py

CMD ["python" , "/code/web-service-with-mlflow.py"]

#Image build command: docker build --tag diabetes_image .
#Container running command: docker run --name diabetes_container --restart=on-failure:10 -d -p 9696:9696 diabetes_image