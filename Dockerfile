FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    libreoffice \
    poppler-utils \
    python3-dev \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean

# Create app directory
WORKDIR /app

# Copy files
COPY . /app

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]