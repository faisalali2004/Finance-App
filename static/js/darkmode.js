// static/js/darkmode.js

document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const htmlElement = document.documentElement;

    // Function to set the theme
    const setTheme = (theme) => {
        if (theme === 'dark') {
            htmlElement.classList.add('dark');
            htmlElement.classList.remove('light');
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        } else {
            htmlElement.classList.add('light');
            htmlElement.classList.remove('dark');
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
        }
        localStorage.setItem('theme', theme);
    };

    // Check for saved theme in localStorage on load
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        setTheme(savedTheme);
    } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        // Default to dark mode if system prefers it
        setTheme('dark');
    } else {
        // Default to light mode
        setTheme('light');
    }

    // Event listener for the theme toggle button
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = htmlElement.classList.contains('dark') ? 'dark' : 'light';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
        });
    }
});
