# Deployment Guide - VINAYAK REXINE HOUSE

## Server Types

### 🔧 Development Server (Current)
- **File**: `python app.py` or `python dev_server.py`
- **Purpose**: Development and testing only
- **Features**: Debug mode, auto-reload, detailed error pages
- **Warning**: ⚠️ NOT for production use!

### 🚀 Production Servers
- **Local Production**: `python local_production_server.py` - Production server for local testing
- **Full Production**: `python production_server.py` - Production server for deployment
- **Features**: Multi-threaded, optimized, secure
- **Server**: Waitress WSGI server

## Quick Start

### For Development:
```bash
python dev_server.py
```
Access at: http://127.0.0.1:5000

### For Local Production Testing:
```bash
python local_production_server.py
```
Access at: http://127.0.0.1:5000 or http://localhost:5000

### For Full Production Deployment:
```bash
python production_server.py
```
Binds to all interfaces (0.0.0.0), access via server IP

## Environment Variables (Optional)

```bash
# Production server configuration
set HOST=0.0.0.0
set PORT=8080
set SECRET_KEY=your-production-secret-key

# Then run
python production_server.py
```

## Production Deployment Options

### 1. Simple Production (Windows)
```bash
python production_server.py
```

### 2. With Custom Port
```bash
set PORT=8080
python production_server.py
```

### 3. Background Service (Windows)
```bash
# Using nssm (Non-Sucking Service Manager)
nssm install VinayakRexineHouse "C:\path\to\python.exe" "C:\catalogue_website\production_server.py"
nssm start VinayakRexineHouse
```

### 4. Cloud Deployment
- **Heroku**: Use `Procfile` with `web: python production_server.py`
- **AWS**: Deploy with Elastic Beanstalk
- **Digital Ocean**: Use App Platform
- **Railway**: Direct deployment from Git

## Security Checklist for Production

✅ Use `production_server.py` instead of `app.py`
✅ Set strong SECRET_KEY environment variable
✅ Disable debug mode (done automatically)
✅ Use HTTPS (configure reverse proxy)
✅ Set up firewall rules
✅ Regular security updates
✅ Monitor server logs

## Performance Tips

- Use a reverse proxy (Nginx/Apache) for static files
- Set up database connection pooling for high traffic
- Configure caching (Redis/Memcached)
- Use CDN for static assets
- Monitor with tools like New Relic or DataDog