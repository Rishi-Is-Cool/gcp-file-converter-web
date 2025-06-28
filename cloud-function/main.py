import datetime
from google.cloud import firestore, storage
import fitz  # PyMuPDF

print("📦 Cloud Function loaded successfully")

db = firestore.Client()
storage_client = storage.Client()

def pubsub_entry_point(event, context):
    attributes = event.get("attributes", {})
    bucket_name = attributes.get("bucket")
    file_name = attributes.get("name")

    if not bucket_name or not file_name:
        print("❌ Missing bucket or filename in Pub/Sub attributes.")
        return

    print(f"🚀 Triggered for file: {file_name} in bucket: {bucket_name}")

    # Log object
    log_entry = {
        "file_name": file_name,
        "bucket": bucket_name,
        "timestamp": datetime.datetime.utcnow().isoformat(),
    }

    # Only handle PDFs
    if file_name.lower().endswith(".pdf"):
        try:
            print("📄 It's a PDF. Downloading...")
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(file_name)
            content = blob.download_as_bytes()
            print("✅ Downloaded. Extracting text...")

            doc = fitz.open(stream=content, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()

            log_entry["extracted_text"] = text[:5000]  # limit for Firestore
            print("🧠 Text extracted successfully.")

        except Exception as e:
            log_entry["error"] = f"PDF processing failed: {str(e)}"
            print(f"❌ PDF extraction error: {e}")
    else:
        log_entry["note"] = "Not a PDF file — skipped text extraction."
        print("⚠️ Not a PDF. Skipping extraction.")

    # Save to Firestore
    try:
        db.collection("file_upload_logs").add(log_entry)
        print("✅ Log entry written to Firestore.")
    except Exception as e:
        print(f"❌ Firestore write failed: {e}")
