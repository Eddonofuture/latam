FROM python:3.9-slim

ENV PORT 8080
ENV PROJECT='fveloso-latam'
ENV GCS_BUCKET='fveloso_mlflow_model_repository'
ENV MODEL_PATH='1/a806205c719142659a3e6138c21218df/artifacts/model'

COPY . ./

RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 4 api:app