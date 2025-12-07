// ===== DOM Elements =====
const urlInput = document.getElementById('urlInput');
const generateBtn = document.getElementById('generateBtn');
const progressSection = document.getElementById('progressSection');
const progressTitle = document.getElementById('progressTitle');
const progressPercentage = document.getElementById('progressPercentage');
const progressFill = document.getElementById('progressFill');
const progressMessage = document.getElementById('progressMessage');
const resultSection = document.getElementById('resultSection');
const downloadBtn = document.getElementById('downloadBtn');
const downloadPptBtn = document.getElementById('downloadPptBtn');
const newVideoBtn = document.getElementById('newVideoBtn');

// ===== State =====
let currentProgress = 0;
let videoPath = null;
let pptPath = null;

// ===== Progress Steps Configuration =====
const steps = [
    { id: 1, name: 'Scraping', message: 'Extracting content from webpage...' },
    { id: 2, name: 'AI Generation', message: 'Generating presentation structure with AI...' },
    { id: 3, name: 'Creating Slides', message: 'Creating PowerPoint presentation...' },
    { id: 4, name: 'Adding Music', message: 'Selecting background music...' },
    { id: 5, name: 'Narration', message: 'Generating AI narration...' },
    { id: 6, name: 'Final Output', message: 'Finalizing presentation and video...' }
];

// ===== Event Listeners =====
generateBtn.addEventListener('click', handleGenerate);
newVideoBtn.addEventListener('click', resetForm);
downloadBtn.addEventListener('click', handleDownload);
downloadPptBtn.addEventListener('click', handleDownloadPpt);

urlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleGenerate();
    }
});

// ===== Main Functions =====
async function handleGenerate() {
    const url = urlInput.value.trim();

    // Validation
    if (!url) {
        showError('Please enter a valid URL');
        return;
    }

    if (!isValidUrl(url)) {
        showError('Please enter a valid URL (e.g., https://example.com)');
        return;
    }

    // Start generation process
    startGeneration(url);
}

async function startGeneration(url) {
    // Hide input, show progress
    document.querySelector('.input-container').style.display = 'none';
    progressSection.classList.remove('hidden');
    resultSection.classList.add('hidden');

    // Reset progress
    currentProgress = 0;
    updateProgress(0);

    try {
        // Call backend API with credentials for authentication
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        if (!response.ok) {
            // Handle specific error cases
            if (response.status === 401) {
                showError('Please log in to generate content.');
                window.location.href = '/login.html';
                return;
            }
            throw new Error(data.message || 'Failed to start generation');
        }

        const jobId = data.job_id;

        // Poll for progress
        pollProgress(jobId);

    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Failed to generate content. Please try again.');
        resetForm();
    }
}

async function pollProgress(jobId) {
    const pollInterval = setInterval(async () => {
        try {
            const response = await fetch(`/api/progress/${jobId}`, {
                credentials: 'include'
            });
            const data = await response.json();

            // Handle queued and processing statuses
            if (data.status === 'queued' || data.status === 'processing') {
                updateProgress(data.progress, data.step, data.message);
            } else if (data.status === 'completed') {
                clearInterval(pollInterval);
                updateProgress(100, 6, 'Generation successful!');
                setTimeout(() => {
                    showResult(data.video_path, data.ppt_path);
                }, 1000);
            } else if (data.status === 'error') {
                clearInterval(pollInterval);
                showError(data.error || data.message || 'An error occurred during generation');
                resetForm();
            }
        } catch (error) {
            console.error('Polling error:', error);
            clearInterval(pollInterval);
            showError('Lost connection to server. Please try again.');
            resetForm();
        }
    }, 2000); // Poll every 2 seconds
}

function updateProgress(percentage, stepId = null, message = null) {
    // Update percentage
    currentProgress = percentage;
    progressPercentage.textContent = `${Math.round(percentage)}%`;
    progressFill.style.width = `${percentage}%`;

    // Update step indicators
    if (stepId !== null) {
        const stepElements = document.querySelectorAll('.step');
        stepElements.forEach((step, index) => {
            const stepNumber = index + 1;
            step.classList.remove('active', 'completed');

            if (stepNumber < stepId) {
                step.classList.add('completed');
            } else if (stepNumber === stepId) {
                step.classList.add('active');
            }
        });
    }

    // Update message
    if (message) {
        progressMessage.textContent = message;
    }
}

function showResult(vPath, pPath) {
    videoPath = vPath;
    pptPath = pPath;
    progressSection.classList.add('hidden');
    resultSection.classList.remove('hidden');
}

function showError(message) {
    alert(message); // You can replace this with a nicer toast notification
}

function resetForm() {
    // Reset UI
    document.querySelector('.input-container').style.display = 'flex';
    progressSection.classList.add('hidden');
    resultSection.classList.add('hidden');

    // Clear input
    urlInput.value = '';
    videoPath = null;
    pptPath = null;

    // Reset progress
    currentProgress = 0;
    updateProgress(0);

    // Reset step indicators
    const stepElements = document.querySelectorAll('.step');
    stepElements.forEach(step => {
        step.classList.remove('active', 'completed');
    });
}

async function handleDownload() {
    if (!videoPath) {
        showError('No video available for download');
        return;
    }

    try {
        // Trigger download
        const link = document.createElement('a');
        link.href = `/api/download/${videoPath}`;
        link.download = videoPath; // Use the actual filename
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        console.error('Download error:', error);
        showError('Failed to download video. Please try again.');
    }
}

async function handleDownloadPpt() {
    if (!pptPath) {
        showError('No presentation available for download');
        return;
    }

    try {
        // Trigger download
        const link = document.createElement('a');
        link.href = `/api/download/${pptPath}`;
        link.download = pptPath; // Use the actual filename
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        console.error('Download error:', error);
        showError('Failed to download presentation. Please try again.');
    }
}

// ===== Utility Functions =====
function isValidUrl(string) {
    try {
        const url = new URL(string);
        return url.protocol === 'http:' || url.protocol === 'https:';
    } catch (_) {
        return false;
    }
}

// ===== Demo Mode (for testing without backend) =====
// Uncomment this to test the UI without a backend
/*
async function startGeneration(url) {
    document.querySelector('.input-container').style.display = 'none';
    progressSection.classList.remove('hidden');
    resultSection.classList.add('hidden');
    
    // Simulate progress
    for (let i = 0; i < steps.length; i++) {
        await new Promise(resolve => setTimeout(resolve, 2000));
        const progress = ((i + 1) / steps.length) * 100;
        updateProgress(progress, i + 1, steps[i].message);
    }
    
    setTimeout(() => {
        showResult('demo_video.mp4');
    }, 1000);
}
*/

// ===== Smooth Scroll for Navigation =====
document.querySelectorAll('.nav a').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetSection = document.querySelector(targetId);

        if (targetSection) {
            targetSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ===== Add subtle parallax effect to gradient orbs =====
document.addEventListener('mousemove', (e) => {
    const orbs = document.querySelectorAll('.gradient-orb');
    const mouseX = e.clientX / window.innerWidth;
    const mouseY = e.clientY / window.innerHeight;

    orbs.forEach((orb, index) => {
        const speed = (index + 1) * 10;
        const x = (mouseX - 0.5) * speed;
        const y = (mouseY - 0.5) * speed;

        orb.style.transform = `translate(${x}px, ${y}px)`;
    });
});

// ===== Feature Details Modal Logic =====
const featureDetails = {
    scraping: {
        icon: '🌐',
        title: 'Advanced Web Scraping',
        description: 'Our intelligent scraping engine extracts the essence of any webpage, filtering out clutter and ads to focus on the core content.',
        features: [
            'Automatic text extraction and summarization',
            'Smart image detection and selection',
            'Removes ads, popups, and navigation menus',
            'Works with blogs, news articles, and documentation',
            'Maintains context and content hierarchy'
        ]
    },
    ai: {
        icon: '🤖',
        title: 'AI Content Generation',
        description: 'Powered by Google Gemini AI, we transform raw text into engaging presentation narratives structured for maximum impact.',
        features: [
            'Generates professional slide titles and bullet points',
            'Creates natural-sounding scripts for narration',
            'Structures content logically (Intro, Body, Conclusion)',
            'Adapts tone based on the source material',
            'Summarizes complex topics into digestable slides'
        ]
    },
    slides: {
        icon: '📊',
        title: 'Professional Slides',
        description: 'Create visually stunning PowerPoint presentations instantly. No more wrestling with formatting or layout tools.',
        features: [
            'Modern, clean slide layouts',
            'Automatic image placement and sizing',
            'Consistent typography and styling',
            'Generates standard .pptx files editable in PowerPoint',
            'Includes title slides and section headers'
        ]
    },
    narration: {
        icon: '🎙️',
        title: 'AI Voice Narration',
        description: 'Turn text into lifelike speech. Our AI narrators bring your presentation to life with natural intonation and pacing.',
        features: [
            'High-quality neural text-to-speech',
            'Natural pauses and emphasis',
            'Synchronized perfectly with slide transitions',
            'Crystal clear audio quality',
            'Engaging voice tones suitable for presentations'
        ]
    },
    music: {
        icon: '🎵',
        title: 'Smart Music Selection',
        description: 'The right background music sets the mood. Our AI analyzes your content to pick the perfect backing track.',
        features: [
            'Context-aware music matching',
            'Seamless looping and integration',
            'Auto-ducking (lowers volume during narration)',
            'Royalty-free premium tracks',
            'Mood matching (Upbeat, Professional, Calm)'
        ]
    },
    video: {
        icon: '🎬',
        title: 'Automated Video Assembly',
        description: 'We bring it all together into a polished MP4 video ready for sharing on YouTube, LinkedIn, or social media.',
        features: [
            'Full HD (1080p) video export',
            'Smooth slide transitions',
            'Perfect audio-visual synchronization',
            'Compressed for easy sharing',
            'Ready for streaming platforms'
        ]
    }
};

function openModal(featureKey) {
    const modal = document.getElementById('featureModal');
    const modalBody = document.getElementById('modalBody');
    const content = featureDetails[featureKey];

    if (!content) return;

    modalBody.innerHTML = `
        <div class="modal-header">
            <span class="modal-icon">${content.icon}</span>
            <h2 class="modal-title">${content.title}</h2>
        </div>
        <p class="modal-description">${content.description}</p>
        <div class="feature-list">
            <h3>Key Capabilities:</h3>
            <ul>
                ${content.features.map(feature => `<li>${feature}</li>`).join('')}
            </ul>
        </div>
    `;

    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden'; // Prevent scrolling
}

function closeModal(event) {
    if (!event || event.target.classList.contains('modal-overlay') ||
        event.target.classList.contains('close-modal') ||
        event.key === 'Escape') {

        document.getElementById('featureModal').classList.add('hidden');
        document.body.style.overflow = ''; // Restore scrolling
    }
}

// Close modal on Escape key
document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
        closeModal(event);
    }
});
