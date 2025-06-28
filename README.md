# 📄 GCP File Converter Web

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)](https://www.python.org/downloads/)
[![GCP](https://img.shields.io/badge/Google_Cloud-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/)
[![Flask](https://img.shields.io/badge/flask-%23000.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

A scalable and serverless PDF processing platform built on **Google Cloud Platform (GCP)**. This application enables users to upload PDF files through a web interface, automatically extracts text content from the first few pages, and stores both files and extracted insights in Firestore.

## ✨ Features

- 🌐 **Web-based File Upload**: Intuitive interface for PDF file uploads
- ☁️ **Cloud Storage Integration**: Secure file storage using Google Cloud Storage
- ⚡ **Event-driven Processing**: Automatic PDF processing triggered by Pub/Sub events
- 📋 **Text Extraction**: Intelligent text extraction from PDF documents using Cloud Functions
- 💾 **Data Persistence**: Metadata and extracted content stored in Firestore
- 📊 **Activity Dashboard**: User-friendly interface to view processing logs and results

## 📸 Screenshots

### Upload Interface
![Upload UI](images/home.png)

### Logs Dashboard
![Logs UI](images/logs.png)

## 🏗️ Architecture

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │
┌──────▼──────┐
│ Flask Web   │
│ App (Cloud  │
│ Run)        │
└──────┬──────┘
       │
┌──────▼──────┐
│ Cloud       │
│ Storage     │
│ Bucket      │
└──────┬──────┘
       │
┌──────▼──────┐
│ Pub/Sub     │
│ Topic       │
└──────┬──────┘
       │
┌──────▼──────┐
│ Cloud       │
│ Function    │
│ (PDF        │
│ Processor)  │
└──────┬──────┘
       │
┌──────▼──────┐
│ Firestore   │
│ Database    │
└─────────────┘

![Upload UI](images/gcp1.png)

![Logs UI](images/gcp2.png)

```

## 📁 Project Structure

```
smart-feedback-analyzer/
│
├── app.py                  # Flask backend entry point
├── Dockerfile              # Cloud Run deployment configuration
├── requirements.txt        # Python dependencies
│
├── templates/              # HTML templates
│   ├── index.html         # Upload page template
│   └── logs.html          # Logs dashboard template
│
├── cloud-function/         # PDF processing logic
│   └── main.py            # Cloud Function source code
│
├── screenshots/           # UI screenshots
│   ├── upload-ui.png
│   └── logs-ui.png
│
└── README.md              # Project documentation
```

## 🛠️ Technology Stack

### 🎨 Frontend
- HTML5 & CSS3
- Jinja2 templating engine

### ⚙️ Backend
- Python Flask framework
- PyMuPDF (fitz) for PDF processing

### ☁️ Google Cloud Services
- **Cloud Run**: Serverless container deployment
- **Cloud Storage**: File storage and management
- **Pub/Sub**: Event-driven messaging
- **Cloud Functions**: Serverless compute for PDF processing
- **Firestore**: NoSQL document database

### 🚀 Development & Deployment
- Docker for containerization
- Google Cloud SDK for deployment

## 💻 Local Development

### 📋 Prerequisites
- Python 3.8+
- Google Cloud SDK
- Git

### 🚀 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/smart-feedback-analyzer.git
   cd smart-feedback-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your browser and navigate to `http://localhost:8080`

## 🌩️ Deployment to Google Cloud

### Step 1: Enable Required APIs
```bash
gcloud services enable run.googleapis.com \
    pubsub.googleapis.com \
    firestore.googleapis.com \
    cloudfunctions.googleapis.com
```

### Step 2: Create Cloud Storage Bucket
```bash
gsutil mb -l asia-south1 gs://uploaded-files-sm-vita-project
```

### Step 3: Deploy Cloud Function
```bash
cd cloud-function
gcloud functions deploy pubsub_entry_point \
  --runtime python310 \
  --trigger-topic new-file-upload \
  --entry-point pubsub_entry_point \
  --region asia-south1 \
  --project sm-vita-project \
  --source=.
```

### Step 4: Deploy Web Application
```bash
cd ..
gcloud run deploy smart-feedback-ui \
  --source . \
  --region asia-south1 \
  --platform managed \
  --allow-unauthenticated \
  --project sm-vita-project
```

## ⚙️ Configuration

Ensure the following environment variables are configured:
- `GOOGLE_CLOUD_PROJECT`: Your GCP project ID
- `STORAGE_BUCKET`: Cloud Storage bucket name
- `PUBSUB_TOPIC`: Pub/Sub topic for file processing events

## 🚀 Future Enhancements

- 🔐 **Authentication**: Implement Firebase Authentication for secure user access
- 🧠 **Sentiment Analysis**: Integrate Cloud Natural Language API for content analysis
- 📊 **Analytics Dashboard**: Add BigQuery integration for historical trend analysis
- 👨‍💼 **Admin Panel**: Develop administrative interface for user and file management
- 📄 **Multi-format Support**: Extend support to additional document formats

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Rishikesh**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=white)](https://linkedin.com/in/your-profile)
[![GitHub](https://img.shields.io/badge/GitHub-100000?logo=github&logoColor=white)](https://github.com/your-username)

---

<div align="center">
  <p><em>Built using Google Cloud Platform</em></p>
  
  <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg" alt="Made with Python">
  <img src="https://img.shields.io/badge/Powered%20by-Google%20Cloud-4285F4.svg" alt="Powered by Google Cloud">
</div>