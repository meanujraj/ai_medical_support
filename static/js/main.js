// Main JavaScript file for AI Medical Support

document.addEventListener('DOMContentLoaded', function() {
    // Theme toggle functionality
    initThemeToggle();
    
    // Initialize tooltips
    initTooltips();
    
    // Initialize form validation
    initFormValidation();
});

// Theme toggle functionality
function initThemeToggle() {
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    if (!themeToggleBtn) return;
    
    // Check for saved theme preference or use preferred color scheme
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const savedTheme = localStorage.getItem('theme');
    
    // Apply theme based on saved preference or system preference
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.documentElement.setAttribute('data-bs-theme', 'dark');
        themeToggleBtn.innerHTML = '<i class="fas fa-sun"></i> <span>Light Mode</span>';
    } else {
        document.documentElement.setAttribute('data-bs-theme', 'light');
        themeToggleBtn.innerHTML = '<i class="fas fa-moon"></i> <span>Dark Mode</span>';
    }
    
    // Toggle theme on button click
    themeToggleBtn.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-bs-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        // Update button icon and text
        if (newTheme === 'dark') {
            themeToggleBtn.innerHTML = '<i class="fas fa-sun"></i> <span>Light Mode</span>';
        } else {
            themeToggleBtn.innerHTML = '<i class="fas fa-moon"></i> <span>Dark Mode</span>';
        }
    });
}

// Initialize Bootstrap tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Form validation
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

// Symptom analysis form handling
function handleSymptomForm() {
    const symptomForm = document.getElementById('symptom-form');
    if (!symptomForm) return;
    
    symptomForm.addEventListener('submit', function(e) {
        const selectedSymptoms = document.querySelectorAll('input[name="symptoms"]:checked');
        if (selectedSymptoms.length === 0) {
            e.preventDefault();
            alert('Please select at least one symptom');
        }
    });
}

// Medicine search functionality
function initMedicineSearch() {
    const searchInput = document.getElementById('medicine-search');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function() {
        if (this.value.length >= 3) {
            // Show loading indicator
            document.getElementById('search-loading').classList.remove('d-none');
        }
    });
}

// Animate elements when they come into view
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    }, { threshold: 0.1 });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
} 