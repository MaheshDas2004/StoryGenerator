document.addEventListener('DOMContentLoaded', function() {
            const tabBtns = document.querySelectorAll('.tab-btn');
            const tabContents = document.querySelectorAll('.tab-content');

            tabBtns.forEach(btn => {
                btn.addEventListener('click', function() {
                    const targetTab = this.dataset.tab;

                    // Remove active class from all tabs and contents
                    tabBtns.forEach(tab => {
                        tab.classList.remove('active', 'bg-orange-500/10', 'text-orange-500', 'border', 'border-orange-500/30');
                        tab.classList.add('bg-transparent', 'text-gray-400', 'border-0', 'hover:text-orange-500');
                    });
                    tabContents.forEach(content => {
                        content.classList.remove('active', 'block');
                        content.classList.add('hidden');
                    });

                    // Add active class to clicked tab and corresponding content
                    this.classList.add('active', 'bg-orange-500/10', 'text-orange-500', 'border', 'border-orange-500/30');
                    this.classList.remove('bg-transparent', 'text-gray-400', 'border-0', 'hover:text-orange-500');
                    
                    const targetContent = document.getElementById(targetTab);
                    if (targetContent) {
                        targetContent.classList.add('active', 'block');
                        targetContent.classList.remove('hidden');
                    }
                });
            });

            // Theme button functionality
            const themeButtons = document.querySelectorAll('.theme-btn');
            const hiddenInput = document.getElementById('selectedThemes');

            themeButtons.forEach(btn => {
                btn.addEventListener('click', function () {
                this.classList.toggle('active');

                // Toggle styling
                if (this.classList.contains('active')) {
                    this.classList.remove('bg-gray-800/50', 'text-gray-300', 'border-gray-600/30');
                    this.classList.add('bg-orange-500', 'text-white', 'border-orange-500');
                } else {
                    this.classList.add('bg-gray-800/50', 'text-gray-300', 'border-gray-600/30');
                    this.classList.remove('bg-orange-500', 'text-white', 'border-orange-500');
                }

                // ✅ Update hidden input with selected themes
                const selected = Array.from(themeButtons)
                    .filter(btn => btn.classList.contains('active'))
                    .map(btn => btn.dataset.theme);

                hiddenInput.value = selected.join(',');
                });
  });

        });
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });