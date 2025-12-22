FROM python:3.10-slim
WORKDIR /app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copies everything else in the folder
COPY . .

# Enable the entrypoint script
RUN chmod +x /app/docker_entrypoint.sh

# Expose the folder where models will be saved
VOLUME ["/app/models"]

# Set the entrypoint for the W&B login
ENTRYPOINT ["/app/docker_entrypoint.sh"]

# Run main.py by default when the container starts
CMD ["python", "main.py"]