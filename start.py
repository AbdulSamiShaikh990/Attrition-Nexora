#!/usr/bin/env python3
"""
Combined startup script for Streamlit + Flask API
Runs both applications simultaneously
"""

import os
import sys
import subprocess
import threading
import time

def run_flask_api():
    """Run Flask API on port 5000"""
    print("🚀 Starting Flask API on port 5000")
    try:
        # Use gunicorn for production
        cmd = [
            'gunicorn',
            '--bind', '0.0.0.0:5000',
            '--workers', '2',
            '--timeout', '120',
            '--access-logfile', '-',
            '--error-logfile', '-',
            'api:app'
        ]
        print(f"📋 Flask Command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Flask API error: {e}")
    except Exception as e:
        print(f"❌ Flask startup error: {e}")

def run_streamlit():
    """Run Streamlit app on main PORT"""
    # Get PORT from environment, default to 8501
    port = os.environ.get('PORT', '8501')
    
    print(f"🚀 Starting Streamlit app on port {port}")
    
    # Build the streamlit command
    cmd = [
        'streamlit', 'run', 'app.py',
        '--server.port', port,
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--server.enableCORS', 'true'
    ]
    
    print(f"📋 Streamlit Command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Streamlit error: {e}")
    except Exception as e:
        print(f"❌ Streamlit startup error: {e}")

def main():
    print("=" * 60)
    print("🚀 STARTING ATTRITION-NEXORA APPLICATION")
    print("=" * 60)
    
    # Start Flask API in a background thread
    flask_thread = threading.Thread(target=run_flask_api, daemon=True)
    flask_thread.start()
    
    # Give Flask API time to start
    print("⏳ Waiting for Flask API to initialize...")
    time.sleep(3)
    
    # Run Streamlit in main thread
    print("\n" + "=" * 60)
    try:
        run_streamlit()
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested")
        sys.exit(0)

if __name__ == "__main__":
    main()