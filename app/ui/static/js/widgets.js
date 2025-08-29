// Widget refresh functionality
document.addEventListener('DOMContentLoaded', function() {
  // Load profile name
  fetch('/profiles/current')
    .then(response => response.json())
    .then(data => {
      document.getElementById('who').textContent = data.name;
    })
    .catch(error => {
      console.error('Error loading profile:', error);
      document.getElementById('who').textContent = 'Guest';
    });
    
  // Set up periodic widget refreshes
  // Weather: every 30 minutes
  setInterval(() => {
    htmx.trigger("#weather-container", "refreshWeather");
  }, 30 * 60 * 1000);
  
  // Quote: every 24 hours
  setInterval(() => {
    htmx.trigger("#quote-container", "refreshQuote");
  }, 24 * 60 * 60 * 1000);
  
  // News: every 2 hours
  setInterval(() => {
    htmx.trigger("#news-container", "refreshNews");
  }, 2 * 60 * 60 * 1000);
});