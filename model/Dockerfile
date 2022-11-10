FROM python

WORKDIR /model
COPY . .
ENV MLFLOW_TRACKING_URI http://34.123.167.230:5000
RUN pip install -r requirements.txt
CMD ["python", "main.py"]