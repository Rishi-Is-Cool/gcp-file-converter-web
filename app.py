from flask import Flask, request, render_template
from google.cloud import storage, pubsub_v1
import os

app = Flask(__name__)

# Configure clients
storage_client = storage.Client()
publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
TOPIC_NAME = "new-file-upload"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            # Upload to Cloud Storage
            bucket = storage_client.bucket("uploaded-files-" + PROJECT_ID)
            blob = bucket.blob(file.filename)
            blob.upload_from_string(file.read(), content_type=file.content_type)
            
            # Trigger conversion via Pub/Sub
            topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
            publisher.publish(topic_path, attributes={
                "bucket": "uploaded-files-" + PROJECT_ID,
                "name": file.filename
            })
            
            return "File uploaded! Conversion started."
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))