# my_html_assets.py

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
</style>
"""

JAVASCRIPT = """
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const navLinks = document.querySelectorAll('a[href^="#"]');
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
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
    {{ css_styles|safe }}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
        <div class="container">
            <a class="navbar-brand" href="#home">Vidyapati Kumar</a>
        </div>
    </nav>
    <section id="home" class="hero-section">
        <div class="container text-center">
            <img src="data:image/jpeg;base64,{{ profile_image }}" alt="Vidyapati Kumar" class="profile-photo">
            <h1 class="hero-title">Vidyapati Kumar</h1>
            <p class="hero-subtitle">PhD Candidate | IIT Kharagpur</p>
        </div>
    </section>
    <section id="publications" class="py-5 bg-light">
        <div class="container">
            <h2 class="section-title text-center">Selected Publications</h2>
            {% for pub in publications %}
            <div class="publication-item">
                <h5 class="publication-title">{{ pub['bib']['title'] }}</h5>
                <p class="publication-journal">{{ pub['bib']['venue'] }} ({{ pub['bib']['pub_year'] }})</p>
                <p>Citations: {{ pub['num_citations'] }}</p>
                <a href="{{ pub['pub_url'] }}" target="_blank" class="btn btn-sm btn-outline-primary">View Paper</a>
            </div>
            {% endfor %}
            <div class="text-center mt-4">
                <a href="https://scholar.google.com/citations?user=thYJjvAAAAAJ&hl=en" target="_blank" class="btn btn-primary">View Full List on Google Scholar</a>
            </div>
        </div>
    </section>
    {{ javascript|safe }}
</body>
</html>
"""
