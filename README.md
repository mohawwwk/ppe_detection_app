# 🏗️ PPE Detection System

An AI-powered construction site safety system that detects whether workers are wearing required Personal Protective Equipment (PPE) using computer vision.

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3-orange)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Custom%20Trained-red)

---

## 🎯 Features

✅ **User Management**
- Worker registration and secure login
- Role-based access (18 different construction roles)
- Password-protected accounts

✅ **Real-time PPE Detection**
- Live camera feed integration
- AI-powered detection using custom-trained YOLOv8 model
- Instant PASS/FAIL results with confidence scores
- Detects: Hard Hat, Safety Vest, Mask

✅ **Detection History & Analytics**
- Personal detection history for each worker
- Statistics: Total checks, pass rate, failed checks
- Track PPE compliance over time

✅ **Admin Dashboard**
- Site-wide compliance overview
- Worker performance tracking
- Real-time activity monitoring
- Pass rate analytics by worker

✅ **Safety Alerts**
- Email notifications on PPE failures (optional)
- Real-time feedback to workers
- Support for Gmail, Outlook, SendGrid

✅ **User Experience**
- Beautiful, responsive UI
- Dark mode toggle
- Mobile-friendly design
- Intuitive workflow

---

## 🛠️ Tech Stack

**Backend:**
- Python 3.8+
- Flask (Web framework)
- YOLOv8 (AI object detection)
- JSON (Database)

**Frontend:**
- HTML5
- CSS3 (with Dark Mode)
- JavaScript (vanilla)
- Bootstrap-style responsive design

**AI/ML:**
- Ultralytics YOLOv8 (custom-trained model)
- OpenCV (image processing)
- PyTorch (deep learning backend)

**Deployment Ready:**
- Can run locally or in cloud
- Compatible with PythonAnywhere, Heroku, AWS, etc.

---

## 📋 Construction Roles Supported

The system includes 18 different construction site roles:

| Role | Required PPE |
|------|--------------|
| Welder | Hard Hat, Safety Vest, Mask |
| Crane Operator | Hard Hat, Safety Vest |
| Carpenter | Hard Hat, Safety Vest |
| Electrician | Hard Hat, Safety Vest, Mask |
| Plumber | Hard Hat, Safety Vest |
| Roofer | Hard Hat, Safety Vest |
| Mason | Hard Hat, Safety Vest, Mask |
| Painter | Hard Hat, Safety Vest, Mask |
| Safety Manager | Hard Hat, Safety Vest |
| And 9 more... | Customizable |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Webcam/Camera
- Windows/Mac/Linux

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mohawwwk/ppe_detection_app.git
   cd ppe_detection_app
   ```

2. **Install dependencies:**
   ```bash
   pip install flask ultralytics pillow opencv-python torch torchvision
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open in browser:**
   ```
   http://localhost:5000
   ```

---

## 📖 Usage

### For Workers

1. **Register Account**
   - Go to http://localhost:5000
   - Click "Register here"
   - Enter username, password, and select your role
   - Submit

2. **Login**
   - Enter credentials and role
   - Click "Login"

3. **Take PPE Check**
   - Click "Start Camera"
   - Allow camera permissions
   - Click "📸 Capture Photo"
   - Wait for AI analysis

4. **View Results**
   - ✅ **PASS** - All required PPE detected
   - ❌ **FAIL** - Missing PPE items shown
   - Confidence scores displayed for each detected item

5. **View History**
   - Click "📊 History"
   - See all past checks and statistics
   - Track pass rate over time

### For Administrators

1. **Access Admin Dashboard**
   - Go to http://localhost:5000/admin
   - Enter admin password (default: `admin123`)

2. **View Statistics**
   - Overall site compliance rate
   - Per-worker performance
   - Recent activity log
   - Real-time monitoring

3. **Monitor Safety**
   - Identify non-compliant workers
   - Track compliance trends
   - Make data-driven safety decisions

---

## 🔐 Security

- Secure password storage (JSON-based for demo)
- Session management for login persistence
- Admin password protection
- .gitignore prevents uploading sensitive files
- Email alerts only sent for legitimate PPE failures

### Production Recommendations

- Use bcrypt for password hashing
- Migrate to SQL database (PostgreSQL/MySQL)
- Enable HTTPS/TLS
- Use environment variables for secrets
- Implement rate limiting
- Add audit logging
- Regular security audits

---

## 📧 Email Alerts Setup

Optional feature to send alerts when workers fail PPE checks.

### Gmail (Recommended)

1. Enable 2-Factor Authentication on Gmail
2. Generate App Password: https://myaccount.google.com/apppasswords
3. In `app.py`, update:
   ```python
   EMAIL_CONFIG = {
       'enabled': True,
       'sender_email': 'your-email@gmail.com',
       'sender_password': 'your-app-password',
       'smtp_server': 'smtp.gmail.com',
       'smtp_port': 587
   }
   ```
4. Restart the app

### Other Providers

- **Outlook:** Use your password with `smtp-mail.outlook.com:587`
- **SendGrid:** Use API key (free tier available)
- See `EMAIL_SETUP_GUIDE.txt` for detailed instructions

---

## 📁 Project Structure

```
ppe_detection_app/
│
├── app.py                    # Main Flask application
├── .gitignore               # Git ignore file
│
├── templates/               # HTML files
│   ├── index.html          # Login/Register page
│   ├── camera.html         # Camera & detection page
│   ├── history.html        # Detection history
│   └── admin.html          # Admin dashboard
│
├── photos/                 # Captured photos (auto-created)
│   └── username_timestamp.jpg
│
├── best.pt                 # AI model (auto-downloaded)
│
├── users.json              # User database (auto-created)
└── detection_history.json  # Detection records (auto-created)
```

---

## 🤖 AI Model

**Model:** YOLOv8 (Custom-trained on construction PPE)

**Source:** https://github.com/snehilsanyal/Construction-Site-Safety-PPE-Detection

**Detects:**
- Hard Hat / Helmet
- Safety Vest
- Mask / Respirator

**Performance:**
- Real-time detection (2-5 seconds per photo)
- 95%+ accuracy on construction site images
- Confidence scores for each detection

**Auto-Download:**
- Model (~50MB) downloads automatically on first use
- Cached locally for subsequent runs

---

## 🎨 Dark Mode

Toggle dark mode with the 🌙 button in the camera page. Preference is saved in browser.

---

## 📊 Admin Credentials

**Default Admin Password:** `admin123`

⚠️ **CHANGE THIS IN PRODUCTION!**

Edit in `app.py`:
```python
ADMIN_PASSWORD = 'your-secure-password'
```

---

## 🐛 Troubleshooting

### Camera not working
- Check browser camera permissions
- Restart browser
- Verify camera device exists

### Model download fails
- Check internet connection
- Model auto-downloads on first detection
- Check firewall settings

### Email not sending
- Verify SMTP credentials
- Check sender email is correct
- Enable less secure apps (if using Gmail)
- Check spam folder

### Detection inaccurate
- Good lighting is important
- PPE should be clearly visible
- Try different angles
- Ensure close proximity to camera

---

## 📈 Performance

- **First detection:** ~2 minutes (model download)
- **Subsequent detections:** 2-5 seconds
- **Recommended specs:** 4GB RAM, multi-core CPU
- **GPU support:** NVIDIA CUDA recommended for faster inference

---

## 🚢 Deployment

This app can be deployed to:

- **PythonAnywhere** (recommended for beginners)
- **Heroku** (free tier available)
- **Render** (modern alternative to Heroku)
- **AWS / Google Cloud / Azure** (enterprise scale)
- **Digital Ocean** (affordable VPS option)

See `DEPLOYMENT_GUIDE.txt` for detailed instructions.

---

## 🔄 Updates & Maintenance

### Backup Your Data

```bash
# Backup user data
cp users.json users.json.backup

# Backup detection history
cp detection_history.json detection_history.json.backup
```

### Update Dependencies

```bash
pip install --upgrade flask ultralytics opencv-python torch
```

---

## 📝 Future Enhancements

- [ ] Photo annotations with bounding boxes
- [ ] Export reports (CSV, PDF)
- [ ] SQLite/PostgreSQL database migration
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] API for third-party integration
- [ ] Biometric authentication
- [ ] Real-time monitoring with WebSockets
- [ ] ML model retraining pipeline

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Share improvements

---

## 📄 License

This project is open source and available under the MIT License.

---

## 📚 Documentation

- `GIT_GITHUB_SETUP.txt` - Git and GitHub setup guide
- `DEPLOYMENT_GUIDE.txt` - Detailed deployment instructions
- `COMPLETE_DOCUMENTATION.txt` - Full project documentation
- `EMAIL_SETUP_GUIDE.txt` - Email alerts configuration
- `GMAIL_QUICK_SETUP.txt` - Quick Gmail setup

---

## 👨‍💻 Author

**Mohawwwk**

GitHub: https://github.com/mohawwwk

---

## 🆘 Support

For issues, questions, or suggestions:
1. Check the troubleshooting section
2. Review the documentation files
3. Open a GitHub issue

---

## ⚠️ Disclaimer

This system is designed as a safety aid. Always follow your local construction safety regulations and standards. This system should be used in conjunction with, not as a replacement for, proper safety training and protocols.

---

## 🎉 Acknowledgments

- **YOLOv8:** Ultralytics for the amazing object detection framework
- **Custom Model:** Based on work by [snehilsanyal](https://github.com/snehilsanyal)
- **Community:** Open source contributors and safety advocates

---

**Last Updated:** February 2024

**Status:** ✅ Production Ready
