FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system tools for gRPC
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your project files
COPY . .

# Automatically compile the proto file
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. secure_mail.proto

EXPOSE 50051

CMD ["python", "main.py"]
