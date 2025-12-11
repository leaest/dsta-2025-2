FROM python:3.10-slim
WORKDIR /app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copies everything else in the folder
COPY . .

# Expose the folder where models will be saved
VOLUME ["/app/models"]

# Run main.py by default when the container starts
CMD ["python", "main.py"]