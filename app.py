from flask import Flask, request, render_template
from google.cloud import storage, pubsub_v1
from google.cloud import firestore
import os

app = Flask(__name__)

# GCP Clients
storage_client = storage.Client()
publisher = pubsub_v1.PublisherClient()
db = firestore.Client()

# Env vars (set in Cloud Run or locally)
PROJECT_ID = "sm-vita-project"  # Replace with your actual project ID
TOPIC_NAME = "new-file-upload"

@app.route("/logs")
def show_logs():
    try:
        docs = db.collection("file_upload_logs").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
        logs = []

        for doc in docs:
            data = doc.to_dict()
            logs.append({
                "file_name": data.get("file_name", "N/A"),
                "timestamp": data.get("timestamp", "N/A"),
                "text": data.get("extracted_text", data.get("note", data.get("error", "No content")))
            })

        return render_template("logs.html", logs=logs)
    
    except Exception as e:
        return f"Failed to load logs: {str(e)}", 500

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            bucket_name = f"uploaded-files-{PROJECT_ID}"
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(file.filename)
            blob.upload_from_string(file.read(), content_type=file.content_type)

            topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
            publisher.publish(
                topic_path,
                b"",
                bucket=bucket_name,
                name=file.filename
            )

            return render_template("index.html", success=True)

    return render_template("index.html", success=False)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Cloud Run provides $PORT
    app.run(host="0.0.0.0", port=port)
