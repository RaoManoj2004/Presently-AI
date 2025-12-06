# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies required for the app
# libreoffice: for converting PPT to PDF
# poppler-utils: for converting PDF to images
# ffmpeg: for video processing
RUN apt-get update && apt-get install -y \
    libreoffice \
    poppler-utils \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Create temp directories if they don't exist
RUN mkdir -p temp/images temp/audio temp/slide_images

# Expose the port the app runs on
EXPOSE 5000

# Define environment variable
ENV PORT=5000
ENV PYTHONUNBUFFERED=1

# Run the application using Gunicorn
# --chdir web: Change to the 'web' directory before loading the app
# app:app: Load the 'app' object from 'app.py'
CMD gunicorn --chdir web --bind 0.0.0.0:$PORT app:app --timeout 120
