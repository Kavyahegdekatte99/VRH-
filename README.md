# VINAYAK REXINE HOUSE - Product Catalog System

A modern, responsive web-based product catalog system with dual-access functionality for administrators and customers.

## Features

### 🔐 Authentication System
- **Separate Login Portals**: Different access levels for administrators and customers
- **Session Management**: Maintains login state across browser visits
- **Secure Storage**: Protected user data with hashed passwords

### 👨‍💼 Administrator Dashboard
- **CRUD Operations**: Create, read, update, and delete products
- **Multi-Media Support**: Upload PDFs, images, and videos
- **Real-Time Updates**: Changes immediately visible to users
- **Product Management**: Categorization and organization tools

### 👥 User Interface
- **Product Catalog**: Browse comprehensive product information
- **Media Access**: View and download uploaded files
- **Favorites System**: Star/bookmark products (saved across sessions)
- **Responsive Design**: Works perfectly on all devices

### 🎨 Design Features
- **Brand Colors**: Dark blue/teal navigation with gold accents
- **Professional Layout**: Clean, modern interface
- **Smooth Animations**: Enhanced user experience
- **Mobile Responsive**: Perfect display on all screen sizes

## Demo Credentials

- **Admin Access**: 
  - Email: `admin@rexinehouse.com`
  - Password: `admin123`

- **User Access**: Register a new account through the registration form

**Note**: The catalog starts empty - the admin needs to add products using the admin dashboard.

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone/Download the Project
```bash
# If using git
git clone <repository-url>
cd catalogue_website

# Or extract the downloaded files to a folder
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

### Step 5: Add Products
The catalog starts empty. Login as admin (`admin@rexinehouse.com` / `admin123`) to add products through the admin dashboard.

## Project Structure

```
catalogue_website/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── catalog.db            # SQLite database (created automatically)
├── uploads/              # Directory for uploaded files
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── admin_dashboard.html  # Admin panel
│   ├── user_dashboard.html   # User favorites
│   └── contact.html      # Contact page
└── static/               # Static assets
    ├── css/
    │   └── style.css     # Custom styling
    └── js/
        └── main.js       # JavaScript functionality
```

## How to Use

### For Visitors
1. **Browse Catalog**: View all products immediately without login
2. **View Details**: See product information, images, and files
3. **Access Media**: Click on PDF, image, or video buttons to view files

### For Registered Users
1. **Register/Login**: Create account or login with existing credentials
2. **Star Products**: Click the star icon to bookmark favorite products
3. **My Favorites**: Access starred products from the user dashboard
4. **Persistent Storage**: Favorites are saved across browser sessions

### For Administrators
1. **Login**: Use admin credentials to access dashboard
2. **Add Products**: Fill out the form with product details and upload files
3. **Upload Files**: Support for images (JPG, PNG), PDFs, and videos (MP4, AVI)
4. **Manage Catalog**: Delete products and view all catalog items
5. **Real-Time Updates**: Changes appear immediately for all users

## Features in Detail

### Security
- Password hashing using Werkzeug security
- Session-based authentication
- File upload validation and security
- SQL injection protection through parameterized queries

### File Management
- Secure file uploads with extension validation
- Automatic file cleanup when products are deleted
- Support for multiple file types per product
- 16MB maximum file size limit

### Database
- SQLite database for easy deployment
- Automatic database initialization
- Relational design with foreign key constraints
- Efficient queries for performance

### Responsive Design
- Bootstrap 5 framework for mobile-first design
- Custom CSS with brand colors
- Smooth animations and transitions
- Professional layout matching brand identity

## Brand Identity

### Colors Used
- **Dark Blue/Teal** (`#1e3a5f`): Navigation, buttons, headings
- **Gold/Yellow** (`#d4af37`): Accents, hover effects, badges  
- **Black** (`#000000`): Text content
- **White** (`#ffffff`): Clean backgrounds

### Typography
- Professional, clean fonts
- Consistent sizing and spacing
- High contrast for readability

## Contact Information

**VINAYAK REXINE HOUSE**
- 📍 Address: Gas Office Road, Near Varadha Hotel, Kumta, Uttara Kannada, Karnataka 581343
- 📞 Phone: +91 9900106114, +91 87654 32109
- 📧 Email: vrexinehouse@yahoo.co.in
- 🕒 Hours: Mon-Sat 9AM-8PM, Sun: Contact admin and visit store

## Services
- ✅ Free delivery on orders above ₹5,000
- ✅ 100% genuine rexine materials
- ✅ Custom orders and tailored solutions
- ✅ 24/7 customer support

## Technical Requirements

### Server Requirements
- Python 3.7+
- Flask web framework
- SQLite (included with Python)
- Minimum 100MB disk space
- 512MB RAM recommended

### Browser Compatibility
- Chrome 70+
- Firefox 65+
- Safari 12+
- Edge 79+
- Mobile browsers supported

## Troubleshooting

### Common Issues

**Database not creating:**
- Ensure write permissions in the application directory
- Check if SQLite is properly installed

**File uploads not working:**
- Verify the `uploads/` directory exists and is writable
- Check file size limits (16MB maximum)
- Ensure proper file extensions

**Styling not loading:**
- Confirm `static/` directory structure is correct
- Check browser developer tools for 404 errors
- Clear browser cache

## Customization

### Adding New File Types
Edit the `ALLOWED_EXTENSIONS` in `app.py`:
```python
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'wmv', 'doc', 'docx'}
```

### Changing Brand Colors
Modify the CSS variables in `static/css/style.css`:
```css
:root {
    --dark-blue: #your-color;
    --gold: #your-gold-color;
}
```

### Adding New Product Fields
1. Update the database schema in the `init_db()` function
2. Modify the admin form in `admin_dashboard.html`
3. Update the product display templates

## Support

For technical support or business inquiries:
- Email: vrexinehouse@yahoo.co.in
- Phone: +91 9900106114, +91 87654 32109

## License

© 2025 VINAYAK REXINE HOUSE. All rights reserved.

This is a proprietary system developed for VINAYAK REXINE HOUSE. Unauthorized copying, modification, or distribution is prohibited.