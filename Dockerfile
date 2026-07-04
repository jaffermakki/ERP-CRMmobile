# Use an official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (required for PostgreSQL and building packages)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Referencing your original requirements structure
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application project
COPY . .

# Expose the port the app runs on
EXPOSE 8000
