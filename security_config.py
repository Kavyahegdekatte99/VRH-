# Security Configuration for VINAYAK REXINE HOUSE Catalog System

import os
from datetime import timedelta

class SecurityConfig:
    """Security-focused configuration settings"""
    
    # Basic Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour
    
    # Session Security
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # File Upload Security
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'wmv'}
    
    # Database Security
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'catalog.db'
    DATABASE_QUERY_TIMEOUT = 30  # seconds
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = "memory://"
    RATELIMIT_DEFAULT = "100 per hour"
    RATELIMIT_LOGIN = "10 per minute"
    
    # Content Security Policy
    CSP_DIRECTIVES = {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline' https://cdn.jsdelivr.net",
        'style-src': "'self' 'unsafe-inline' https://cdn.jsdelivr.net",
        'img-src': "'self' data: https:",
        'font-src': "'self' https://cdn.jsdelivr.net",
        'connect-src': "'self'",
        'frame-ancestors': "'none'",
        'base-uri': "'self'",
        'form-action': "'self'"
    }
    
    # Security Headers
    SECURITY_HEADERS = {
        'X-Frame-Options': 'DENY',
        'X-Content-Type-Options': 'nosniff',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Referrer-Policy': 'strict-origin-when-cross-origin'
    }
    
    # Password Policy
    MIN_PASSWORD_LENGTH = 8
    REQUIRE_UPPERCASE = False
    REQUIRE_LOWERCASE = False
    REQUIRE_DIGITS = False
    REQUIRE_SPECIAL_CHARS = False
    
    # Input Validation
    MAX_EMAIL_LENGTH = 254
    MAX_NAME_LENGTH = 100
    MAX_DESCRIPTION_LENGTH = 1000
    MAX_FILENAME_LENGTH = 255

class DevelopmentConfig(SecurityConfig):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False

class ProductionConfig(SecurityConfig):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    
    # Enhanced production security
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")
    
    # Database configuration for production
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable must be set in production")

class TestingConfig(SecurityConfig):
    """Testing environment configuration"""
    TESTING = True
    DEBUG = True
    DATABASE_URL = ':memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.environ.get('TEST_SECRET_KEY', os.urandom(24).hex())

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}