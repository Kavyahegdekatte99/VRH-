// Main JavaScript functionality for VINAYAK REXINE HOUSE
document.addEventListener('DOMContentLoaded', function() {
    
    // Star/Unstar Product Functionality
    const starButtons = document.querySelectorAll('.star-btn');
    
    starButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const productId = this.dataset.productId;
            const starIcon = this.querySelector('i');
            
            // Add loading state
            const originalContent = starIcon.className;
            starIcon.className = 'bi bi-arrow-clockwise loading';
            
            // Make AJAX request
            fetch(`/star_product/${productId}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update star icon based on response
                    if (data.starred) {
                        starIcon.className = 'bi bi-star-fill';
                        starIcon.style.color = '#d4af37';
                        showToast('Product added to favorites!', 'success');
                    } else {
                        starIcon.className = 'bi bi-star';
                        starIcon.style.color = '#6c757d';
                        showToast('Product removed from favorites!', 'info');
                    }
                } else {
                    // Restore original icon on error
                    starIcon.className = originalContent;
                    showToast(data.message || 'Please login to star products', 'error');
                }
            })
            .catch(error => {
                // Handle network or server errors
                starIcon.className = originalContent;
                showToast('An error occurred. Please try again.', 'error');
            });
        });
    });
    
    // Toast Notification System
    function showToast(message, type = 'info') {
        // Remove any existing toasts
        const existingToast = document.querySelector('.toast-notification');
        if (existingToast) {
            existingToast.remove();
        }
        
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `toast-notification alert alert-${getBootstrapAlertClass(type)} position-fixed`;
        toast.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            border: none;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
        `;
        
        toast.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="bi bi-${getIconForType(type)} me-2"></i>
                <span>${message}</span>
                <button type="button" class="btn-close ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
        `;
        
        // Add to page
        document.body.appendChild(toast);
        
        // Trigger animation
        setTimeout(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateX(0)';
        }, 100);
        
        // Auto remove after 4 seconds
        setTimeout(() => {
            if (toast.parentElement) {
                toast.style.opacity = '0';
                toast.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    if (toast.parentElement) {
                        toast.remove();
                    }
                }, 300);
            }
        }, 4000);
    }
    
    function getBootstrapAlertClass(type) {
        const typeMap = {
            'success': 'success',
            'error': 'danger',
            'warning': 'warning',
            'info': 'info'
        };
        return typeMap[type] || 'info';
    }
    
    function getIconForType(type) {
        const iconMap = {
            'success': 'check-circle-fill',
            'error': 'x-circle-fill',
            'warning': 'exclamation-triangle-fill',
            'info': 'info-circle-fill'
        };
        return iconMap[type] || 'info-circle-fill';
    }
    
    // Form Enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        // Add loading state to submit buttons
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="loading me-2"></span>Processing...';
                submitBtn.disabled = true;
                
                // Reset button after 5 seconds (fallback)
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 5000);
            }
        });
        
        // Real-time form validation
        const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', validateField);
            input.addEventListener('input', clearValidation);
        });
    });
    
    function validateField(e) {
        const field = e.target;
        const value = field.value.trim();
        
        // Remove existing validation classes
        field.classList.remove('is-valid', is-invalid');
        
        if (field.hasAttribute('required') && !value) {
            field.classList.add('is-invalid');
            showFieldError(field, 'This field is required.');
        } else if (field.type === 'email' && value && !isValidEmail(value)) {
            field.classList.add('is-invalid');
            showFieldError(field, 'Please enter a valid email address.');
        } else if (field.type === 'password' && value && value.length < 6) {
            field.classList.add('is-invalid');
            showFieldError(field, 'Password must be at least 6 characters long.');
        } else if (value) {
            field.classList.add('is-valid');
            hideFieldError(field);
        }
    }
    
    function clearValidation(e) {
        const field = e.target;
        field.classList.remove('is-valid', 'is-invalid');
        hideFieldError(field);
    }
    
    function showFieldError(field, message) {
        hideFieldError(field); // Remove existing error
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback d-block';
        errorDiv.textContent = message;
        
        field.parentNode.appendChild(errorDiv);
    }
    
    function hideFieldError(field) {
        const existingError = field.parentNode.querySelector('.invalid-feedback');
        if (existingError) {
            existingError.remove();
        }
    }
    
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    // File Upload Preview
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Show file name
                const fileName = file.name;
                const fileSize = (file.size / 1024 / 1024).toFixed(2); // MB
                
                // Create or update preview
                let preview = input.parentNode.querySelector('.file-preview');
                if (!preview) {
                    preview = document.createElement('small');
                    preview.className = 'file-preview text-muted d-block mt-1';
                    input.parentNode.appendChild(preview);
                }
                
                preview.innerHTML = `
                    <i class="bi bi-file-earmark me-1"></i>
                    ${fileName} (${fileSize} MB)
                `;
                
                // Validate file size (16MB limit)
                if (file.size > 16 * 1024 * 1024) {
                    preview.className = 'file-preview text-danger d-block mt-1';
                    preview.innerHTML = `
                        <i class="bi bi-exclamation-triangle me-1"></i>
                        File too large. Maximum size is 16MB.
                    `;
                    input.value = '';
                }
            }
        });
    });
    
    // Smooth Scrolling for Anchor Links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Image Lazy Loading
    const images = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for browsers without IntersectionObserver
        images.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
        });
    }
    
    // Product Card Hover Effects
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Search/Filter Functionality (if needed in future)
    const searchInput = document.querySelector('#product-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const products = document.querySelectorAll('.product-card');
            
            products.forEach(product => {
                const productName = product.querySelector('.card-title').textContent.toLowerCase();
                const productDesc = product.querySelector('.card-text')?.textContent.toLowerCase() || '';
                
                if (productName.includes(searchTerm) || productDesc.includes(searchTerm)) {
                    product.style.display = 'block';
                } else {
                    product.style.display = 'none';
                }
            });
        });
    }
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Contact Form Enhancement
    const contactForm = document.querySelector('#contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Simulate form submission
            const formData = new FormData(this);
            const submitBtn = this.querySelector('button[type="submit"]');
            
            submitBtn.innerHTML = '<span class="loading me-2"></span>Sending...';
            submitBtn.disabled = true;
            
            // Simulate delay
            setTimeout(() => {
                showToast('Thank you for your message! We will get back to you soon.', 'success');
                this.reset();
                submitBtn.innerHTML = '<i class="bi bi-send me-2"></i>Send Message';
                submitBtn.disabled = false;
            }, 2000);
        });
    }
    
    // Add fade-in animation to elements as they come into view
    const animateElements = document.querySelectorAll('.card, .product-card');
    if ('IntersectionObserver' in window) {
        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, {
            threshold: 0.1
        });
        
        animateElements.forEach(el => animationObserver.observe(el));
    }
});

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function formatDate(dateString) {
    return new Intl.DateTimeFormat('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    }).format(new Date(dateString));
}

// Global error handler
window.addEventListener('error', function(e) {
    // Handle global JavaScript errors silently
    showToast('An unexpected error occurred', 'error');
});

// Service Worker Registration (for PWA functionality in future)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // navigator.serviceWorker.register('/sw.js')
        //     .then(function(registration) {
        //         // ServiceWorker registration successful
        //     })
        //     .catch(function(err) {
        //         // ServiceWorker registration failed
        //     });
    });
}