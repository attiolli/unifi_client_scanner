# Use the official Python image from Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install python-dotenv --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY known_clients.txt .
COPY app.py .

# Define the command to run your application
CMD ["python", "app.py"]
