document.addEventListener("DOMContentLoaded", function () {
  // Check the user's dark mode preference on page load
  let isDarkModeEnabled = localStorage.getItem("darkMode") === "enabled";

  // Apply dark mode if the preference is enabled
  if (isDarkModeEnabled) {
    enableDarkMode();
  }

  // Button click event listener to toggle dark mode
  const darkModeToggleButton = document.getElementById("mode");
  darkModeToggleButton.addEventListener("click", toggleDarkMode);

  function toggleDarkMode() {
    isDarkModeEnabled = !isDarkModeEnabled; // Update the variable after toggling
    const newMode = isDarkModeEnabled ? "enabled" : "disabled";
    setThemePreference(newMode);
    isDarkModeEnabled ? enableDarkMode() : disableDarkMode();
  }

  function enableDarkMode() {
    document.body.classList.add("dark");
    document.getElementById("mode").textContent = "☀️";
  }

  function disableDarkMode() {
    document.body.classList.remove("dark");
    document.getElementById("mode").textContent = "🌙";
  }

  function setThemePreference(value) {
    localStorage.setItem("darkMode", value);
  }
});

document.addEventListener("DOMContentLoaded", function(event) {
  // Your code to run since DOM is loaded and ready
  bootstrap();
});
    const menuToggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.nav');

    menuToggle.addEventListener('click', function() {
      this.classList.toggle('open');
      nav.classList.toggle('open');
    });

