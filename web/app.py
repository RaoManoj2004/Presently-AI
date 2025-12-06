from flask import Flask, request, jsonify, send_file, session
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sys
import threading
import uuid
import time
from datetime import datetime

# Add parent directory to path to import presently modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from web_scraper import scrape_website
import content_generator
from convert_to_ppt import markdown_to_ppt
from music_selection import select_best_music
from text_to_audio import generate_audio_from_markdown
from convert_to_images import ppt_to_images
from generate_video import create_presentation_video

# Initialize Flask app
app = Flask(__name__, static_folder='.', static_url_path='')
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

# Initialize extensions
CORS(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# ===== Database Models =====
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ===== Job System =====
jobs = {}

class Job:
    def __init__(self, job_id, url):
        self.id = job_id
        self.url = url
        self.status = 'queued'
        self.progress = 0
        self.step = 0
        self.message = 'Queued'
        self.video_path = None
        self.ppt_path = None
        self.error = None

# ===== Mail Configuration =====
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@presently.app')

mail = Mail(app)

# ===== Token Serializer =====
def get_serializer():
    return URLSafeTimedSerializer(app.config['SECRET_KEY'])

# ===== Email Helper =====
def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Failed to send email: {e}")

def send_email(subject, recipient, template):
    msg = Message(
        subject,
        recipients=[recipient],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    thr = threading.Thread(target=send_async_email, args=[app, msg])
    thr.start()

# ===== Authentication Routes =====
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    fullname = data.get('fullname')
    email = data.get('email')
    password = data.get('password')
    
    # Validation
    if not fullname or not email or not password:
        return jsonify({'message': 'All fields are required'}), 400
    
    if len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters'}), 400
    
    # Check if user exists
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered'}), 400
    
    # Create new user
    user = User(fullname=fullname, email=email)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    # Send Welcome Email
    welcome_html = f"""
    <h3>Welcome to Presently, {fullname}!</h3>
    <p>We are thrilled to have you on board.</p>
    <p>Start transforming your web content into amazing presentations and videos today.</p>
    <br>
    <p>Best regards,<br>The Presently Team</p>
    """
    send_email("Welcome to Presently!", email, welcome_html)
    
    return jsonify({'message': 'Account created successfully'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid email or password'}), 401
    
    login_user(user)
    
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'fullname': user.fullname,
            'email': user.email
        }
    }), 200

@app.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'message': 'Email is required'}), 400
        
    user = User.query.filter_by(email=email).first()
    if not user:
        # Don't reveal account existence
        return jsonify({'message': 'If an account exists, a reset link has been sent.'}), 200
        
    # Generate token
    s = get_serializer()
    token = s.dumps(email, salt='password-reset-salt')
    
    # Send Reset Email (assuming localhost for link, ideally use request.host_url)
    link = f"{request.host_url}reset_password.html?token={token}"
    
    reset_html = f"""
    <h3>Password Reset Request</h3>
    <p>Click the link below to reset your password:</p>
    <p><a href="{link}">Reset Password</a></p>
    <p>If you did not request this, please ignore this email.</p>
    """
    
    send_email("Reset Your Password", email, reset_html)
    
    return jsonify({'message': 'If an account exists, a reset link has been sent.'}), 200

@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('password')
    
    if not token or not new_password:
        return jsonify({'message': 'Token and new password are required'}), 400
        
    s = get_serializer()
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600) # 1 hour expiry
    except Exception:
        return jsonify({'message': 'Invalid or expired token'}), 400
        
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
        
    user.set_password(new_password)
    db.session.commit()
    
    return jsonify({'message': 'Password has been reset successfully'}), 200

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/auth/check', methods=['GET'])
def check_auth():
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': current_user.id,
                'fullname': current_user.fullname,
                'email': current_user.email
            }
        }), 200
    else:
        return jsonify({'authenticated': False}), 200

# ===== Video Generation Routes =====
@app.route('/api/generate', methods=['POST'])
@login_required
def generate_video():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'message': 'URL is required'}), 400
    
    # Create job
    job_id = str(uuid.uuid4())
    job = Job(job_id, url)
    jobs[job_id] = job
    
    # Start background processing
    thread = threading.Thread(target=process_video, args=(job,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'job_id': job_id}), 202

def process_video(job):
    try:
        workspace_root = os.path.join(os.path.dirname(__file__), '..')
        
        # Step 1: Web Scraping
        job.step = 1
        job.progress = 10
        job.message = 'Extracting content from webpage...'
        
        _, content_dict, image_paths, markdown_path, workspace_root, url = scrape_website(job.url)
        
        # Step 2: Content Generation
        job.step = 2
        job.progress = 30
        job.message = 'Generating presentation structure with AI...'
        
        presentation_content = content_generator.generate_content(markdown_path)
        presentation_content_path = os.path.join(workspace_root, "temp", "presentation.md")
        with open(presentation_content_path, 'w', encoding='utf-8') as f:
            f.write(presentation_content)
        
        # Step 3: PowerPoint Creation
        job.step = 3
        job.progress = 45
        job.message = 'Creating PowerPoint presentation...'
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ppt_filename = f"presentation_{timestamp}.ppt"
        markdown_to_ppt(workspace_root, output_file=os.path.join(workspace_root, "temp", ppt_filename))
        
        # Step 4: Music Selection
        job.step = 4
        job.progress = 55
        job.message = 'Selecting background music...'
        
        select_best_music(workspace_root, presentation_content)
        
        # Step 5: Audio Generation
        job.step = 5
        job.progress = 65
        job.message = 'Generating AI narration...'
        
        generate_audio_from_markdown(presentation_content, os.path.join(workspace_root, "temp", "audio"))
        
        # Step 6: Image Conversion & Video Assembly
        job.step = 6
        job.progress = 85
        job.message = 'Finalizing presentation and video...'
        
        ppt_to_images_path = ppt_to_images(workspace_root=workspace_root)
        presentation_video_path = create_presentation_video(workspace_root=workspace_root)
        
        # Complete
        job.status = 'completed'
        job.progress = 100
        job.message = 'Generation successful!'
        job.video_path = os.path.basename(presentation_video_path)
        job.ppt_path = ppt_filename
        
    except Exception as e:
        job.status = 'error'
        job.error = str(e)
        job.message = f'Error: {str(e)}'

@app.route('/api/progress/<job_id>', methods=['GET'])
@login_required
def get_progress(job_id):
    job = jobs.get(job_id)
    
    if not job:
        return jsonify({'message': 'Job not found'}), 404
    
    return jsonify({
        'status': job.status,
        'progress': job.progress,
        'step': job.step,
        'message': job.message,
        'video_path': job.video_path,
        'ppt_path': job.ppt_path,
        'error': job.error
    }), 200

@app.route('/api/download/<filename>', methods=['GET'])
@login_required
def download_video(filename):
    workspace_root = os.path.join(os.path.dirname(__file__), '..')
    video_path = os.path.join(workspace_root, 'temp', filename)
    
    if not os.path.exists(video_path):
        return jsonify({'message': 'File not found'}), 404
    
    return send_file(video_path, as_attachment=True, download_name=filename)

# ===== Static File Routes =====
@app.route('/')
def index():
    if current_user.is_authenticated:
        return app.send_static_file('index.html')
    else:
        return app.send_static_file('login.html')

@app.route('/login.html')
def login_page():
    return app.send_static_file('login.html')

@app.route('/signup.html')
def signup_page():
    return app.send_static_file('signup.html')

# ===== Initialize Database =====
with app.app_context():
    db.create_all()
    print("Database initialized!")

# ===== Run Server =====
if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Presently Web Server Starting...")
    print("="*50)
    print(f"📍 Server: http://localhost:5000")
    print(f"🔐 Login: http://localhost:5000/login.html")
    print(f"📝 Signup: http://localhost:5000/signup.html")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
