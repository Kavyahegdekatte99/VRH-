#!/usr/bin/env python3
"""
Production server for VINAYAK REXINE HOUSE Catalog System
Uses Waitress WSGI server for production deployment
"""

import os
import sys
from waitress import serve
from app import app

def main():
    """Run the application with Waitress production server"""
    
    # Set production environment
    os.environ['FLASK_ENV'] = 'production'
    
    # Disable debug mode for production
    app.debug = False
    
    # Configure host and port
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    # Display URL - use localhost for local access
    display_url = f"http://localhost:{port}" if host == '0.0.0.0' else f"http://{host}:{port}"
    
    print("=" * 60)
    print("🚀 VINAYAK REXINE HOUSE - Production Server Starting")
    print("=" * 60)
    print(f"📡 Server: Waitress WSGI Server (Production)")
    print(f"🌐 Binding to: {host}:{port}")
    print(f"🔗 Access URL: {display_url}")
    print(f"🛡️ Security: Production Mode (Debug Disabled)")
    print("=" * 60)
    print("✅ Server ready for production traffic!")
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