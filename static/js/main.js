document.addEventListener("DOMContentLoaded", () => {
  // --- 1. GLOBAL THEME PERSISTENCE ---
  const body = document.body;
  const themeToggleDropdown = document.getElementById("theme-toggle");
  const navThemeToggle = document.getElementById("nav-theme-toggle");
  const navThemeText = document.getElementById("nav-theme-text");

  function updateThemeUI(isDark) {
    if (isDark) {
      body.classList.add("dark-mode");
      if (themeToggleDropdown) themeToggleDropdown.innerHTML = "☀️ Light Mode";
      if (navThemeText) navThemeText.innerText = "☀️ Light Mode";
    } else {
      body.classList.remove("dark-mode");
      if (themeToggleDropdown) themeToggleDropdown.innerHTML = "🌙 Dark Mode";
      if (navThemeText) navThemeText.innerText = "🌙 Dark Mode";
    }
  }

  const savedTheme = localStorage.getItem("global-theme");
  const isInitiallyDark = savedTheme === "dark" || !savedTheme; 
  updateThemeUI(isInitiallyDark);

  const toggleTheme = (e) => {
    e.preventDefault(); 
    const isNowDark = !body.classList.contains("dark-mode");
    localStorage.setItem("global-theme", isNowDark ? "dark" : "light");
    updateThemeUI(isNowDark);
  };

  if (themeToggleDropdown) themeToggleDropdown.addEventListener("click", toggleTheme);
  if (navThemeToggle) navThemeToggle.addEventListener("click", toggleTheme);

 // --- 2. THE FINAL DROPDOWN FIX ---
const dropdownTriggers = document.querySelectorAll(".dropdown-trigger");

dropdownTriggers.forEach(trigger => {
    trigger.addEventListener("click", function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        console.log("Dropdown clicked!"); // Check your F12 console for this!

        const parent = this.closest(".dropdown");
        const content = parent.querySelector(".dropdown-content");

        // Close all other dropdowns
        document.querySelectorAll(".dropdown-content.show").forEach(openContent => {
            if (openContent !== content) {
                openContent.classList.remove("show");
            }
        });

        // Toggle the 'show' class
        content.classList.toggle("show");
    });
});

// Close when clicking outside
document.addEventListener("click", (e) => {
    if (!e.target.closest(".dropdown")) {
        document.querySelectorAll(".dropdown-content.show").forEach(content => {
            content.classList.remove("show");
        });
    }
});

  // --- 3. DYNAMIC COPY BUTTONS ---
  document.querySelectorAll("pre").forEach((block) => {
    if (!block.querySelector(".copy-btn")) {
      const button = document.createElement("button");
      button.innerText = "Copy";
      button.className = "copy-btn";
      button.onclick = () => {
        const codeElement = block.querySelector("code") || block;
        navigator.clipboard.writeText(codeElement.innerText).then(() => {
          button.innerText = "Copied!";
          button.classList.add("copied");
          setTimeout(() => {
            button.innerText = "Copy";
            button.classList.remove("copied");
          }, 1500);
        });
      };
      block.style.position = "relative";
      block.appendChild(button);
    }
  });

  // --- 4. MOBILE HAMBURGER ---
  const hamburgerBtn = document.getElementById("hamburger-btn");
  const navMenu = document.getElementById("main-nav");
  if (hamburgerBtn && navMenu) {
    hamburgerBtn.addEventListener("click", () => {
      const isActive = navMenu.classList.toggle("mobile-active");
      hamburgerBtn.innerText = isActive ? "✕" : "☰";
    });
  }

  // Progress Bar
  window.onscroll = function () {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (height > 0) ? (winScroll / height) * 100 : 0;
    const progressBar = document.getElementById("progress-bar");
    if (progressBar) progressBar.style.width = scrolled + "%";
  };
});