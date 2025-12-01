# ================================
# BASE IMAGE
# ================================
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ================================
# SYSTEM DEPS
# ================================
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ================================
# WORKDIR
# ================================
WORKDIR /app

# ================================
# INSTALL PIP DEPS
# ================================
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# ================================
# COPY PROJECT
# ================================
COPY . /app/

# ================================
# DEFAULT CMD
# ================================
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
