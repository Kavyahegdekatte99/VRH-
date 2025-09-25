#!/usr/bin/env python3
"""
Local Production server for VINAYAK REXINE HOUSE Catalog System
Production-grade server for local testing and development
"""

import os
import sys
from waitress import serve
from app import app

def main():
    """Run the application with Waitress on localhost"""
    
    # Set production environment
    os.environ['FLASK_ENV'] = 'production'
    
    # Disable debug mode for production
    app.debug = False
    
    # Configure for local access
    host = '127.0.0.1'  # localhost only
    port = int(os.environ.get('PORT', 5000))
    
    print("=" * 60)
    print("🚀 VINAYAK REXINE HOUSE - Local Production Server")
    print("=" * 60)
    print(f"📡 Server: Waitress WSGI Server (Production)")
    print(f"🌐 Host: {host} (localhost)")
    print(f"🔌 Port: {port}")
    print(f"🔗 Access URL: http://{host}:{port}")
    print(f"🔗 Alternative: http://localhost:{port}")
    print(f"🛡️ Security: Production Mode (Debug Disabled)")
    print("=" * 60)
    print("✅ Server ready for local production testing!")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Start Waitress server
        serve(
            app,
            host=host,
            port=port,
            threads=4,  # Handle multiple requests simultaneously
            connection_limit=100,  # Limit concurrent connections
            cleanup_interval=30,  # Clean up connections regularly
            channel_timeout=120,  # Timeout for slow clients
            url_scheme='http'
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()