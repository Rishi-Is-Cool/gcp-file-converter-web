from flask import Flask, request, render_template
from google.cloud import storage, pubsub_v1
import os

app = Flask(__name__)

# GCP Clients
storage_client = storage.Client()
publisher = pubsub_v1.PublisherClient()

# Env vars (set in Cloud Run or locally)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
TOPIC_NAME = os.getenv("TOPIC_ID", "new-file-upload")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            # Upload to Cloud Storage
            bucket_name = f"uploaded-files-{PROJECT_ID}"
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(file.filename)
            blob.upload_from_string(file.read(), content_type=file.content_type)

            # Publish to Pub/Sub
            topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
            publisher.publish(topic_path, attributes={
                "bucket": bucket_name,
                "name": file.filename
            })

            return "✅ File uploaded and message published!"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
