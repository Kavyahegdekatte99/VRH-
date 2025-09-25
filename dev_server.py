#!/usr/bin/env python3
"""
Development server for VINAYAK REXINE HOUSE Catalog System
⚠️ DEVELOPMENT ONLY - DO NOT USE IN PRODUCTION ⚠️
"""

import os
from app import app, init_db

def main():
    """Run the application in development mode"""
    
    print("=" * 70)
    print("🔧 VINAYAK REXINE HOUSE - Development Server Starting")
    print("=" * 70)
    print("⚠️  WARNING: This is a DEVELOPMENT server!")
    print("⚠️  Do NOT use this in production!")
    print("⚠️  For production, use: python production_server.py")
    print("=" * 70)
    print(f"🌐 Development URL: http://127.0.0.1:5000")
    print(f"🔧 Debug Mode: Enabled")
    print(f"🔄 Auto-reload: Enabled")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 70)
    
    # Initialize database
    init_db()
    
    # Run development server
    app.run(
        debug=True,
        host='127.0.0.1',
        port=5000,
        use_reloader=True
    )

if __name__ == '__main__':
    main()