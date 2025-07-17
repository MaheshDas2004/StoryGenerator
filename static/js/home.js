document.addEventListener('DOMContentLoaded', function() {
  const themeToggle = document.getElementById('themeToggle');
  const toggleIcon = document.getElementById('toggleIcon');
  const body = document.getElementById('body');
  let isDarkMode = false;
  themeToggle.addEventListener('click', () => {
    isDarkMode = !isDarkMode;
    if (isDarkMode) {
      body.classList.remove('light-mode');
      body.classList.add('dark-mode');
      toggleIcon.textContent = '☀️';
    } else {
      body.classList.remove('dark-mode');
      body.classList.add('light-mode');
      toggleIcon.textContent = '🌙';
    }
  });
  // Add some extra sparkle animation on button hover
  const button = document.querySelector('.glow-button');
  button.addEventListener('mouseenter', () => {
    for (let i = 0; i < 5; i++) {
      const sparkle = document.createElement('div');
      sparkle.className = 'magic-sparkle';
      sparkle.style.position = 'absolute';
      sparkle.style.left = Math.random() * 100 + '%';
      sparkle.style.top = Math.random() * 100 + '%';
      sparkle.style.animationDelay = Math.random() * 2 + 's';
      button.appendChild(sparkle);
      setTimeout(() => {
        if (sparkle.parentNode) {
          sparkle.parentNode.removeChild(sparkle);
        }
      }, 2000);
    }
  });
});
