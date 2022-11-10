import os
import flask
from google.cloud import storage
import pickle
from flask import jsonify, request
import pandas as pd

PROJECT = os.getenv('PROJECT')
GCS_BUCKET = os.getenv('GCS_BUCKET')
MODEL_PATH = os.getenv('MODEL_PATH')

# Load model from gcs
storage_client = storage.Client(PROJECT)
bucket = storage_client.bucket(GCS_BUCKET)
blob = bucket.blob(MODEL_PATH + '/model.pkl')
data = blob.download_as_string()
model = pickle.loads(data)

# Initialize server
app = flask.Flask(__name__)

# prediction


@app.route('/prediction', methods=['POST'])
def prediction():
    try:
        feature_vector = request.json['feature_vector'].split(",")
        feature_vector = pd.DataFrame(
            [int(x) for x in feature_vector]).T.to_numpy()
        prediction = model.predict(feature_vector)
        predicted_class = ""

        if (prediction[0] == 0):
            predicted_class = "On Time"

        elif (prediction[0] == 1):
            predicted_class = "Delay"

        return jsonify({'prediction': int(prediction[0]), 'predicted_class': predicted_class}), 200

    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
