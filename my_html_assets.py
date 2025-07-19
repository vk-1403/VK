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

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
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
</style>
"""

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
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(jsonData)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Thank you for your message! I will contact you soon.');
                        form.reset();
                    } else {
                        alert('Error sending message. Please try again later.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error sending message. Please try again later.');
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
                    <li class="nav-item"><a class="nav-link" href="#publications">Publications</a></li>
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
            <div class="mt-3">
                <a href="mailto:vidyapatikumar.me@gmail.com" class="btn-download">Contact Me</a>
            </div>
        </div>
    </section>

    <section id="research" class="py-5">
        <div class="container">
            <h2 class="section-title">Research Interests</h2>
            <div class="row text-center">
                <div class="col-md-4">
                    <div class="card">
                        <h5>AI in Healthcare</h5>
                        <p>Explainable AI models for prosthetic control & medical decision systems.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card">
                        <h5>Biomechatronics</h5>
                        <p>Intelligent prosthetic limbs, wearable sensors, and real-time embedded systems.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card">
                        <h5>IoT for Assistive Tech</h5>
                        <p>ESP32 & Raspberry Pi systems for patient-centric healthcare IoT devices.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="publications" class="py-5 bg-light">
        <div class="container">
            <h2 class="section-title">Publications</h2>
            {% for theme, papers in publications.items() %}
            <div class="mb-4">
                <span class="publication-category">{{ theme }}</span>
                {% for pub in papers %}
                <div class="card mt-3">
                    <h5>{{ pub.title }}</h5>
                    <p class="mb-1"><strong>{{ pub.journal }}</strong> ({{ pub.year }})</p>
                    <a href="{{ pub.link }}" target="_blank" class="btn btn-sm btn-outline-primary mt-2">
                        <i class="fas fa-external-link-alt"></i> View Paper
                    </a>
                </div>
                {% endfor %}
            </div>
            {% endfor %}
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
