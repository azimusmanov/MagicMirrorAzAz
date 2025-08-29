// Dark mode functionality
document.addEventListener('DOMContentLoaded', function() {
  // Configure Tailwind for dark mode
  tailwind.config = {
    darkMode: 'class',
    theme: {
      extend: {}
    }
  };
  
  // Check for dark mode preference
  if (window.matchMedia('(prefers-color-scheme: dark)').matches || 
      localStorage.getItem('darkMode') === 'true') {
    document.documentElement.classList.add('dark');
  }
});

// Function to toggle dark mode
function toggleDarkMode() {
  if (document.documentElement.classList.contains('dark')) {
    document.documentElement.classList.remove('dark');
    localStorage.setItem('darkMode', 'false');
  } else {
    document.documentElement.classList.add('dark');
    localStorage.setItem('darkMode', 'true');
  }
}

// Function to toggle mirror mode
function toggleMirrorMode() {
  document.body.classList.toggle('mirror-mode');
  localStorage.setItem('mirrorMode', document.body.classList.contains('mirror-mode'));
}