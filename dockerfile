# Base Image

FROM python:3.10-slim

# Set the working directory

WORKDIR /app

# copy the requirements file

COPY requirements.txt .

# Install the dependencies

RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code

COPY . .

# Expose the port

EXPOSE 5000

# Run the application

CMD ["python", "app.py"]


# Build the Docker image

# docker build -t diabetes-app:1.0 .