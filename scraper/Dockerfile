FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set Firebase credentials path
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/service-account.json"

# Cloud Run requires a port to listen on
ENV PORT 8080

# We'll run the FastAPI app which handles health checks and the scraper
CMD ["python", "main.py"]
