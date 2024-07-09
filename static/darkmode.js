document.addEventListener("DOMContentLoaded", function () {
  // Check the user's dark mode preference on page load
  let isDarkModeEnabled = localStorage.getItem("darkMode") === "enabled";

  // Apply dark mode if the preference is enabled without transition
  if (isDarkModeEnabled) {
    enableDarkMode(false); // Pass false to skip the transition on page load
  } else {
    disableDarkMode(false);
  }

  // Button click event listener to toggle dark mode
  const darkModeToggleButton = document.getElementById("mode");
  darkModeToggleButton.addEventListener("click", toggleDarkMode);

  // Function to toggle dark mode
  function toggleDarkMode() {
    isDarkModeEnabled = !isDarkModeEnabled;
    const newMode = isDarkModeEnabled ? "enabled" : "disabled";
    setThemePreference(newMode);
    isDarkModeEnabled ? enableDarkMode() : disableDarkMode();
  }

  // Function to enable dark mode
  function enableDarkMode(applyTransition = true) {
    document.body.classList.add("dark");
    document.body.classList.remove("light");
    document.getElementById("mode").textContent = "☀️";
    document.getElementById("mode").title = "Switch to Light Mode";
  }

  // Function to disable dark mode
  function disableDarkMode(applyTransition = true) {
    document.body.classList.add("light");
    document.body.classList.remove("dark");
    document.getElementById("mode").textContent = "🌙";
    document.getElementById("mode").title = "Switch to Dark Mode";
  }

  // Function to set theme preference in localStorage
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
