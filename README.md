# Presently 🎬

**AI-Powered Presentation Video Generator**

Transform any webpage into professional presentation videos with AI-generated narration, background music, and beautiful slides.

![Presently Logo](web/logo.png)

## ✨ Features

- 🌐 **Web Scraping** - Extract content and images from any webpage automatically
- 🤖 **AI Content Generation** - Google Gemini AI creates structured presentation content
- 📊 **Professional Slides** - Beautiful PowerPoint presentations with custom layouts
- 🎙️ **AI Narration** - Natural-sounding text-to-speech for each slide
- 🎵 **Smart Music Selection** - AI-powered background music matching your content
- 🎬 **Video Assembly** - Combines everything into a polished final video
- 🔐 **User Authentication** - Secure login and signup system
- 🌐 **Modern Web Interface** - Beautiful, responsive web UI

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- LibreOffice (for PPT to PDF conversion)
- Poppler (for PDF to image conversion)
- Google Gemini API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/RaoManoj2004/presently.git
   cd presently
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install system dependencies**
   - **LibreOffice**: Download from [libreoffice.org](https://www.libreoffice.org/)
   - **Poppler**: 
     - Windows: Download from [poppler releases](https://github.com/oschwartz10612/poppler-windows/releases)
     - Linux: `sudo apt-get install poppler-utils`
     - macOS: `brew install poppler`

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

5. **Run the web application**
   ```bash
   cd web
   python app.py
   ```

6. **Access the application**
   
   Open your browser and navigate to:
   - Main App: http://localhost:5000
   - Login: http://localhost:5000/login.html
   - Signup: http://localhost:5000/signup.html

## 📖 Usage

### Web Interface

1. **Create an account** or **log in**
2. **Enter a webpage URL** you want to convert
3. **Click "Generate Video"**
4. **Watch the progress** in real-time
5. **Download your video** when complete!

### Command Line (Original)

```bash
cd src
python main.py
```

Then enter the URL when prompted.

## 🏗️ Project Structure

```
presently/
├── src/                      # Core Python application
│   ├── main.py              # CLI entry point
│   ├── web_scraper.py       # Web content extraction
│   ├── content_generator.py # AI content generation
│   ├── convert_to_ppt.py    # PowerPoint creation
│   ├── music_selection.py   # Background music selection
│   ├── text_to_audio.py     # Text-to-speech generation
│   ├── convert_to_images.py # PPT to images conversion
│   └── generate_video.py    # Final video assembly
├── web/                      # Web frontend
│   ├── app.py               # Flask backend API
│   ├── index.html           # Main application page
│   ├── login.html           # Login page
│   ├── signup.html          # Signup page
│   ├── terms.html           # Terms of Service
│   ├── privacy.html         # Privacy Policy
│   ├── style.css            # Styles
│   └── script.js            # Frontend JavaScript
├── assets/                   # Static assets
│   └── music/               # Background music files
├── temp/                     # Temporary files (gitignored)
└── requirements.txt         # Python dependencies
```

## 🔧 Configuration

### Google API Setup

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

### API Models Used

- **Content Generation**: `gemini-2.0-flash`
- **Text-to-Speech**: `gemini-2.5-flash-tts`

## 🎨 Technologies

### Backend
- Python 3.14
- Flask (Web server)
- Flask-Login (Authentication)
- Flask-SQLAlchemy (Database)
- Google Generative AI (Content & TTS)
- MoviePy (Video editing)
- python-pptx (PowerPoint generation)
- BeautifulSoup4 (Web scraping)

### Frontend
- HTML5
- CSS3 (Modern design with glassmorphism)
- Vanilla JavaScript
- Google Fonts (Inter)

## 📝 API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/check` - Check login status

### Video Generation
- `POST /api/generate` - Start video generation
- `GET /api/progress/<job_id>` - Get generation progress
- `GET /api/download/<filename>` - Download generated video

## ⚠️ Known Limitations

- **API Quota**: Google Gemini API has free tier limits:
  - Content Generation: 200 requests/day
  - TTS: 15 requests/day, 3 requests/minute
- **Processing Time**: Video generation can take 5-10 minutes depending on content
- **File Size**: Large webpages may take longer to process

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Google Gemini AI for content generation and TTS
- LibreOffice for document conversion
- MoviePy for video processing
- All open-source contributors

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ by Manoj Rao**

⭐ Star this repo if you find it helpful!
