#!/bin/bash

# Run Flask API with gunicorn
PORT=${PORT:-5000}

echo "🚀 Starting Attrition API on port $PORT"

gunicorn \
  --bind 0.0.0.0:$PORT \
  --workers 2 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  --log-level debug \
  api:app

echo "✅ API Started"
