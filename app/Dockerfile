FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# The model will be mounted from a Docker volume in /app/models
VOLUME ["/app/models"]

# Run the main script when container starts
CMD ["python", "main.py"]
