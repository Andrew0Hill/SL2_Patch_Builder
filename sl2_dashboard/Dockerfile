FROM python:3.9-slim

ENV PYTHONUNBUFFERED True

# Set working directory
WORKDIR /app

# Copy files for SL2 module and dashboard
COPY sl2/ ./sl2
COPY sl2_dashboard/ ./

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run dashboard
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app_server


