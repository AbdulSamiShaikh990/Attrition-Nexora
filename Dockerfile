FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port (Railway will set PORT dynamically)
EXPOSE $PORT

# Run Streamlit using our startup script
CMD ["python", "start.py"]
