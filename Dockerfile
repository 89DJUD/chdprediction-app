# Dockerfile for the Streamlit CHD app
# Use a light python image (matches the local venv Python 3.13)
FROM python:3.13-slim

# Set a working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt /app/requirements.txt

# Install system deps for some packages (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the app content
COPY . /app

# Expose Streamlit port
EXPOSE 8501

# Forward logs to docker logs
ENV PYTHONUNBUFFERED=1

# Command to run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
