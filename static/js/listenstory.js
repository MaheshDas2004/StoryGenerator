    // Text-to-Speech and Audio Controls
    let isPlaying = false;
    let currentUtterance = null;
    let currentSpeed = 1;
    let storyText = '';
    let currentPosition = 0;
    let totalDuration = 0;
    let startTime = 0;

    // Initialize
    document.addEventListener('DOMContentLoaded', function() {
        storyText = document.getElementById('storyText').innerText;
        totalDuration = estimateDuration(storyText);
        
        // Check if speech synthesis is supported
        if (!('speechSynthesis' in window)) {
            alert('Text-to-speech is not supported in your browser.');
            document.getElementById('playPauseBtn').disabled = true;
        }
    });

    // Play/Pause functionality
    document.getElementById('playPauseBtn').addEventListener('click', function() {
        if (!isPlaying) {
            playStory();
        } else {
            pauseStory();
        }
    });

    // Speed control
    document.getElementById('speedBtn').addEventListener('click', function() {
        const speeds = [1, 1.25, 1.5, 0.75];
        const currentIndex = speeds.indexOf(currentSpeed);
        currentSpeed = speeds[(currentIndex + 1) % speeds.length];
        document.getElementById('speedBtn').textContent = currentSpeed + 'x';
        
        if (isPlaying) {
            pauseStory();
            setTimeout(() => playStory(), 100);
        }
    });

    function playStory() {
        if (currentUtterance) {
            speechSynthesis.cancel();
        }

        currentUtterance = new SpeechSynthesisUtterance(storyText);
        currentUtterance.rate = currentSpeed;
        currentUtterance.pitch = 1;
        currentUtterance.volume = 1;

        // Find a suitable voice (prefer female voice for children's stories)
        const voices = speechSynthesis.getVoices();
        const preferredVoice = voices.find(voice => 
            voice.name.includes('female') || 
            voice.name.includes('Female') ||
            voice.gender === 'female'
        ) || voices[0];
        
        if (preferredVoice) {
            currentUtterance.voice = preferredVoice;
        }

        currentUtterance.onstart = function() {
            isPlaying = true;
            startTime = Date.now();
            updatePlayButton(true);
            startProgressUpdate();
        };

        currentUtterance.onend = function() {
            isPlaying = false;
            updatePlayButton(false);
            resetProgress();
        };

        currentUtterance.onerror = function(event) {
            console.error('Speech synthesis error:', event);
            isPlaying = false;
            updatePlayButton(false);
        };

        speechSynthesis.speak(currentUtterance);
    }

    function pauseStory() {
        if (currentUtterance) {
            speechSynthesis.cancel();
            isPlaying = false;
            updatePlayButton(false);
        }
    }

    function updatePlayButton(playing) {
        const playIcon = document.getElementById('playIcon');
        const pauseIcon = document.getElementById('pauseIcon');
        
        if (playing) {
            playIcon.classList.add('hidden');
            pauseIcon.classList.remove('hidden');
        } else {
            playIcon.classList.remove('hidden');
            pauseIcon.classList.add('hidden');
        }
    }

    function startProgressUpdate() {
        const progressInterval = setInterval(() => {
            if (!isPlaying) {
                clearInterval(progressInterval);
                return;
            }

            const elapsed = (Date.now() - startTime) / 1000;
            const progress = Math.min((elapsed / totalDuration) * 100, 100);
            
            document.getElementById('progressBar').style.width = progress + '%';

            if (progress >= 100) {
                clearInterval(progressInterval);
            }
        }, 1000);
    }

    function resetProgress() {
        document.getElementById('progressBar').style.width = '0%';
    }

    function estimateDuration(text) {
        // Estimate reading duration (average 150 words per minute for TTS)
        const wordCount = text.split(' ').length;
        return Math.ceil((wordCount / 150) * 60);
    }

    // Enhanced PDF Download functionality
    document.getElementById('downloadPdfBtn').addEventListener('click', function() {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        
        // Story data
        const storyTitle = "The Brave Little Explorer";
        const storyContent = document.getElementById('storyText').innerText;
        const moral = "True bravery means facing your fears and doing what's right, even when you feel scared. Believing in yourself opens doors to amazing discoveries and adventures.";
        
        // PDF styling
        const pageWidth = doc.internal.pageSize.getWidth();
        const pageHeight = doc.internal.pageSize.getHeight();
        const margin = 20;
        const maxWidth = pageWidth - (margin * 2);
        
        let currentY = margin + 20;
        
        // Title
        doc.setFontSize(24);
        doc.setFont('helvetica', 'bold');
        const titleLines = doc.splitTextToSize(storyTitle, maxWidth);
        titleLines.forEach(line => {
            const titleWidth = doc.getTextWidth(line);
            const titleX = (pageWidth - titleWidth) / 2;
            doc.text(line, titleX, currentY);
            currentY += 15;
        });
        
        currentY += 20;
        
        // Story content
        doc.setFontSize(12);
        doc.setFont('helvetica', 'normal');
        const contentLines = doc.splitTextToSize(storyContent, maxWidth);
        
        contentLines.forEach(line => {
            if (currentY > pageHeight - 40) {
                doc.addPage();
                currentY = margin + 20;
            }
            doc.text(line, margin, currentY);
            currentY += 8;
        });
        
        currentY += 20;
        
        // Moral section
        if (currentY > pageHeight - 60) {
            doc.addPage();
            currentY = margin + 20;
        }
        
        doc.setFontSize(16);
        doc.setFont('helvetica', 'bold');
        doc.text('The Moral of Our Story', margin, currentY);
        currentY += 15;
        
        doc.setFontSize(12);
        doc.setFont('helvetica', 'normal');
        const moralLines = doc.splitTextToSize(moral, maxWidth);
        moralLines.forEach(line => {
            doc.text(line, margin, currentY);
            currentY += 8;
        });
        
        // Footer
        doc.setFontSize(10);
        doc.setFont('helvetica', 'italic');
        doc.text('Generated by StorySpark - Where AI Magic Meets Storytelling', margin, pageHeight - 15);
        
        // Save the PDF
        doc.save(`${storyTitle.replace(/\s+/g, '_')}.pdf`);
        
        // Visual feedback
        const originalIcon = this.innerHTML;
        this.innerHTML = '<svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>';
        this.classList.add('bg-green-600');
        
        setTimeout(() => {
            this.innerHTML = originalIcon;
            this.classList.remove('bg-green-600');
        }, 2000);
    });

    // Load voices when they become available
    if (speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = function() {
            // Voices loaded
        };
    }
