// Dark Mode Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Toggle script loaded');
    
    // Check if toggle element exists
    const toggle = document.querySelector(".toggle-container");
    if (!toggle) {
        console.log('Toggle element not found');
        return;
    }
    
    console.log('Toggle element found');
    
    // Check for saved theme preference or use preferred color scheme
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    console.log('Saved theme:', savedTheme);
    console.log('Prefers dark:', prefersDark);
    
    // Apply theme based on saved preference or system preference
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        applyDarkMode();
    } else {
        applyLightMode();
    }
    
    // Toggle theme on button click
    toggle.addEventListener('click', function() {
        console.log('Toggle clicked');
        
        if (document.body.classList.contains('dark-mode')) {
            applyLightMode();
        } else {
            applyDarkMode();
        }
    });
    
    function applyDarkMode() {
        console.log('Applying dark mode');
        document.body.classList.add('dark-mode');
        document.documentElement.setAttribute('data-bs-theme', 'dark');
        document.documentElement.classList.add('dark-theme');
        toggle.classList.add('night');
        
        // Ensure footer background changes in dark mode
        const footers = document.querySelectorAll('footer.bg-dark');
        footers.forEach(footer => {
            footer.style.backgroundColor = '#1a1a1a';
        });
        
        const icon = toggle.querySelector('.toggle-circle i');
        if (icon) {
            icon.className = ''; // Clear all classes
            icon.classList.add('fas', 'fa-lightbulb-off');
            // If fa-lightbulb-off doesn't exist in Font Awesome, use alternative
            if (window.getComputedStyle(icon).content === '') {
                icon.classList.remove('fa-lightbulb-off');
                icon.classList.add('fa-moon');
            }
        }
        
        localStorage.setItem('theme', 'dark');
    }
    
    function applyLightMode() {
        console.log('Applying light mode');
        document.body.classList.remove('dark-mode');
        document.documentElement.setAttribute('data-bs-theme', 'light');
        document.documentElement.classList.remove('dark-theme');
        toggle.classList.remove('night');
        
        // Reset footer background in light mode
        const footers = document.querySelectorAll('footer.bg-dark');
        footers.forEach(footer => {
            footer.style.backgroundColor = '';
        });
        
        const icon = toggle.querySelector('.toggle-circle i');
        if (icon) {
            icon.className = ''; // Clear all classes
            icon.classList.add('fas', 'fa-lightbulb');
        }
        
        localStorage.setItem('theme', 'light');
    }
}); 