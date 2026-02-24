#!/bin/bash

# Get the PORT from environment, default to 8501 if not set
PORT=${PORT:-8501}

echo "🚀 Starting Streamlit app on port $PORT"

# Run streamlit with the correct port
exec streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false