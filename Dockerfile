# Use slim Python base image
FROM python:3.9-slim

# Install LibreOffice
RUN apt-get update && apt-get install -y \
    libreoffice \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy app files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]