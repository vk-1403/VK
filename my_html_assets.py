import base64
import logging

# -------------------------------
# Encode profile image or fallback
# -------------------------------
def get_profile_image_base64():
    """Load and encode the profile image from static folder"""
    try:
        with open("static/mypic/VK.png", "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logging.error(f"Error loading profile image: {e}")
        # Fallback placeholder SVG
        placeholder_svg = """
        <svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="100" fill="#18bc9c"/>
            <text x="50%" y="55%" font-size="50" text-anchor="middle" fill="#fff">VK</text>
        </svg>
        """
        return base64.b64encode(placeholder_svg.encode()).decode('utf-8')

# -------------------------------
# 🌟 Modern Aesthetic CSS
# -------------------------------
CSS_STYLES = """
<style>
    :root {
        --primary: #2c3e50;
        --accent: #18bc9c;
        --background: #f5f7fa;
        --text: #34495e;
        --muted: #7f8c8d;
        --white: #fff;
        --shadow: rgba(0,0,0,0.1);
    }

    body {
        font-family: 'Poppins', sans-serif;
        background-color: var(--background);
        color: var(--text);
        line-height: 1.6;
    }

    .navbar {
        background: linear-gradient(135deg, var(--primary), var(--accent));
        box-shadow: 0 4px 10px var(--shadow);
    }

    .navbar-brand {
        font-weight: bold;
        font-size: 1.5rem;
        color: var(--white) !important;
    }

    .navbar-nav .nav-link {
        color: var(--white) !important;
        margin: 0 10px;
        transition: 0.3s;
    }

    .navbar-nav .nav-link:hover {
        color: var(--accent) !important;
    }

    .hero-section {
        background: linear-gradient(135deg, var(--accent), var(--primary));
        color: var(--white);
        text-align: center;
        padding: 100px 20px;
    }

    .profile-photo {
        width: 180px;
        height: 180px;
        border-radius: 50%;
        border: 4px solid var(--white);
        box-shadow: 0 8px 25px var(--shadow);
        object-fit: cover;
        margin-bottom: 20px;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 20px;
    }

    .btn-download {
        background: var(--primary);
        color: var(--white);
        padding: 10px 25px;
        border-radius: 30px;
        text-transform: uppercase;
        font-weight: 600;
        transition: 0.3s;
        text-decoration: none;
    }

    .btn-download:hover {
        background: var(--accent);
        color: var(--white);
        text-decoration: none;
    }

    .section-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 40px;
        text-align: center;
        position: relative;
    }

    .section-title::after {
        content: '';
        width: 80px;
        height: 4px;
        background: var(--accent);
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
    }

    .card {
        background: var(--white);
        border-radius: 15px;
        box-shadow: 0 6px 20px var(--shadow);
        padding: 20px;
        margin-bottom: 30px;
        transition: 0.3s;
    }

    .card:hover {
        transform: translateY(-5px);
    }

    .publication-category {
        background: var(--accent);
        color: var(--white);
        padding: 8px 15px;
        border-radius: 50px;
        display: inline-block;
        margin-bottom: 10px;
        font-weight: 500;
    }

    .contact-form {
        background: var(--white);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 6px 20px var(--shadow);
    }

    .form-control, .btn-submit {
        border-radius: 30px;
    }

    .btn-submit {
        background: var(--accent);
        color: var(--white);
        font-weight: 600;
        transition: 0.3s;
    }

    .btn-submit:hover {
        background: var(--primary);
    }

    .cv-section {
        margin-top: 50px;
    }

    .cv-subsection {
        margin-bottom: 30px;
    }

    .cv-subsection h3 {
        color: var(--primary);
        margin-bottom: 20px;
        font-weight: 600;
    }
</style>
"""

# -------------------------------
# ⚡ JavaScript for Contact Form
# -------------------------------
JAVASCRIPT = """
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('contact-form');
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                const formData = new FormData(this);
                const jsonData = Object.fromEntries(formData);

                fetch('/contact', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(jsonData)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Thank you! Your message has been sent.');
                        form.reset();
                    } else {
                        alert('Error sending message. Try again later.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error sending message. Try again later.');
                });
            });
        }
    });
</script>
"""

# -------------------------------
# 📄 Full Academic HTML Template
# -------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    {{ css_styles|safe }}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="#home">Vidyapati Kumar</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="#about">About</a></li>
                    <li class="nav-item"><a class="nav-link" href="#cv">CV</a></li>
                    <li class="nav-item"><a class="nav-link" href="#contact">Contact</a></li>
                    <li class="nav-item"><a class="btn-download ms-3" href="/cv" target="_blank">Download CV</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <section id="home" class="hero-section">
        <div class="container">
            <img src="data:image/jpeg;base64,{{ profile_image }}" alt="Profile" class="profile-photo">
            <h1 class="hero-title">Vidyapati Kumar</h1>
            <p class="hero-subtitle">PhD Candidate | AI-Driven Biomechatronics & Prosthetics</p>
        </div>
    </section>

    <section id="about" class="py-5">
        <div class="container">
            <h2 class="section-title">About Me</h2>
            <p class="lead">Ph.D. candidate in Mechanical Engineering at IIT Kharagpur, specializing in AI-driven biomechatronic systems, advanced manufacturing, and multi-objective optimization. My research integrates machine learning, sensor fusion, and embedded systems for intelligent prosthetics, wearable health technologies, and process optimization. I have published peer-reviewed journal articles, contributed to edited books, and hold a patent and software copyright. With interdisciplinary expertise spanning biomedical engineering, robotics, and smart manufacturing, I aim to contribute to cutting-edge research in AI-enabled systems and real-world healthcare innovations through a postdoctoral position.</p>
        </div>
    </section>

    <section id="cv" class="py-5 cv-section">
        <div class="container">
            <h2 class="section-title">Curriculum Vitae</h2>
            <div class="cv-subsection">
                <h3>Education</h3>
                <ul class="list-group">
                    <li class="list-group-item">Ph.D. (Mechanical Engineering), IIT Kharagpur, India – Dec 2025 (Expected) – CGPA: 8.5/10</li>
                    <li class="list-group-item">M.E. (Production Engineering), Jadavpur University, India – 2018 – CGPA: 8.38/10</li>
                    <li class="list-group-item">B.Tech (Mechanical Engineering), MAKAUT, India – 2016 – CGPA: 9.19/10</li>
                </ul>
            </div>
            
            <div class="cv-subsection">
                <h3>Experience</h3>
                <p>Senior Research Fellow – AI-Enhanced Powered Ankle-Foot Prosthetic System (Jul. 2021 – Present, IIT Kharagpur)</p>
                <p>Project Mentor – TIH Foundation for IoT and IoE (Feb. 2024 – Present, IIT Bombay & DST)</p>
                <p>Teaching Assistant – NPTEL Courses (Jan. 2021 – Present, IIT Kharagpur)</p>
                <p>Faculty – GATE (Mechanical) (Aug. 2020 – Dec. 2020, Unacademy)</p>
            </div>

            <div class="cv-subsection">
                <h3>Selected Publications & Patents</h3>
                {% for theme, papers in publications.items() %}
                <h5>{{ theme }}</h5>
                <ul>
                    {% for pub in papers %}
                    <li><strong>{{ pub.title }}</strong> – {{ pub.journal }} (<a href="{{ pub.link }}" target="_blank">Link</a>)</li>
                    {% endfor %}
                </ul>
                {% endfor %}
            </div>

            <div class="cv-subsection">
                <h3>Books & Chapters</h3>
                <p>See full list in CV or <a href="/cv" target="_blank">Download CV</a></p>
            </div>

            <div class="cv-subsection">
                <h3>Technical Skills</h3>
                <p>Python, MATLAB, Embedded Systems, AI/ML (PyTorch, TensorFlow), FEA, Computer Vision, IoT Devices</p>
            </div>

            <div class="cv-subsection">
                <h3>Awards & Certifications</h3>
                <p>RAAIBA-2022 Workshop, GATE Fellowship (2016–2018), Stanford ML (Coursera)</p>
            </div>
        </div>
    </section>

    <section id="contact" class="py-5">
        <div class="container">
            <h2 class="section-title">Contact Me</h2>
            <div class="row">
                <div class="col-lg-6 mx-auto">
                    <div class="contact-form">
                        <form id="contact-form">
                            <div class="mb-3">
                                <input type="text" name="name" class="form-control" placeholder="Your Name" required>
                            </div>
                            <div class="mb-3">
                                <input type="email" name="email" class="form-control" placeholder="Your Email" required>
                            </div>
                            <div class="mb-3">
                                <textarea name="message" rows="5" class="form-control" placeholder="Your Message" required></textarea>
                            </div>
                            <button type="submit" class="btn btn-submit w-100">Send Message</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <footer class="py-4 text-center">
        <p>&copy; 2025 Vidyapati Kumar. All Rights Reserved.</p>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {{ javascript|safe }}
</body>
</html>
"""
