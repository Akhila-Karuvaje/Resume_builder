# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PDF, images, audio, and pycairo
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libcairo2-dev \
    pkg-config \
    libffi-dev \
    ffmpeg \
    libsndfile1 \
    libjpeg62-turbo-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]
