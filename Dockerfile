# Use Python 3.10
FROM python:3.10-slim

# Set env vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set workdir
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Cloud Run expects app to listen on PORT
ENV PORT=8080
EXPOSE 8080

# Start Flask app
CMD ["python", "app.py"]
