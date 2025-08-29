// Clock functionality
function updateClock() {
  const now = new Date();
  
  // Update time - using 12-hour format with AM/PM (no seconds)
  const hours12 = now.getHours() % 12 || 12; // Convert 0 to 12
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const ampm = now.getHours() >= 12 ? 'PM' : 'AM';
  document.getElementById('clock').textContent = `${hours12}:${minutes} ${ampm}`;
  
  // Update date
  const options = { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  };
  document.getElementById('date').textContent = now.toLocaleDateString(undefined, options);
}

// Update immediately
document.addEventListener('DOMContentLoaded', function() {
  updateClock();
  
  // Then update every second
  setInterval(updateClock, 1000);
});