from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'wmv'}

def allowed_file(filename):
    """Check if uploaded file has an allowed extension.
    
    Args:
        filename (str): Name of the file to check
        
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect('catalog.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Products table
    c.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        category TEXT,
        price REAL,
        image_url TEXT,
        pdf_url TEXT,
        video_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Starred products table
    c.execute('''CREATE TABLE IF NOT EXISTS starred_products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (product_id) REFERENCES products (id),
        UNIQUE(user_id, product_id)
    )''')
    
    # Create admin user if not exists
    admin_email = 'admin@rexinehouse.com'
    c.execute('SELECT id FROM users WHERE email = ?', (admin_email,))
    if not c.fetchone():
        admin_password = generate_password_hash('admin123')
        c.execute('INSERT INTO users (email, password, is_admin) VALUES (?, ?, 1)', 
                 (admin_email, admin_password))
    
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def index():
    """Display the home page with product catalog."""
    conn = sqlite3.connect('catalog.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products ORDER BY created_at DESC')
    products = c.fetchall()
    
    # Get starred products if user is logged in
    starred_products = []
    if 'user_id' in session:
        c.execute('SELECT product_id FROM starred_products WHERE user_id = ?', (session['user_id'],))
        starred_products = [row[0] for row in c.fetchall()]
    
    conn.close()
    return render_template('index.html', products=products, starred_products=starred_products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login authentication."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('catalog.db')
        c = conn.cursor()
        c.execute('SELECT id, password, is_admin FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['email'] = email
            session['is_admin'] = bool(user[2])
            flash('Login successful!', 'success')
            
            if session['is_admin']:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid email or password!', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('catalog.db')
        c = conn.cursor()
        
        # Check if user already exists
        c.execute('SELECT id FROM users WHERE email = ?', (email,))
        if c.fetchone():
            flash('Email already registered!', 'error')
            conn.close()
            return render_template('register.html')
        
        # Create new user
        hashed_password = generate_password_hash(password)
        c.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Handle user logout by clearing session."""
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """Display admin dashboard for product management."""
    if not session.get('is_admin'):
        flash('Admin access required!', 'error')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('catalog.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products ORDER BY created_at DESC')
    products = c.fetchall()
    conn.close()
    
    return render_template('admin_dashboard.html', products=products)

@app.route('/user/dashboard')
def user_dashboard():
    """Display user dashboard with starred products."""
    if 'user_id' not in session or session.get('is_admin'):
        flash('User access required!', 'error')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('catalog.db')
    c = conn.cursor()
    c.execute('''SELECT p.* FROM products p 
                 JOIN starred_products sp ON p.id = sp.product_id 
                 WHERE sp.user_id = ? ORDER BY sp.created_at DESC''', (session['user_id'],))
    starred_products = c.fetchall()
    conn.close()
    
    return render_template('user_dashboard.html', starred_products=starred_products)

def handle_file_upload(file_key):
    """Handle individual file upload and return filename.
    
    Args:
        file_key (str): Key for the file in request.files
        
    Returns:
        str: Filename if uploaded successfully, empty string otherwise
    """
    if file_key in request.files and request.files[file_key].filename != '':
        file = request.files[file_key]
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return filename
    return ''

@app.route('/admin/add_product', methods=['POST'])
def add_product():
    """Add new product to the catalog."""
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Admin access required'})
    
    # Extract form data
    name = request.form['name']
    description = request.form['description']
    category = request.form['category']
    price = float(request.form['price']) if request.form['price'] else 0.0
    
    # Handle file uploads
    image_url = handle_file_upload('image')
    pdf_url = handle_file_upload('pdf')
    video_url = handle_file_upload('video')
    
    # Save to database
    conn = sqlite3.connect('catalog.db')
    c = conn.cursor()
    c.execute('''INSERT INTO products (name, description, category, price, image_url, pdf_url, video_url) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', 
              (name, description, category, price, image_url, pdf_url, video_url))
    conn.commit()
    conn.close()
    
    flash('Product added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_product/<int:product_id>')
def delete_product(product_id):
    """Delete a product and its associated files from the catalog.
    
    Args:
        product_id (int): ID of the product to delete
        
    Returns:
        Response: Redirect to admin dashboard with flash message
    """
    if not session.get('is_admin'):
        flash('Admin access required!', 'error')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('catalog.db')
    c = conn.cursor()
    
    # Get file URLs to delete files
    c.execute('SELECT image_url, pdf_url, video_url FROM products WHERE id = ?', (product_id,))
    product = c.fetchone()
    
    if product:
        # Delete files
        for file_url in product:
            if file_url:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_url)
                if os.path.exists(file_path):
                    os.remove(file_path)
        
        # Delete product and related starred entries
        c.execute('DELETE FROM starred_products WHERE product_id = ?', (product_id,))
        c.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        flash('Product deleted successfully!', 'success')
    else:
        flash('Product not found!', 'error')
    
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/star_product/<int:product_id>')
def star_product(product_id):
    """Toggle star/favorite status for a product.
    
    Args:
        product_id (int): ID of the product to star/unstar
        
    Returns:
        JSON: Success status and whether product is now starred
    """
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Login required'})
    
    conn = sqlite3.connect('catalog.db')
    c = conn.cursor()
    
    # Check if already starred
    c.execute('SELECT id FROM starred_products WHERE user_id = ? AND product_id = ?', 
              (session['user_id'], product_id))
    
    if c.fetchone():
        # Remove star
        c.execute('DELETE FROM starred_products WHERE user_id = ? AND product_id = ?', 
                  (session['user_id'], product_id))
        starred = False
    else:
        # Add star
        c.execute('INSERT INTO starred_products (user_id, product_id) VALUES (?, ?)', 
                  (session['user_id'], product_id))
        starred = True
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'starred': starred})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files from the upload directory.
    
    Args:
        filename (str): Name of the file to serve
        
    Returns:
        File: The requested file from uploads directory
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/contact')
def contact():
    """Render the contact page.
    
    Returns:
        HTML: Rendered contact template
    """
    return render_template('contact.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)