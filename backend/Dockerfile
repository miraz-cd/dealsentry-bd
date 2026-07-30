FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y     wget     gnupg     libgconf-2-4     libatk1.0-0     libatk-bridge2.0-0     libgdk-pixbuf2.0-0     libgtk-3-0     libgbm1     libnss3     libxss1     libasound2     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium

COPY app/ ./app/
COPY seed_data.py .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
