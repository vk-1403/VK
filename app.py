import os
import logging
from flask import Flask, render_template_string, request, jsonify, send_file
from datetime import datetime
import base64
from flask_mail import Mail, Message

# Create Flask app FIRST
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")

# Configure Flask-Mail AFTER app is created
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vidyapatikumar.me@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('GMAIL_APP_PASSWORD')  # Secure env var
app.config['MAIL_DEFAULT_SENDER'] = 'vidyapatikumar.me@gmail.com'

mail = Mail(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Profile photo (base64 encoded)
def get_profile_image():
    """Load and encode the profile image"""
    try:
        with open("mypic/VK.png", "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except:
        # Return a placeholder SVG if image not found
        return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxjaXJjbGUgY3g9IjEwMCIgY3k9IjEwMCIgcj0iMTAwIiBmaWxsPSIjMzQ5OGRiIi8+Cjx0ZXh0IHg9IjEwMCIgeT0iMTEwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSJ3aGl0ZSIgZm9udC1zaXplPSI3MCI+VktLPC90ZXh0Pgo8L3N2Zz4="

# Enhanced CSS with professional styling
CSS_STYLES = """
<style>
    :root {
        --primary-blue: #2c3e50;
        --accent-blue: #3498db;
        --light-blue: #ecf0f1;
        --dark-text: #2c3e50;
        --light-text: #7f8c8d;
        --white: #ffffff;
        --success-green: #27ae60;
        --royal-blue: #2E74B5;
        --forest-green: #228B22;
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: var(--dark-text);
        background-color: #f8f9fa;
    }

    .navbar {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--accent-blue) 100%);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }

    .navbar-brand {
        font-weight: 700;
        font-size: 1.5rem;
        color: white !important;
    }

    .navbar-nav .nav-link {
        color: white !important;
        font-weight: 500;
        margin: 0 10px;
        transition: color 0.3s ease;
    }

    .navbar-nav .nav-link:hover {
        color: var(--light-blue) !important;
    }

    .hero-section {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--accent-blue) 100%);
        color: white;
        padding: 100px 0;
    }

    .profile-photo {
        width: 220px;
        height: 220px;
        border-radius: 50%;
        border: 5px solid white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        object-fit: cover;
        margin-bottom: 30px;
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .hero-subtitle {
        font-size: 1.4rem;
        margin-bottom: 20px;
        opacity: 0.9;
    }

    .hero-description {
        font-size: 1.1rem;
        opacity: 0.85;
        max-width: 900px;
        margin: 0 auto 30px;
        line-height: 1.7;
    }

    .social-links a {
        color: white;
        font-size: 1.8rem;
        margin: 0 20px;
        transition: all 0.3s ease;
        text-decoration: none;
    }

    .social-links a:hover {
        transform: translateY(-3px);
        color: var(--light-blue);
        text-shadow: 0 5px 15px rgba(255,255,255,0.3);
    }

    .section-title {
        color: var(--primary-blue);
        font-weight: 700;
        margin-bottom: 40px;
        position: relative;
        padding-bottom: 15px;
        font-size: 2.5rem;
    }

    .section-title::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 4px;
        background: var(--accent-blue);
        border-radius: 2px;
    }

    .card {
        border: none;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        margin-bottom: 30px;
        border-radius: 10px;
    }

    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    }

    .card-header {
        background: var(--accent-blue);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 10px 10px 0 0 !important;
    }

    .experience-item {
        border-left: 4px solid var(--accent-blue);
        padding-left: 25px;
        margin-bottom: 40px;
        position: relative;
        background: white;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .experience-item::before {
        content: '';
        width: 16px;
        height: 16px;
        background: var(--accent-blue);
        border-radius: 50%;
        position: absolute;
        left: -10px;
        top: 30px;
        border: 3px solid white;
        box-shadow: 0 0 0 3px var(--accent-blue);
    }

    .experience-title {
        color: var(--primary-blue);
        font-weight: 700;
        font-size: 1.3rem;
        margin-bottom: 8px;
    }

    .experience-company {
        color: var(--accent-blue);
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 5px;
    }

    .experience-date {
        color: var(--light-text);
        font-style: italic;
        font-weight: 500;
        margin-bottom: 15px;
    }

    .skill-tag {
        background: linear-gradient(45deg, var(--light-blue), #d5dbdb);
        color: var(--primary-blue);
        padding: 8px 16px;
        border-radius: 25px;
        margin: 5px;
        display: inline-block;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }

    .skill-tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }

    .publication-item {
        background: white;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-left: 4px solid var(--accent-blue);
        transition: all 0.3s ease;
    }

    .publication-item:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.15);
    }

    .publication-title {
        color: var(--primary-blue);
        font-weight: 700;
        margin-bottom: 10px;
        font-size: 1.1rem;
    }

    .publication-journal {
        color: var(--accent-blue);
        font-style: italic;
        font-weight: 500;
        margin-bottom: 8px;
    }

    .research-interest {
        background: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }

    .research-interest:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }

    .research-interest i {
        font-size: 3.5rem;
        color: var(--accent-blue);
        margin-bottom: 20px;
    }

    .education-table {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }

    .education-table th {
        background: var(--accent-blue);
        color: white;
        font-weight: 700;
        padding: 20px;
        font-size: 1.1rem;
    }

    .education-table td {
        padding: 20px;
        border-bottom: 1px solid #eee;
        font-weight: 500;
    }

    .patent-item {
        background: white;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-left: 4px solid var(--royal-blue);
    }

    .contact-form {
        background: white;
        padding: 50px;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }

    .btn-primary {
        background: linear-gradient(45deg, var(--accent-blue), var(--primary-blue));
        border: none;
        padding: 15px 35px;
        font-weight: 700;
        transition: all 0.3s ease;
        border-radius: 25px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    .footer {
        background: var(--primary-blue);
        color: white;
        padding: 50px 0;
        margin-top: 100px;
    }

    @media (max-width: 768px) {
        .hero-title { font-size: 2.5rem; }
        .hero-subtitle { font-size: 1.2rem; }
        .profile-photo { width: 180px; height: 180px; }
        .contact-form { padding: 30px; }
        .section-title { font-size: 2rem; }
    }
</style>
"""

# Embedded JavaScript
JAVASCRIPT = """
<script>
    // Smooth scrolling for navigation links
    document.addEventListener('DOMContentLoaded', function() {
        const navLinks = document.querySelectorAll('a[href^="#"]');
        
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Contact form submission
        const contactForm = document.getElementById('contact-form');
        if (contactForm) {
            contactForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                const formData = new FormData(this);
                const data = Object.fromEntries(formData);
                
                fetch('/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Thank you for your message! I will get back to you soon.');
                        this.reset();
                    } else {
                        alert('Sorry, there was an error sending your message. Please try again.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Sorry, there was an error sending your message. Please try again.');
                });
            });
        }

        // Navbar scroll effect
        window.addEventListener('scroll', function() {
            const navbar = document.querySelector('.navbar');
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(44, 62, 80, 0.95)';
            } else {
                navbar.style.background = 'linear-gradient(135deg, var(--primary-blue) 0%, var(--accent-blue) 100%)';
            }
        });
    });
</script>
"""

# Comprehensive HTML template with all resume details
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <meta name="description" content="Vidyapati Kumar - PhD candidate in Mechanical Engineering at IIT Kharagpur specializing in AI-driven biomechatronic systems and intelligent prosthetics">
    <meta name="keywords" content="Vidyapati Kumar, PhD, Mechanical Engineering, AI, Biomechatronics, Prosthetics, Machine Learning, IIT Kharagpur, Postdoc">
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    {{ css_styles|safe }}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
        <div class="container">
            <a class="navbar-brand" href="#home">Vidyapati Kumar</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="#home">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="#about">About</a></li>
                    <li class="nav-item"><a class="nav-link" href="#education">Education</a></li>
                    <li class="nav-item"><a class="nav-link" href="#experience">Experience</a></li>
                    <li class="nav-item"><a class="nav-link" href="#patents">Patents</a></li>
                    <li class="nav-item"><a class="nav-link" href="#publications">Publications</a></li>
                    <li class="nav-item"><a class="nav-link" href="#skills">Skills</a></li>
                    <li class="nav-item"><a class="nav-link" href="#contact">Contact</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="hero-section">
        <div class="container text-center">
            <img src="data:image/jpeg;base64,{{ profile_image }}" alt="Vidyapati Kumar" class="profile-photo">
            <h1 class="hero-title">Vidyapati Kumar</h1>
            <p class="hero-subtitle">PhD Candidate in Mechanical Engineering</p>
            <p class="hero-subtitle">IIT Kharagpur, India • CGPA: 8.5/10</p>
            <p class="hero-description">
                Ph.D. candidate specializing in AI-driven biomechatronic systems, intelligent prosthetics, and wearable health technologies. 
                My work explores the integration of sensor data, embedded platforms, and machine learning for real-time decision-making in healthcare-related contexts.
                Currently seeking postdoctoral opportunities in AI-enabled healthcare robotics and biomechanics.
            </p>
            <div class="social-links">
                <a href="https://rb.gy/xh4gy" target="_blank" title="Google Scholar">
                    <i class="fas fa-graduation-cap"></i>
                </a>
                <a href="https://in.linkedin.com/in/vidyapati-kumar-37332251" target="_blank" title="LinkedIn">
                    <i class="fab fa-linkedin"></i>
                </a>
                <a href="https://www.researchgate.net/profile/Vidyapati-Kumar" target="_blank" title="ResearchGate">
                    <i class="fab fa-researchgate"></i>
                </a>
                <a href="mailto:vidyapatikumar.me@gmail.com" title="Email">
                    <i class="fas fa-envelope"></i>
                </a>
                <a href="tel:+918017847748" title="Phone">
                    <i class="fas fa-phone"></i>
                </a>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="py-5">
        <div class="container">
            <h2 class="section-title text-center">About Me</h2>
            <div class="row">
                <div class="col-lg-10 mx-auto">
                    <div class="card">
                        <div class="card-body p-4">
                            <p class="lead">
                                I am a Ph.D. candidate in Mechanical Engineering at IIT Kharagpur, currently working on AI-based biomechatronic systems, 
                                with a focus on intelligent prosthetics and wearable health applications. My work explores the integration of sensor data, 
                                embedded platforms, and machine learning for real-time decision-making in healthcare-related contexts.
                            </p>
                            <p>
                                I have been fortunate to contribute to interdisciplinary projects involving computer vision, physiological signal analysis, 
                                and assistive technologies. I'm genuinely interested in exploring collaborative research that brings together AI, 
                                human sensing, and healthcare innovation.
                            </p>
                            <div class="row mt-4">
                                <div class="col-md-6">
                                    <h5><i class="fas fa-user text-primary"></i> Personal Info</h5>
                                    <ul class="list-unstyled">
                                        <li><strong>Email:</strong> vidyapatikumar.me@gmail.com</li>
                                        <li><strong>Phone:</strong> +91-8017847748</li>
                                        <li><strong>Location:</strong> Kharagpur, India</li>
                                        <li><strong>Status:</strong> Seeking Postdoc Opportunities</li>
                                    </ul>
                                </div>
                                <div class="col-md-6">
                                    <h5><i class="fas fa-chart-line text-primary"></i> Quick Stats</h5>
                                    <ul class="list-unstyled">
                                        <li><strong>Publications:</strong> 30+ Peer-reviewed</li>
                                        <li><strong>Patents:</strong> 2 Filed (1 Published)</li>
                                        <li><strong>Citations:</strong> Available on Google Scholar</li>
                                        <li><strong>Experience:</strong> 7+ Years Research</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Research Interests -->
            <div class="row mt-5">
                <div class="col-12">
                    <h3 class="text-center mb-4">Research Interests</h3>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="research-interest">
                        <i class="fas fa-robot"></i>
                        <h5>AI-Driven Biomechatronics</h5>
                        <p>Intelligent prosthetic systems with real-time control and multimodal sensor fusion</p>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="research-interest">
                        <i class="fas fa-brain"></i>
                        <h5>Machine Learning & AI</h5>
                        <p>Vision Transformers, deep learning, and explainable AI for healthcare applications</p>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="research-interest">
                        <i class="fas fa-heartbeat"></i>
                        <h5>Healthcare Technology</h5>
                        <p>Wearable health monitoring, assistive devices, and clinical decision support systems</p>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="research-interest">
                        <i class="fas fa-microchip"></i>
                        <h5>Embedded IoT Systems</h5>
                        <p>ESP32, Raspberry Pi, sensor fusion, and real-time data processing platforms</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Education Section -->
    <section id="education" class="py-5 bg-light">
        <div class="container">
            <h2 class="section-title text-center">Education</h2>
            <div class="row">
                <div class="col-12">
                    <div class="education-table">
                        <table class="table table-responsive mb-0">
                            <thead>
                                <tr>
                                    <th>Year</th>
                                    <th>Degree</th>
                                    <th>Institute</th>
                                    <th>CGPA</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>2025 (Pursuing)</strong></td>
                                    <td>Ph.D. (Mechanical Engineering)</td>
                                    <td>IIT Kharagpur, India</td>
                                    <td><span class="badge bg-success">8.5 / 10</span></td>
                                </tr>
                                <tr>
                                    <td><strong>2018</strong></td>
                                    <td>M.E. (Production Engineering)</td>
                                    <td>Jadavpur University, India</td>
                                    <td><span class="badge bg-success">8.38 / 10</span></td>
                                </tr>
                                <tr>
                                    <td><strong>2016</strong></td>
                                    <td>B.Tech (Mechanical Engineering)</td>
                                    <td>MAKAUT, India</td>
                                    <td><span class="badge bg-success">9.19 / 10</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Experience Section -->
    <section id="experience" class="py-5">
        <div class="container">
            <h2 class="section-title text-center">Professional Experience</h2>
            
            <div class="experience-item">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <div>
                        <h4 class="experience-title">Senior Research Fellow</h4>
                        <p class="experience-company">Indian Institute of Technology Kharagpur</p>
                        <p class="mb-1"><strong>Project:</strong> AI-Enhanced Powered Ankle-Foot Prosthetic System</p>
                    </div>
                    <span class="experience-date">Jul 2021 - Present</span>
                </div>
                <ul class="list-unstyled">
                    <li><i class="fas fa-check-circle text-success me-2"></i>Designed microcontroller-based sensor fusion platform using ESP32 and Raspberry Pi</li>
                    <li><i class="fas fa-check-circle text-success me-2"></i>Developed multimodal control strategy for powered ankle-foot prosthesis</li>
                    <li><i class="fas fa-check-circle text-success me-2"></i>Built comprehensive Python-based ML pipelines achieving >90% accuracy in gait phase detection</li>
                    <li><i class="fas fa-check-circle text-success me-2"></i>Implemented computer vision using Vision Transformers and YOLOv8 for gait analysis</li>
                    <li><i class="fas fa-check-circle text-success me-2"></i>Developed LLM-driven clinical decision support tool using LangChain and Streamlit</li>
                </ul>
            </div>

            <div class="experience-item">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <div>
                        <h4 class="experience-title">Project Mentor</h4>
                        <p class="experience-company">TIH Foundation for IoT and IoE (IIT Bombay)</p>
                        <p class="mb-1"><strong>Project:</strong> Chanakya Fellowship - Intelligent Prosthetic Development</p>
                    </div>
                    <span class="experience-date">Feb 2024 - Present</span>
                </div>
                <ul class="list-unstyled">
                    <li><i class="fas fa-check-circle text-success me-2"></i>Leading prestigious DST-funded project under Chanakya Fellowship Scheme</li>
                    <li><i class="fas fa-check-circle text-success me-2"></i>Mentoring end-to-end IoT-enabled prosthetic system development</li>
                    <li><i class="fas fa-check-circle text-success me-2"></i>Coordinating cross-functional teams across hardware, firmware, and cloud layers</li>
                </ul>
            </div>

            <div class="experience-item">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <div>
                        <h4 class="experience-title">Teaching Assistant</h4>
                        <p class="experience-company">IIT Kharagpur - NPTEL Courses</p>
                    </div>
                    <span class="experience-date">Jan 2021 - Present</span>
                </div>
                <ul class="list-unstyled">
                    <li><i class="fas fa-check-circle text-success me-2"></i>Assisted in delivering NPTEL courses on Robotics, Fuzzy Logic, and Optimization Tools</li>
                    <li><i class="fas fa-check-circle text-success me-2"></i>Developed code examples in Python and MATLAB</li>
                </ul>
            </div>
        </div>
    </section>

    <!-- Skills Section -->
    <section id="skills" class="py-5 bg-light">
        <div class="container">
            <h2 class="section-title text-center">Technical Skills & Expertise</h2>
            <div class="row">
                <div class="col-lg-4 mb-4">
                    <div class="card h-100">
                        <div class="card-header">
                            <i class="fas fa-brain me-2"></i>Machine Learning & AI
                        </div>
                        <div class="card-body">
                            <div class="skill-tag">Python</div>
                            <div class="skill-tag">TensorFlow</div>
                            <div class="skill-tag">PyTorch</div>
                            <div class="skill-tag">Scikit-learn</div>
                            <div class="skill-tag">Pandas</div>
                            <div class="skill-tag">NumPy</div>
                            <div class="skill-tag">SciPy</div>
                            <div class="skill-tag">SHAP</div>
                            <div class="skill-tag">XGBoost</div>
                            <div class="skill-tag">SBLSTM</div>
                            <div class="skill-tag">Extra Trees</div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 mb-4">
                    <div class="card h-100">
                        <div class="card-header">
                            <i class="fas fa-eye me-2"></i>Computer Vision & Deep Learning
                        </div>
                        <div class="card-body">
                            <div class="skill-tag">Vision Transformers</div>
                            <div class="skill-tag">YOLOv8</div>
                            <div class="skill-tag">OpenPose</div>
                            <div class="skill-tag">RTM Pose</div>
                            <div class="skill-tag">OpenCV</div>
                            <div class="skill-tag">Grad-CAM</div>
                            <div class="skill-tag">Saliency Maps</div>
                            <div class="skill-tag">Gait Energy Images</div>
                            <div class="skill-tag">Background Subtraction</div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 mb-4">
                    <div class="card h-100">
                        <div class="card-header">
                            <i class="fas fa-microchip me-2"></i>Embedded & IoT Systems
                        </div>
                        <div class="card-body">
                            <div class="skill-tag">ESP32</div>
                            <div class="skill-tag">Raspberry Pi</div>
                            <div class="skill-tag">Arduino</div>
                            <div class="skill-tag">IMU Sensors</div>
                            <div class="skill-tag">LiDAR</div>
                            <div class="skill-tag">FSR Sensors</div>
                            <div class="skill-tag">sEMG</div>
                            <div class="skill-tag">Maxon Motors</div>
                            <div class="skill-tag">Sensor Fusion</div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 mb-4">
                    <div class="card h-100">
                        <div class="card-header">
                            <i class="fas fa-tools me-2"></i>Engineering & Simulation
                        </div>
                        <div class="card-body">
                            <div class="skill-tag">MATLAB</div>
                            <div class="skill-tag">COMSOL</div>
                            <div class="skill-tag">FEA</div>
                            <div class="skill-tag">OpenSim</div>
                            <div class="skill-tag">CAD Modeling</div>
                            <div class="skill-tag">MCDM</div>
                            <div class="skill-tag">Optimization</div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 mb-4">
                    <div class="card h-100">
                        <div class="card-header">
                            <i class="fas fa-laptop-code me-2"></i>Software Development
                        </div>
                        <div class="card-body">
                            <div class="skill-tag">LangChain</div>
                            <div class="skill-tag">Streamlit</div>
                            <div class="skill-tag">Flask</div>
                            <div class="skill-tag">Git</div>
                            <div class="skill-tag">VBASIC</div>
                            <div class="skill-tag">Database Design</div>
                            <div class="skill-tag">API Development</div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 mb-4">
                    <div class="card h-100">
                        <div class="card-header">
                            <i class="fas fa-heartbeat me-2"></i>Biomedical Applications
                        </div>
                        <div class="card-body">
                            <div class="skill-tag">Gait Analysis</div>
                            <div class="skill-tag">Biomechanics</div>
                            <div class="skill-tag">Prosthetic Design</div>
                            <div class="skill-tag">Motion Capture</div>
                            <div class="skill-tag">Clinical Decision Support</div>
                            <div class="skill-tag">Healthcare AI</div>
                            <div class="skill-tag">Assistive Technology</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Patents Section -->
    <section id="patents" class="py-5">
        <div class="container">
            <h2 class="section-title text-center">Patents & Intellectual Property</h2>
            
            <div class="row">
                <div class="col-12">
                    <div class="patent-item">
                        <h4 class="publication-title">
                            <i class="fas fa-lightbulb me-2 text-warning"></i>
                            A Compact and Powered Ankle-Foot Prosthetic Device
                        </h4>
                        <p class="publication-journal">
                            <strong>Indian Patent Application No. 202431037184</strong> (Published & Under Examination)
                        </p>
                        <p><strong>Year:</strong> 2024 | <strong>Institution:</strong> IIT Kharagpur, India</p>
                        <ul class="mt-3">
                            <li>Developed a prosthetic device addressing limitations of conventional systems through real-time foot height and ankle angle adjustments</li>
                            <li>Integrated a spring-loaded split forefoot to enhance shock absorption and push-off dynamics during gait</li>
                            <li>Engineered a hybrid actuation system (active + passive) to improve stability and mobility for transtibial amputees</li>
                        </ul>
                    </div>

                    <div class="patent-item">
                        <h4 class="publication-title">
                            <i class="fas fa-copyright me-2 text-info"></i>
                            ProsthetiX-AI – Clinical Decision Support System for Ankle-Foot Prosthetic Recommendations
                        </h4>
                        <p class="publication-journal">
                            <strong>Indian Copyright Application No. 9678/2025-CO/SW</strong>
                        </p>
                        <p><strong>Year:</strong> 2025 | <strong>Institution:</strong> IIT Kharagpur, India</p>
                        <ul class="mt-3">
                            <li>Designed and implemented a copyright-registered clinical decision support tool for ankle-foot prosthetic prescriptions</li>
                            <li>Powered by LLMs, LangChain, and Streamlit; integrates explainable AI, K-level logic, and real-time academic citation justification for clinical use</li>
                        </ul>
                        <p class="mt-3">
                            <a href="#" onclick="alert('Patent documents will be available upon request')" class="btn btn-sm btn-outline-primary">
                                <i class="fas fa-file-pdf me-1"></i>View Patent Documents
                            </a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Publications Section -->
    <section id="publications" class="py-5 bg-light">
        <div class="container">
            <h2 class="section-title text-center">Selected Publications</h2>
            
            <div class="row">
                <div class="col-12">
                    <div class="publication-item">
                        <h5 class="publication-title">Wearable sensor‑based intent recognition for adaptive control of intelligent ankle‑foot prosthetics</h5>
                        <p class="publication-journal"><strong>Measurement: Sensors</strong>, Volume 39, 101865, Elsevier (2025)</p>
                        <ul>
                            <li>Developed an intent recognition system using wearable FSR and accelerometer data to classify gait speed and terrain inclination</li>
                            <li>Achieved <strong>96.3% accuracy</strong> using SBLSTM, outperforming CNN, KNN, and ANFIS in both accuracy and inference speed (25 ms)</li>
                        </ul>
                        <a href="https://www.sciencedirect.com/science/article/pii/S2665917425000595" target="_blank" class="btn btn-sm btn-outline-primary">
                            <i class="fas fa-external-link-alt me-1"></i>View Paper
                        </a>
                    </div>

                    <div class="publication-item">
                        <h5 class="publication-title">Biomechanical material selection for ankle‑foot prosthetics: An ensemble MCDM‑FEA framework</h5>
                        <p class="publication-journal"><strong>International Journal on Interactive Design and Manufacturing (IJIDeM)</strong> (2025)</p>
                        <ul>
                            <li>Developed a hybrid MCDM-FEA model to rank prosthetic materials based on mechanical strength, fatigue, and damping</li>
                        </ul>
                        <a href="https://link.springer.com/article/10.1007/s12008-025-02340-4" target="_blank" class="btn btn-sm btn-outline-primary">
                            <i class="fas fa-external-link-alt me-1"></i>View Paper
                        </a>
                    </div>

                    <div class="publication-item">
                        <h5 class="publication-title">Vision Transformer-based pose estimation for automated gait analysis in ankle-foot prosthetic design</h5>
                        <p class="publication-journal"><strong>IEEE 2nd International Conference on Advancement in Computation & Computer Technologies</strong> (2024)</p>
                        <ul>
                            <li>Benchmarked YOLOv8, DeepPose, and RTM Pose models for automated gait analysis</li>
                            <li>Achieved <strong>MAE = 19.75</strong>, <strong>R² = 99.5%</strong>, and <strong>107.7 ms inference time</strong> using RTM Pose</li>
                        </ul>
                        <a href="https://ieeexplore.ieee.org/document/10551002" target="_blank" class="btn btn-sm btn-outline-primary">
                            <i class="fas fa-external-link-alt me-1"></i>View Paper
                        </a>
                    </div>
                </div>
            </div>

            <div class="text-center mt-4">
                <p class="text-muted">
                    <strong>Total Publications:</strong> 30+ peer-reviewed articles | 
                    <a href="https://rb.gy/xh4gy" target="_blank" class="text-decoration-none">
                        <i class="fas fa-graduation-cap me-1"></i>View Complete List on Google Scholar
                    </a>
                </p>
            </div>
        </div>
    </section>


        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="py-5 bg-light">
        <div class="container">
            <h2 class="section-title text-center">Contact Me</h2>
            <div class="row">
                <div class="col-lg-6">
                    <div class="contact-form">
                        <h4 class="mb-4">Get In Touch</h4>
                        <form id="contact-form">
                            <div class="mb-3">
                                <label for="name" class="form-label">Name</label>
                                <input type="text" class="form-control" id="name" name="name" required>
                            </div>
                            <div class="mb-3">
                                <label for="email" class="form-label">Email</label>
                                <input type="email" class="form-control" id="email" name="email" required>
                            </div>
                            <div class="mb-3">
                                <label for="subject" class="form-label">Subject</label>
                                <input type="text" class="form-control" id="subject" name="subject" required>
                            </div>
                            <div class="mb-3">
                                <label for="message" class="form-label">Message</label>
                                <textarea class="form-control" id="message" name="message" rows="5" required></textarea>
                            </div>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-paper-plane me-2"></i>Send Message
                            </button>
                        </form>
                    </div>
                </div>
                <div class="col-lg-6">
                    <div class="contact-form">
                        <h4 class="mb-4">Contact Information</h4>
                        <div class="mb-4">
                            <h6><i class="fas fa-envelope me-2"></i>Email</h6>
                            <p>vidyapatikumar.me@gmail.com</p>
                        </div>
                        <div class="mb-4">
                            <h6><i class="fas fa-phone me-2"></i>Phone</h6>
                            <p>+91-8017847748</p>
                        </div>
                        <div class="mb-4">
                            <h6><i class="fas fa-map-marker-alt me-2"></i>Location</h6>
                            <p>IIT Kharagpur, West Bengal, India</p>
                        </div>
                        <div class="mb-4">
                            <h6><i class="fas fa-graduation-cap me-2"></i>Academic Profiles</h6>
                            <p>
                                <a href="https://rb.gy/xh4gy" target="_blank" class="me-3">
                                    <i class="fas fa-graduation-cap me-1"></i>Google Scholar
                                </a><br>
                                <a href="https://in.linkedin.com/in/vidyapati-kumar-37332251" target="_blank" class="me-3">
                                    <i class="fab fa-linkedin me-1"></i>LinkedIn
                                </a><br>
                                <a href="https://www.researchgate.net/profile/Vidyapati-Kumar" target="_blank">
                                    <i class="fab fa-researchgate me-1"></i>ResearchGate
                                </a>
                            </p>
                        </div>
                        <div class="text-center">
                            <a href="#" class="btn btn-outline-primary" onclick="alert('CV download will be available soon')">
                                <i class="fas fa-download me-2"></i>Download CV
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container text-center">
            <p>&copy; 2025 Vidyapati Kumar. All rights reserved.</p>
            <p>PhD Candidate in Mechanical Engineering | IIT Kharagpur</p>
            <div class="social-links mt-3">
                <a href="https://rb.gy/xh4gy" target="_blank">
                    <i class="fas fa-graduation-cap"></i>
                </a>
                <a href="https://in.linkedin.com/in/vidyapati-kumar-37332251" target="_blank">
                    <i class="fab fa-linkedin"></i>
                </a>
                <a href="https://www.researchgate.net/profile/Vidyapati-Kumar" target="_blank">
                    <i class="fab fa-researchgate"></i>
                </a>
                <a href="mailto:vidyapatikumar.me@gmail.com">
                    <i class="fas fa-envelope"></i>
                </a>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {{ javascript|safe }}
</body>
</html>
"""

def get_profile_image_base64():
    """Convert the uploaded profile image to base64 for embedding in HTML"""
    try:
        with open("mypic/VK.png", "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logging.error(f"Error processing profile image: {e}")
        # Return a professional placeholder SVG
        placeholder_svg = """<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="100" fill="#3498db"/>
            <circle cx="100" cy="80" r="30" fill="white"/>
            <ellipse cx="100" cy="160" rx="50" ry="35" fill="white"/>
        </svg>"""
        return base64.b64encode(placeholder_svg.encode()).decode('utf-8')

@app.route('/')
def index():
    """Main page route"""
    profile_image = get_profile_image_base64()
    
    return render_template_string(
        HTML_TEMPLATE,
        title="Vidyapati Kumar - PhD Candidate | AI & Biomechatronics",
        css_styles=CSS_STYLES,
        javascript=JAVASCRIPT,
        profile_image=profile_image
    )

@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submissions and send email"""
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        # Send email
        msg = Message(subject=f"New Contact Form: {subject}",
                      recipients=["vidyapatikumar.me@gmail.com"])
        msg.body = f"""
        Name: {name}
        Email: {email}
        Subject: {subject}
        Message:
        {message}
        """
        mail.send(msg)

        return jsonify({'success': True, 'message': 'Thank you for your message! I will get back to you soon.'})
    except Exception as e:
        logging.error(f"Error processing contact form: {e}")
        return jsonify({'success': False, 'error': 'Failed to send message'}), 500


@app.route('/cv')
def download_cv():
    """Route for CV download (placeholder)"""
    # In a real application, you would serve the actual CV file
    return "CV download functionality will be implemented with actual CV file", 404

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return "Page not found", 404

@app.errorhandler(500)
def server_error(error):
    """Handle server errors"""
    logging.error(f"Server error: {error}")
    return "Internal server error", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
