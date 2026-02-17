from flask import Flask, render_template, request, jsonify, session
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import base64
import io
from PIL import Image
from ultralytics import YOLO
import urllib.request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-to-something-random-and-long'

# EMAIL CONFIGURATION (OPTIONAL - for alerts)
# You can use Gmail, SendGrid, or any SMTP service
EMAIL_CONFIG = {
    'enabled': True,  # Set to True to enable email alerts
    'sender_email': 'sareenmohak@gmail.com',
    'sender_password': 'lybo oizs kcnm tzbe',  # Use app-specific password for Gmail
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}

# Define roles and their required PPE
ROLES_PPE = {
    'Welder': ['Hardhat', 'Safety Vest', 'Mask'],
    'Crane Operator': ['Hardhat', 'Safety Vest'],
    'General Laborer': ['Hardhat', 'Safety Vest'],
    'Site Inspector': ['Hardhat', 'Safety Vest'],
    'Carpenter': ['Hardhat', 'Safety Vest'],
    'Electrician': ['Hardhat', 'Safety Vest', 'Mask'],
    'Plumber': ['Hardhat', 'Safety Vest'],
    'Concrete Finisher': ['Hardhat', 'Safety Vest', 'Mask'],
    'Heavy Equipment Operator': ['Hardhat', 'Safety Vest'],
    'Safety Manager': ['Hardhat', 'Safety Vest'],
    'Mason': ['Hardhat', 'Safety Vest', 'Mask'],
    'Painter': ['Hardhat', 'Safety Vest', 'Mask'],
    'Roofer': ['Hardhat', 'Safety Vest'],
    'HVAC Technician': ['Hardhat', 'Safety Vest'],
    'Scaffolding Specialist': ['Hardhat', 'Safety Vest'],
    'Demolition Worker': ['Hardhat', 'Safety Vest', 'Mask'],
    'Quality Control Inspector': ['Hardhat', 'Safety Vest'],
    'Forklift Operator': ['Hardhat', 'Safety Vest'],
}

# Model classes
MODEL_CLASSES = {
    0: 'Hardhat',
    1: 'Mask', 
    2: 'NO-Hardhat',
    3: 'NO-Mask',
    4: 'NO-Safety Vest',
    5: 'Person',
    6: 'Safety Cone',
    7: 'Safety Vest',
    8: 'machinery',
    9: 'vehicle'
}

# File paths
USERS_FILE = 'users.json'
DETECTION_HISTORY_FILE = 'detection_history.json'
ADMIN_PASSWORD = 'admin123'  # Change this!

# ==================== DATABASE FUNCTIONS ====================

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def load_detection_history():
    if os.path.exists(DETECTION_HISTORY_FILE):
        with open(DETECTION_HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_detection_history(history):
    with open(DETECTION_HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def add_detection_record(username, role, required_ppe, detected_ppe, missing_ppe, compliant, photo_path):
    """Add a detection record to history"""
    history = load_detection_history()
    record = {
        'username': username,
        'role': role,
        'timestamp': datetime.now().isoformat(),
        'required_ppe': required_ppe,
        'detected_ppe': detected_ppe,
        'missing_ppe': missing_ppe,
        'compliant': compliant,
        'photo_path': photo_path
    }
    history.append(record)
    save_detection_history(history)
    return record

# ==================== EMAIL FUNCTIONS ====================

def send_email_alert(username, role, missing_ppe, worker_email=None):
    """Send email alert when PPE is missing"""
    if not EMAIL_CONFIG['enabled']:
        return False
    
    try:
        missing_items = ', '.join(missing_ppe)
        subject = f"⚠️ PPE Alert: {username} ({role}) missing {missing_items}"
        
        body = f"""
        <html>
            <body>
                <h2>⚠️ PPE Safety Alert</h2>
                <p><strong>Worker:</strong> {username}</p>
                <p><strong>Role:</strong> {role}</p>
                <p><strong>Missing PPE:</strong> {missing_items}</p>
                <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Please ensure the worker equips all required PPE before proceeding.</p>
            </body>
        </html>
        """
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = worker_email or EMAIL_CONFIG['sender_email']
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

# ==================== MODEL FUNCTIONS ====================

def get_model():
    model_path = 'best.pt'
    
    if not os.path.exists(model_path):
        print("Downloading custom PPE detection model...")
        url = "https://github.com/snehilsanyal/Construction-Site-Safety-PPE-Detection/raw/main/models/best.pt"
        try:
            urllib.request.urlretrieve(url, model_path)
            print("Model downloaded successfully!")
        except Exception as e:
            print(f"Could not download model: {e}")
            return YOLO('yolov8n.pt')
    
    return YOLO(model_path)

# ==================== ROUTES ====================

@app.route('/')
def home():
    return render_template('index.html', roles=json.dumps(list(ROLES_PPE.keys())))

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    
    users = load_users()
    
    if username in users:
        return jsonify({'success': False, 'message': 'Username already exists!'}), 400
    
    users[username] = {
        'password': password,
        'role': role,
        'created_at': datetime.now().isoformat()
    }
    save_users(users)
    
    return jsonify({'success': True, 'message': 'Registration successful! Please login.'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    
    users = load_users()
    
    if username not in users:
        return jsonify({'success': False, 'message': 'User not found!'}), 401
    
    if users[username]['password'] != password:
        return jsonify({'success': False, 'message': 'Wrong password!'}), 401
    
    session['username'] = username
    session['role'] = role
    session['required_ppe'] = ROLES_PPE[role]
    
    return jsonify({'success': True, 'message': 'Login successful!', 'role': role}), 200

@app.route('/get-ppe-requirements', methods=['GET'])
def get_ppe_requirements():
    role = request.args.get('role')
    if role in ROLES_PPE:
        return jsonify({'ppe': ROLES_PPE[role]}), 200
    return jsonify({'ppe': []}), 400

@app.route('/camera')
def camera():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    return render_template('camera.html', 
                         username=session['username'],
                         role=session['role'],
                         required_ppe=session['required_ppe'])

@app.route('/upload-photo', methods=['POST'])
def upload_photo():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        data = request.json
        image_data = data.get('image')
        
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        if not os.path.exists('photos'):
            os.makedirs('photos')
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"photos/{session['username']}_{timestamp}.jpg"
        image.save(filename)
        
        return jsonify({
            'success': True, 
            'message': 'Photo captured successfully!',
            'filename': filename
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/logout')
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

@app.route('/detect-ppe', methods=['POST'])
def detect_ppe():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        data = request.json
        filename = data.get('filename')
        
        model = get_model()
        results = model(filename, conf=0.5)
        
        detected_items = []
        
        for detection in results[0].boxes:
            class_id = int(detection.cls[0])
            class_name = MODEL_CLASSES.get(class_id, 'Unknown')
            confidence = float(detection.conf[0])
            
            if confidence > 0.3 and 'NO-' not in class_name and class_name != 'Person' and class_name not in ['Safety Cone', 'machinery', 'vehicle']:
                detected_items.append({
                    'item': class_name,
                    'confidence': round(confidence * 100, 2)
                })
        
        required_ppe = session.get('required_ppe', [])
        
        detected_ppe = []
        for detected in detected_items:
            item_name = detected['item']
            if item_name in required_ppe:
                if item_name not in detected_ppe:
                    detected_ppe.append(item_name)
        
        missing_ppe = [item for item in required_ppe if item not in detected_ppe]
        is_compliant = len(missing_ppe) == 0
        
        # Save detection record
        detection_record = add_detection_record(
            session['username'],
            session['role'],
            required_ppe,
            detected_ppe,
            missing_ppe,
            is_compliant,
            filename
        )
        
        # Send email alert if non-compliant and email enabled
        if not is_compliant and EMAIL_CONFIG['enabled']:
            send_email_alert(session['username'], session['role'], missing_ppe)
        
        return jsonify({
            'success': True,
            'detected_items': detected_items,
            'detected_ppe': detected_ppe,
            'required_ppe': required_ppe,
            'missing_ppe': missing_ppe,
            'compliant': is_compliant,
            'message': 'All PPE detected! You\'re good to go!' if is_compliant else f'Missing: {", ".join(missing_ppe)}'
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error during detection: {str(e)}'}), 500

# ==================== DETECTION HISTORY ====================

@app.route('/history')
def history():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    return render_template('history.html', username=session['username'])

@app.route('/get-user-history', methods=['GET'])
def get_user_history():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    username = session['username']
    history = load_detection_history()
    
    # Filter by current user
    user_history = [record for record in history if record['username'] == username]
    
    # Sort by timestamp (newest first)
    user_history.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return jsonify({'history': user_history}), 200

# ==================== ADMIN DASHBOARD ====================

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.json
    password = data.get('password')
    
    if password == ADMIN_PASSWORD:
        session['admin'] = True
        return jsonify({'success': True, 'message': 'Admin login successful'}), 200
    else:
        return jsonify({'success': False, 'message': 'Wrong admin password'}), 401

@app.route('/admin-logout')
def admin_logout():
    session.pop('admin', None)
    return jsonify({'success': True}), 200

@app.route('/admin-data', methods=['GET'])
def admin_data():
    if session.get('admin') != True:
        return jsonify({'error': 'Not authorized'}), 401
    
    history = load_detection_history()
    users = load_users()
    
    # Calculate statistics
    total_checks = len(history)
    passed_checks = sum(1 for record in history if record['compliant'])
    failed_checks = total_checks - passed_checks
    pass_rate = (passed_checks / total_checks * 100) if total_checks > 0 else 0
    
    # Group by user
    user_stats = {}
    for record in history:
        username = record['username']
        if username not in user_stats:
            user_stats[username] = {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'pass_rate': 0
            }
        user_stats[username]['total'] += 1
        if record['compliant']:
            user_stats[username]['passed'] += 1
        else:
            user_stats[username]['failed'] += 1
        user_stats[username]['pass_rate'] = (user_stats[username]['passed'] / user_stats[username]['total'] * 100)
    
    return jsonify({
        'total_checks': total_checks,
        'passed_checks': passed_checks,
        'failed_checks': failed_checks,
        'overall_pass_rate': round(pass_rate, 2),
        'user_stats': user_stats,
        'total_users': len(users),
        'recent_history': history[-20:]  # Last 20 records
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)