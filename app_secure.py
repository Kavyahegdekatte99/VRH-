"""
VINAYAK REXINE HOUSE - Product Catalog System
Secure Flask application with proper error handling and code quality standards.
"""

import os
import logging
from datetime import datetime
from contextlib import contextmanager
from typing import Optional, Dict, Any, List

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security configurations
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'wmv'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
DATABASE_PATH = 'catalog.db'
UPLOAD_FOLDER = 'uploads'

def create_app() -> Flask:
    """Application factory pattern for better testability."""
    app = Flask(__name__)
    
    # Security configuration
    app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
    app.config['WTF_CSRF_ENABLED'] = True
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    return app

app = create_app()

class DatabaseManager:
    """Database operations with proper connection management."""
    
    @staticmethod
    @contextmanager
    def get_db_connection():
        """Context manager for database connections."""
        conn = None
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def init_database() -> None:
        """Initialize database with proper error handling."""
        try:
            with DatabaseManager.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        is_admin BOOLEAN DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Products table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        category TEXT,
                        price REAL CHECK(price >= 0),
                        image_url TEXT,
                        pdf_url TEXT,
                        video_url TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Starred products table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS starred_products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                        FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE,
                        UNIQUE(user_id, product_id)
                    )
                ''')
                
                # Create admin user if not exists
                DatabaseManager._create_admin_user(cursor)
                conn.commit()
                logger.info("Database initialized successfully")
                
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    @staticmethod
    def _create_admin_user(cursor) -> None:
        """Create default admin user."""
        admin_email = 'admin@rexinehouse.com'
        cursor.execute('SELECT id FROM users WHERE email = ?', (admin_email,))
        if not cursor.fetchone():
            admin_password = generate_password_hash('admin123')
            cursor.execute(
                'INSERT INTO users (email, password, is_admin) VALUES (?, ?, 1)', 
                (admin_email, admin_password)
            )
            logger.info("Admin user created")

class SecurityUtils:
    """Security utility functions."""
    
    @staticmethod
    def is_allowed_file(filename: str) -> bool:
        """Check if file extension is allowed."""
        if not filename:
            return False
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Basic email validation."""
        if not email or '@' not in email:
            return False
        return len(email) <= 254 and '.' in email.split('@')[1]
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """Password strength validation."""
        return password and len(password) >= 6

class UserService:
    """User-related business logic."""
    
    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return user data."""
        try:
            with DatabaseManager.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT id, password, is_admin FROM users WHERE email = ?', 
                    (email,)
                )
                user = cursor.fetchone()
                
                if user and check_password_hash(user['password'], password):
                    return {
                        'id': user['id'],
                        'email': email,
                        'is_admin': bool(user['is_admin'])
                    }
                return None
        except sqlite3.Error as e:
            logger.error(f"Authentication error: {e}")
            return None
    
    @staticmethod
    def create_user(email: str, password: str) -> bool:
        """Create new user account."""
        try:
            if not SecurityUtils.validate_email(email):
                return False
            
            if not SecurityUtils.validate_password(password):
                return False
            
            with DatabaseManager.get_db_connection() as conn:
                cursor = conn.cursor()
                hashed_password = generate_password_hash(password)
                cursor.execute(
                    'INSERT INTO users (email, password) VALUES (?, ?)', 
                    (email, hashed_password)
                )
                conn.commit()
                logger.info(f"User created: {email}")
                return True
                
        except sqlite3.IntegrityError:
            logger.warning(f"Duplicate user registration attempt: {email}")
            return False
        except sqlite3.Error as e:
            logger.error(f"User creation error: {e}")
            return False

class ProductService:
    """Product-related business logic."""
    
    @staticmethod
    def get_all_products() -> List[Dict[str, Any]]:
        """Get all products."""
        try:
            with DatabaseManager.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM products ORDER BY created_at DESC')
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Error fetching products: {e}")
            return []
    
    @staticmethod
    def get_starred_products(user_id: int) -> List[int]:
        """Get user's starred product IDs."""
        try:
            with DatabaseManager.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT product_id FROM starred_products WHERE user_id = ?', 
                    (user_id,)
                )
                return [row['product_id'] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Error fetching starred products: {e}")
            return []
    
    @staticmethod
    def toggle_star_product(user_id: int, product_id: int) -> bool:
        """Toggle star status for a product."""
        try:
            with DatabaseManager.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Check if already starred
                cursor.execute(
                    'SELECT id FROM starred_products WHERE user_id = ? AND product_id = ?', 
                    (user_id, product_id)
                )
                
                if cursor.fetchone():
                    # Remove star
                    cursor.execute(
                        'DELETE FROM starred_products WHERE user_id = ? AND product_id = ?', 
                        (user_id, product_id)
                    )
                    starred = False
                else:
                    # Add star
                    cursor.execute(
                        'INSERT INTO starred_products (user_id, product_id) VALUES (?, ?)', 
                        (user_id, product_id)
                    )
                    starred = True
                
                conn.commit()
                return starred
                
        except sqlite3.Error as e:
            logger.error(f"Error toggling star: {e}")
            return False

# Routes with proper error handling
@app.route('/')
def index():
    """Home page with product catalog."""
    try:
        products = ProductService.get_all_products()
        starred_products = []
        
        if 'user_id' in session:
            starred_products = ProductService.get_starred_products(session['user_id'])
        
        return render_template('index.html', products=products, starred_products=starred_products)
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        flash('An error occurred while loading the catalog.', 'error')
        return render_template('index.html', products=[], starred_products=[])

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login endpoint."""
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            
            if not email or not password:
                flash('Please provide both email and password.', 'error')
                return render_template('login.html')
            
            user = UserService.authenticate_user(email, password)
            if user:
                session['user_id'] = user['id']
                session['email'] = user['email']
                session['is_admin'] = user['is_admin']
                session.permanent = True
                
                flash('Login successful!', 'success')
                
                if user['is_admin']:
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('user_dashboard'))
            else:
                flash('Invalid email or password!', 'error')
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            flash('An error occurred during login.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration endpoint."""
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            
            if not SecurityUtils.validate_email(email):
                flash('Please provide a valid email address.', 'error')
                return render_template('register.html')
            
            if not SecurityUtils.validate_password(password):
                flash('Password must be at least 6 characters long.', 'error')
                return render_template('register.html')
            
            if UserService.create_user(email, password):
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Email already registered or registration failed!', 'error')
                
        except Exception as e:
            logger.error(f"Registration error: {e}")
            flash('An error occurred during registration.', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """User logout endpoint."""
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/star_product/<int:product_id>')
def star_product(product_id):
    """Toggle star status for a product."""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Login required'}), 401
    
    try:
        starred = ProductService.toggle_star_product(session['user_id'], product_id)
        return jsonify({'success': True, 'starred': starred})
    except Exception as e:
        logger.error(f"Error starring product: {e}")
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files with security checks."""
    try:
        # Additional security: check if file exists and is in allowed directory
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path) or not os.path.commonpath([file_path, app.config['UPLOAD_FOLDER']]) == app.config['UPLOAD_FOLDER']:
            return "File not found", 404
        
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        logger.error(f"Error serving file {filename}: {e}")
        return "File not found", 404

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return render_template('500.html'), 500

# Additional routes would go here (admin_dashboard, user_dashboard, etc.)
# For brevity, I'm showing the pattern for the main routes

if __name__ == '__main__':
    try:
        DatabaseManager.init_database()
        app.run(debug=True, host='127.0.0.1', port=5000)
    except Exception as e:
        logger.critical(f"Failed to start application: {e}")
        raise