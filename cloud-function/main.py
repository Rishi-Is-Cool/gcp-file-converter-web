import base64
import datetime
from google.cloud import firestore

db = firestore.Client()

def pubsub_entry_point(event, context):
    attributes = event.get("attributes", {})
    bucket = attributes.get("bucket", "unknown")
    name = attributes.get("name", "unknown")

    print(f"File uploaded: {name} in bucket: {bucket}")

    # Store log in Firestore
    doc_ref = db.collection("file_upload_logs").document()
    doc_ref.set({
        "file_name": name,
        "bucket": bucket,
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

    print("Upload logged to Firestore")