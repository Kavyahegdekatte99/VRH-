/**
 * VINAYAK REXINE HOUSE - Main JavaScript Module
 * Follows ES6+ standards with proper error handling and code quality practices
 */

'use strict';

// Constants
const CONFIG = {
    TOAST_DURATION: 4000,
    ANIMATION_DURATION: 300,
    FILE_SIZE_LIMIT: 16 * 1024 * 1024, // 16MB
    TOAST_POSITION: { top: '20px', right: '20px' }
};

const TOAST_TYPES = {
    SUCCESS: 'success',
    ERROR: 'error',
    WARNING: 'warning',
    INFO: 'info'
};

const BOOTSTRAP_ALERT_CLASSES = {
    [TOAST_TYPES.SUCCESS]: 'success',
    [TOAST_TYPES.ERROR]: 'danger',
    [TOAST_TYPES.WARNING]: 'warning',
    [TOAST_TYPES.INFO]: 'info'
};

const TOAST_ICONS = {
    [TOAST_TYPES.SUCCESS]: 'check-circle-fill',
    [TOAST_TYPES.ERROR]: 'x-circle-fill',
    [TOAST_TYPES.WARNING]: 'exclamation-triangle-fill',
    [TOAST_TYPES.INFO]: 'info-circle-fill'
};

/**
 * Utility functions
 */
class Utils {
    /**
     * Validate email format
     * @param {string} email - Email to validate
     * @returns {boolean} - True if valid email
     */
    static isValidEmail(email) {
        if (!email || typeof email !== 'string') {
            return false;
        }
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email.trim());
    }

    /**
     * Validate password strength
     * @param {string} password - Password to validate
     * @returns {boolean} - True if password meets requirements
     */
    static isValidPassword(password) {
        return password && typeof password === 'string' && password.length >= 6;
    }

    /**
     * Format currency in Indian Rupees
     * @param {number} amount - Amount to format
     * @returns {string} - Formatted currency string
     */
    static formatCurrency(amount) {
        try {
            return new Intl.NumberFormat('en-IN', {
                style: 'currency',
                currency: 'INR'
            }).format(amount);
        } catch (error) {
            console.warn('Currency formatting failed:', error);
            return `₹${amount}`;
        }
    }

    /**
     * Format date in Indian format
     * @param {string} dateString - Date string to format
     * @returns {string} - Formatted date string
     */
    static formatDate(dateString) {
        try {
            return new Intl.DateTimeFormat('en-IN', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            }).format(new Date(dateString));
        } catch (error) {
            console.warn('Date formatting failed:', error);
            return dateString;
        }
    }

    /**
     * Debounce function execution
     * @param {Function} func - Function to debounce
     * @param {number} wait - Wait time in milliseconds
     * @returns {Function} - Debounced function
     */
    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

/**
 * Toast notification system
 */
class ToastManager {
    /**
     * Show toast notification
     * @param {string} message - Message to display
     * @param {string} type - Toast type (success, error, warning, info)
     */
    static show(message, type = TOAST_TYPES.INFO) {
        try {
            ToastManager._removeExistingToast();
            const toast = ToastManager._createToast(message, type);
            ToastManager._displayToast(toast);
            ToastManager._scheduleRemoval(toast);
        } catch (error) {
            console.error('Failed to show toast:', error);
        }
    }

    /**
     * Remove existing toast notifications
     * @private
     */
    static _removeExistingToast() {
        const existingToast = document.querySelector('.toast-notification');
        if (existingToast) {
            existingToast.remove();
        }
    }

    /**
     * Create toast element
     * @private
     * @param {string} message - Toast message
     * @param {string} type - Toast type
     * @returns {HTMLElement} - Toast element
     */
    static _createToast(message, type) {
        const toast = document.createElement('div');
        const alertClass = BOOTSTRAP_ALERT_CLASSES[type] || 'info';
        const icon = TOAST_ICONS[type] || 'info-circle-fill';

        toast.className = `toast-notification alert alert-${alertClass} position-fixed`;
        toast.style.cssText = `
            top: ${CONFIG.TOAST_POSITION.top};
            right: ${CONFIG.TOAST_POSITION.right};
            z-index: 9999;
            min-width: 300px;
            max-width: 400px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            border: none;
            opacity: 0;
            transform: translateX(100%);
            transition: all ${CONFIG.ANIMATION_DURATION}ms ease;
        `;

        toast.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="bi bi-${icon} me-2"></i>
                <span>${Utils.escapeHtml(message)}</span>
                <button type="button" class="btn-close ms-auto" onclick="this.parentElement.parentElement.remove()" aria-label="Close"></button>
            </div>
        `;

        return toast;
    }

    /**
     * Display toast with animation
     * @private
     * @param {HTMLElement} toast - Toast element
     */
    static _displayToast(toast) {
        document.body.appendChild(toast);
        
        // Trigger animation
        setTimeout(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateX(0)';
        }, 50);
    }

    /**
     * Schedule toast removal
     * @private
     * @param {HTMLElement} toast - Toast element
     */
    static _scheduleRemoval(toast) {
        setTimeout(() => {
            if (toast.parentElement) {
                toast.style.opacity = '0';
                toast.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    if (toast.parentElement) {
                        toast.remove();
                    }
                }, CONFIG.ANIMATION_DURATION);
            }
        }, CONFIG.TOAST_DURATION);
    }
}

/**
 * Form validation and enhancement
 */
class FormManager {
    /**
     * Initialize form enhancements
     */
    static init() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            FormManager._enhanceForm(form);
        });
    }

    /**
     * Enhance individual form
     * @private
     * @param {HTMLFormElement} form - Form to enhance
     */
    static _enhanceForm(form) {
        // Add loading state to submit buttons
        form.addEventListener('submit', FormManager._handleFormSubmit);
        
        // Real-time validation
        const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', FormManager._validateField);
            input.addEventListener('input', FormManager._clearValidation);
        });
    }

    /**
     * Handle form submission
     * @private
     * @param {Event} event - Submit event
     */
    static _handleFormSubmit(event) {
        const form = event.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        
        if (submitBtn && !submitBtn.disabled) {
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
            submitBtn.disabled = true;
            
            // Reset button after timeout (fallback)
            setTimeout(() => {
                if (submitBtn.disabled) {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }
            }, 10000);
        }
    }

    /**
     * Validate form field
     * @private
     * @param {Event} event - Blur event
     */
    static _validateField(event) {
        const field = event.target;
        const value = field.value.trim();
        
        FormManager._clearValidation({ target: field });
        
        if (field.hasAttribute('required') && !value) {
            FormManager._showFieldError(field, 'This field is required.');
        } else if (field.type === 'email' && value && !Utils.isValidEmail(value)) {
            FormManager._showFieldError(field, 'Please enter a valid email address.');
        } else if (field.type === 'password' && value && !Utils.isValidPassword(value)) {
            FormManager._showFieldError(field, 'Password must be at least 6 characters long.');
        } else if (value) {
            field.classList.add('is-valid');
        }
    }

    /**
     * Clear field validation
     * @private
     * @param {Event} event - Input event
     */
    static _clearValidation(event) {
        const field = event.target;
        field.classList.remove('is-valid', 'is-invalid');
        FormManager._hideFieldError(field);
    }

    /**
     * Show field error
     * @private
     * @param {HTMLElement} field - Form field
     * @param {string} message - Error message
     */
    static _showFieldError(field, message) {
        field.classList.add('is-invalid');
        FormManager._hideFieldError(field);
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback d-block';
        errorDiv.textContent = message;
        
        field.parentNode.appendChild(errorDiv);
    }

    /**
     * Hide field error
     * @private
     * @param {HTMLElement} field - Form field
     */
    static _hideFieldError(field) {
        const existingError = field.parentNode.querySelector('.invalid-feedback');
        if (existingError) {
            existingError.remove();
        }
    }
}

/**
 * Product interaction manager
 */
class ProductManager {
    /**
     * Initialize product interactions
     */
    static init() {
        const starButtons = document.querySelectorAll('.star-btn');
        starButtons.forEach(button => {
            button.addEventListener('click', ProductManager._handleStarClick);
        });
    }

    /**
     * Handle star button click
     * @private
     * @param {Event} event - Click event
     */
    static async _handleStarClick(event) {
        event.preventDefault();
        
        const button = event.currentTarget;
        const productId = button.dataset.productId;
        const starIcon = button.querySelector('i');
        
        if (!productId || button.disabled) {
            return;
        }
        
        const originalIcon = starIcon.className;
        button.disabled = true;
        starIcon.className = 'bi bi-arrow-clockwise';
        starIcon.style.animation = 'spin 1s linear infinite';
        
        try {
            const response = await fetch(`/star_product/${productId}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                ProductManager._updateStarIcon(starIcon, data.starred);
                const message = data.starred ? 'Product added to favorites!' : 'Product removed from favorites!';
                const type = data.starred ? TOAST_TYPES.SUCCESS : TOAST_TYPES.INFO;
                ToastManager.show(message, type);
            } else {
                throw new Error(data.message || 'Unknown error occurred');
            }
            
        } catch (error) {
            console.error('Star toggle error:', error);
            starIcon.className = originalIcon;
            ToastManager.show(error.message || 'Please login to star products', TOAST_TYPES.ERROR);
        } finally {
            button.disabled = false;
            starIcon.style.animation = '';
        }
    }

    /**
     * Update star icon appearance
     * @private
     * @param {HTMLElement} starIcon - Star icon element
     * @param {boolean} starred - Whether product is starred
     */
    static _updateStarIcon(starIcon, starred) {
        if (starred) {
            starIcon.className = 'bi bi-star-fill';
            starIcon.style.color = '#d4af37';
        } else {
            starIcon.className = 'bi bi-star';
            starIcon.style.color = '#6c757d';
        }
    }
}

/**
 * File upload manager
 */
class FileUploadManager {
    /**
     * Initialize file upload enhancements
     */
    static init() {
        const fileInputs = document.querySelectorAll('input[type="file"]');
        fileInputs.forEach(input => {
            input.addEventListener('change', FileUploadManager._handleFileChange);
        });
    }

    /**
     * Handle file input change
     * @private
     * @param {Event} event - Change event
     */
    static _handleFileChange(event) {
        const input = event.target;
        const file = input.files[0];
        
        if (!file) {
            FileUploadManager._removePreview(input);
            return;
        }
        
        const validation = FileUploadManager._validateFile(file);
        if (!validation.valid) {
            FileUploadManager._showFileError(input, validation.message);
            input.value = '';
            return;
        }
        
        FileUploadManager._showFilePreview(input, file);
    }

    /**
     * Validate uploaded file
     * @private
     * @param {File} file - File to validate
     * @returns {Object} - Validation result
     */
    static _validateFile(file) {
        if (file.size > CONFIG.FILE_SIZE_LIMIT) {
            return {
                valid: false,
                message: 'File too large. Maximum size is 16MB.'
            };
        }
        
        return { valid: true };
    }

    /**
     * Show file preview
     * @private
     * @param {HTMLInputElement} input - File input
     * @param {File} file - Selected file
     */
    static _showFilePreview(input, file) {
        const fileName = file.name;
        const fileSize = (file.size / 1024 / 1024).toFixed(2);
        
        let preview = input.parentNode.querySelector('.file-preview');
        if (!preview) {
            preview = document.createElement('small');
            preview.className = 'file-preview text-muted d-block mt-1';
            input.parentNode.appendChild(preview);
        }
        
        preview.className = 'file-preview text-muted d-block mt-1';
        preview.innerHTML = `
            <i class="bi bi-file-earmark me-1"></i>
            ${Utils.escapeHtml(fileName)} (${fileSize} MB)
        `;
    }

    /**
     * Show file error
     * @private
     * @param {HTMLInputElement} input - File input
     * @param {string} message - Error message
     */
    static _showFileError(input, message) {
        let preview = input.parentNode.querySelector('.file-preview');
        if (!preview) {
            preview = document.createElement('small');
            preview.className = 'file-preview d-block mt-1';
            input.parentNode.appendChild(preview);
        }
        
        preview.className = 'file-preview text-danger d-block mt-1';
        preview.innerHTML = `
            <i class="bi bi-exclamation-triangle me-1"></i>
            ${Utils.escapeHtml(message)}
        `;
    }

    /**
     * Remove file preview
     * @private
     * @param {HTMLInputElement} input - File input
     */
    static _removePreview(input) {
        const preview = input.parentNode.querySelector('.file-preview');
        if (preview) {
            preview.remove();
        }
    }
}

/**
 * Application initialization
 */
class App {
    /**
     * Initialize the application
     */
    static init() {
        try {
            FormManager.init();
            ProductManager.init();
            FileUploadManager.init();
            App._initializeTooltips();
            App._initializeAnimations();
            
            // Application initialized successfully
        } catch (error) {
            console.error('Application initialization failed:', error);
        }
    }

    /**
     * Initialize Bootstrap tooltips
     * @private
     */
    static _initializeTooltips() {
        if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
            const tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
            tooltipElements.forEach(element => {
                new bootstrap.Tooltip(element);
            });
        }
    }

    /**
     * Initialize animations
     * @private
     */
    static _initializeAnimations() {
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('fade-in');
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });

            const animateElements = document.querySelectorAll('.card, .product-card');
            animateElements.forEach(element => observer.observe(element));
        }
    }
}

// Add missing utility method
Utils.escapeHtml = function(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
};

// Global error handler
window.addEventListener('error', function(event) {
    console.error('JavaScript Error:', {
        message: event.message,
        filename: event.filename,
        line: event.lineno,
        column: event.colno,
        error: event.error
    });
});

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', App.init);

// Export for module systems (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { App, Utils, ToastManager, FormManager, ProductManager, FileUploadManager };
}