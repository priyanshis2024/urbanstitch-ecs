# Start from the official lightweight Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install OS-level dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code into the container
COPY . .

# Expose the application port
EXPOSE 8000

# Command to start your app — modify this if you use Flask or Django
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Default command (update to match your entry point)
CMD ["python", "main.py"]
