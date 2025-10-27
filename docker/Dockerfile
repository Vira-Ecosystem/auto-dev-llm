# Dockerfile برای Auto-Dev-LLM
FROM python:3.11-slim

# نصب وابستگی‌های سیستمی
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# تنظیم working directory
WORKDIR /app

# کپی requirements
COPY requirements.txt .

# نصب کتابخانه‌های Python
RUN pip install --no-cache-dir -r requirements.txt

# کپی کل پروژه
COPY . .

# ایجاد پوشه‌های مورد نیاز
RUN mkdir -p logs backups specs models

# تنظیم متغیرهای محیطی
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# نقطه ورود
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]