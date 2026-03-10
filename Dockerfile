FROM python:3.11-slim

WORKDIR /code

# تثبيت أدوات النظام المطلوبة للـ gRPC
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev && rm -rf /var/lib/apt/lists/*

# تحديث pip لأحدث نسخة
RUN pip install --no-cache-dir --upgrade pip

# ⚠️ السر هنا: مسح أي نسخة قديمة وتثبيت النسخة المطلوبة غصب عن أي حد
RUN pip uninstall -y grpcio grpcio-tools
RUN pip install --no-cache-dir grpcio==1.78.0 grpcio-tools==1.78.0

# نسخ الـ requirements وتثبيت الباقي
COPY requirements.txt .
# تأكد إن requirements.txt مفيهاش grpcio خالص
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /code/app

WORKDIR /code/app

# متغير بيئة لضمان إن بايثون بيشوف المكتبات الجديدة
ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages

CMD ["python", "main.py"]