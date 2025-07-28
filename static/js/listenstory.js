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
    // Load voices when they become available
    if (speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = function() {
            // Voices loaded
        };
    }
