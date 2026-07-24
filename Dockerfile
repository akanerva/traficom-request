# Use an official Python image
FROM python:3.13-slim

# Prevent Python from writing .pyc files and buffer stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy only requirements first (better Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create logs directory
RUN mkdir -p /app/logs

# Declare it as a volume
VOLUME ["/app/logs"]

# Run the script
CMD ["python", "mqtt.py"]
