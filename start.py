#!/usr/bin/env python3
"""
Railway Streamlit Startup Script
Handles PORT environment variable properly
"""

import os
import sys
import subprocess

def main():
    # Get PORT from environment, default to 8501
    port = os.environ.get('PORT', '8501')
    
    print(f"🚀 Starting Streamlit app on port {port}")
    
    # Build the streamlit command
    cmd = [
        'streamlit', 'run', 'app.py',
        '--server.port', port,
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--server.enableCORS', 'false'
    ]
    
    print(f"📋 Command: {' '.join(cmd)}")
    
    # Execute streamlit
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting Streamlit: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("🛑 Shutdown requested")
        sys.exit(0)

if __name__ == "__main__":
    main()