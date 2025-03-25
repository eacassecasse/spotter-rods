# Base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
WORKDIR /app
COPY . .

# Run migrations and collectstatic (adjust as needed)
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Entrypoint
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "spotterrods.wsgi:application"]