CSS_STYLES = """
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Playfair+Display:wght@700&display=swap');

    :root {
        --primary-color: #2C3E50;
        --secondary-color: #18BC9C;
        --accent-color: #3498DB;
        --background-light: #F8F9FA;
        --text-dark: #2C3E50;
        --text-light: #7F8C8D;
        --white: #FFFFFF;
    }

    body {
        font-family: 'Roboto', sans-serif;
        background-color: var(--background-light);
        color: var(--text-dark);
        margin: 0;
        padding: 0;
        line-height: 1.6;
    }

    .navbar {
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .navbar-brand {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        color: var(--white) !important;
    }

    .navbar-nav .nav-link {
        color: var(--white) !important;
        margin: 0 10px;
        font-weight: 500;
        transition: color 0.3s ease;
    }

    .navbar-nav .nav-link:hover {
        color: var(--secondary-color) !important;
    }

    .hero-section {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: var(--white);
        text-align: center;
        padding: 100px 20px;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 1.4rem;
        margin-bottom: 20px;
        font-weight: 400;
    }

    .profile-photo {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        border: 5px solid var(--white);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        object-fit: cover;
        margin-bottom: 20px;
    }

    .section-title {
        font-family: 'Playfair Display', serif;
        text-align: center;
        color: var(--primary-color);
        font-size: 2.5rem;
        margin-bottom: 40px;
        position: relative;
    }

    .section-title::after {
        content: "";
        width: 80px;
        height: 4px;
        background: var(--accent-color);
        display: block;
        margin: 10px auto 0;
        border-radius: 2px;
    }

    .card {
        background: var(--white);
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
        padding: 20px;
        margin-bottom: 30px;
    }

    .card:hover {
        transform: translateY(-5px);
    }

    .contact-form {
        background: var(--white);
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
    }

    .btn-primary {
        background: var(--accent-color);
        border: none;
        color: var(--white);
        font-weight: 600;
        padding: 10px 25px;
        border-radius: 25px;
        transition: background 0.3s ease;
    }

    .btn-primary:hover {
        background: var(--secondary-color);
    }

    .footer {
        background: var(--primary-color);
        color: var(--white);
        text-align: center;
        padding: 40px 0;
    }

    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.2rem;
        }
        .hero-subtitle {
            font-size: 1.2rem;
        }
    }
</style>
"""

JAVASCRIPT = """
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Smooth scrolling
        const links = document.querySelectorAll('a[href^="#"]');
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                target.scrollIntoView({ behavior: 'smooth' });
            });
        });

        // Contact form
        const form = document.getElementById('contact-form');
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                fetch('/contact', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(Object.fromEntries(new FormData(form)))
                }).then(r => r.json()).then(data => {
                    alert(data.success ? 'Message sent successfully!' : 'Failed to send message.');
                    if(data.success) form.reset();
                });
            });
        }
    });
</script>
"""

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
                    <li class="nav-item"><a class="nav-link" href="#research">Research</a></li>
                    <li class="nav-item"><a class="nav-link" href="#skills">Skills</a></li>
                    <li class="nav-item"><a class="nav-link" href="#publications">Publications</a></li>
                    <li class="nav-item"><a class="nav-link" href="#contact">Contact</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <section id="home" class="hero-section">
        <div class="container">
            <img src="data:image/jpeg;base64,{{ profile_image }}" alt="Profile" class="profile-photo">
            <h1 class="hero-title">Vidyapati Kumar</h1>
            <p class="hero-subtitle">PhD Candidate | AI & Biomechatronics</p>
        </div>
    </section>

    <section id="about" class="py-5">
        <div class="container">
            <h2 class="section-title">About Me</h2>
            <div class="card">
                <p>I am a PhD candidate in Mechanical Engineering at IIT Kharagpur, specializing in AI-driven biomechatronic systems, prosthetics, and medical AI. My work integrates sensor fusion (EMG, IMU, FSR), embedded platforms, and ML for healthcare applications.</p>
            </div>
        </div>
    </section>

    <section id="research" class="py-5 bg-light">
        <div class="container">
            <h2 class="section-title">Research Interests</h2>
            <div class="row">
                <div class="col-md-6">
                    <div class="card">AI in Prosthetics, Biomechatronics, and Wearable Health Technologies.</div>
                </div>
                <div class="col-md-6">
                    <div class="card">Explainable AI (SHAP, LIME), FEA, and Optimization in Biomedical Devices.</div>
                </div>
            </div>
        </div>
    </section>

    <section id="skills" class="py-5">
        <div class="container">
            <h2 class="section-title">Skills</h2>
            <div class="row">
                <div class="col-md-4"><div class="card">Python, MATLAB, Embedded Systems</div></div>
                <div class="col-md-4"><div class="card">TensorFlow, PyTorch, OpenCV</div></div>
                <div class="col-md-4"><div class="card">Sensor Fusion, Prosthetic Design, IoT</div></div>
            </div>
        </div>
    </section>

    <section id="publications" class="py-5 bg-light">
        <div class="container">
            <h2 class="section-title">Selected Publications</h2>
            <div class="card">
                <p>1. Wearable sensor‑based intent recognition for prosthetics - Measurement: Sensors (Elsevier)</p>
                <p>2. Biomechanical material selection for prosthetics - IJIDeM (Springer)</p>
                <p>3. Vision Transformer-based gait analysis - IEEE Conference</p>
            </div>
        </div>
    </section>

    <section id="contact" class="py-5">
        <div class="container">
            <h2 class="section-title">Contact Me</h2>
            <div class="contact-form">
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
                    <button type="submit" class="btn btn-primary">Send Message</button>
                </form>
            </div>
        </div>
    </section>

    <footer class="footer">
        <p>&copy; 2025 Vidyapati Kumar | IIT Kharagpur</p>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {{ javascript|safe }}
</body>
</html>
"""
