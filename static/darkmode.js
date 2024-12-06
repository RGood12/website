document.addEventListener("DOMContentLoaded", function () {
  // Detect system dark mode preference
  const getSystemDarkModePreference = () => window.matchMedia("(prefers-color-scheme: dark)").matches;

  // Check if a user has manually set a preference in localStorage
  let isDarkModeEnabled = localStorage.getItem("darkMode");

  // Apply the correct theme on load
  if (isDarkModeEnabled === null) {
    // No user preference, use system preference
    isDarkModeEnabled = getSystemDarkModePreference() ? "enabled" : "disabled";
  }
  applyTheme(isDarkModeEnabled, false);

  // Listen for system theme changes
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
    // Clear the localStorage preference when OS theme changes
    localStorage.removeItem("darkMode");

    // Apply the new system preference
    const newMode = e.matches ? "enabled" : "disabled";
    applyTheme(newMode, false);
  });

  // Button click event listener to toggle dark mode
  const darkModeToggleButton = document.getElementById("mode");
  darkModeToggleButton.addEventListener("click", () => {
    // Toggle dark mode even if isDarkModeEnabled is null
    if (isDarkModeEnabled === null) {
      isDarkModeEnabled = isDarkModeEnabled === "enabled" ? "disabled" : "enabled";
    }
    setThemePreference(isDarkModeEnabled);  // Store user preference
    applyTheme(isDarkModeEnabled);  // Apply the chosen theme
  });

  // Function to apply theme (dark or light)
  function applyTheme(mode, applyTransition = true) {
    if (mode === "enabled") {
      enableDarkMode(applyTransition);
    } else {
      disableDarkMode(applyTransition);
    }
  }

  // Enable dark mode
  function enableDarkMode(applyTransition = true) {
    document.body.classList.add("dark");
    document.body.classList.remove("light");
    document.getElementById("mode").textContent = "☀️";
    document.getElementById("mode").title = "Switch to Light Mode";
  }

  // Disable dark mode
  function disableDarkMode(applyTransition = true) {
    document.body.classList.add("light");
    document.body.classList.remove("dark");
    document.getElementById("mode").textContent = "🌙";
    document.getElementById("mode").title = "Switch to Dark Mode";
  }

  // Set the user's theme preference in localStorage
  function setThemePreference(value) {
    localStorage.setItem("darkMode", value);
  }

  // Menu toggle functionality (for mobile/desktop)
  const menuToggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav');

  menuToggle.addEventListener('click', function() {
    this.classList.toggle('open');
    nav.classList.toggle('open');
  });
});

