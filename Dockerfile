# Build from monorepo root:
#   docker build -f SecureMail-Ai/Dockerfile -t securemail-ai .

FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir grpcio==1.78.0 grpcio-tools==1.78.0

COPY SecureMail-Ai/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY SecureMail-Ai/app /code/app
WORKDIR /code/app

ENV PYTHONPATH=/code/app:/code/app/protos
ENV GRPC_PORT=50051

EXPOSE 50051
CMD ["python", "main.py"]
