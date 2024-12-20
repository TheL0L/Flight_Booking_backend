# Backend Dockerfile
FROM python:3.12.6-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Set entrypoint
CMD ["sh", "-c", "cd flight_booking && python manage.py migrate && python manage.py runserver 0.0.0.0:8000 && python manage.py populate_flights && python manage.py add_bookings"]
