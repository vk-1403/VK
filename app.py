# app.py — VK personal site (drop‑in upgrade)
# -------------------------------------------------
# Highlights
# - Adds rich "Publications" with sub‑tabs (Journals / Conferences / Book Chapters)
# - Adds "Books & Editorial" grid with cover images + links
# - Adds Awards, Teaching, Mentoring, Talks sections (easy to edit in DATA below)
# - CV download endpoint serving /static/cv/Vidyapati_Kumar_CV.pdf if present
# - Safer email config (env vars), honeypot anti‑spam field
# - JSON‑LD schema.org for better Google Scholar/SEO
# - All content is editable in the DATA section
# - Single‑file Flask app; no templates directory required

import os
import json
import base64
import logging
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, send_file
from flask_mail import Mail, Message

# ------------------------------
# App + Mail setup
# ------------------------------
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-change-me")

app.config.update(
    MAIL_SERVER=os.environ.get("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_PORT=int(os.environ.get("MAIL_PORT", 587)),
    MAIL_USE_TLS=os.environ.get("MAIL_USE_TLS", "true").lower() == "true",
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME", "vidyapatikumar.me@gmail.com"),
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD") or os.environ.get("GMAIL_APP_PASSWORD"),
    MAIL_DEFAULT_SENDER=os.environ.get("MAIL_DEFAULT_SENDER", "vidyapatikumar.me@gmail.com"),
)
mail = Mail(app)
logging.basicConfig(level=logging.INFO)

# ------------------------------
# Helpers
# ------------------------------

def b64_image(path: str) -> str:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        logging.warning(f"Image not found {path}: {e}")
        # Nice placeholder avatar SVG
        svg = (
            "<svg width='200' height='200' xmlns='http://www.w3.org/2000/svg'>"
            "<defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>"
            "<stop offset='0%' stop-color='#2c3e50'/><stop offset='100%' stop-color='#3498db'/>"
            "</linearGradient></defs>"
            "<rect width='100%' height='100%' fill='url(#g)'/>"
            "<circle cx='100' cy='80' r='35' fill='white'/>"
            "<ellipse cx='100' cy='150' rx='55' ry='40' fill='white'/>"
            "</svg>"
        )
        return base64.b64encode(svg.encode()).decode("utf-8")

PROFILE_IMG_B64 = b64_image("static/mypic/VK.png")

# ------------------------------
# ====== DATA (edit freely) =====
# ------------------------------

BIO = {
    "full_name": "Vidyapati Kumar",
    "tagline": "PhD Scholar • AI & Biomechatronics",
    "affiliation": "IIT Kharagpur, India",
    "email": "vidyapatikumar.me@gmail.com",
    "phone": "+91-8017847748",
    "location": "Kharagpur, India",
    "status": "Seeking Postdoctoral Opportunities",
    "cgpa": "8.5/10",
    "scholar_url": "https://rb.gy/xh4gy",
    "linkedin": "https://in.linkedin.com/in/vidyapati-kumar-37332251",
    "rg": "https://www.researchgate.net/profile/Vidyapati-Kumar",
}

EDUCATION = [
    {"year": "Dec 2025 (Expected)", "degree": "Ph.D. (Mechanical Engineering)", "inst": "IIT Kharagpur, India", "cgpa": "8.5/10"},
    {"year": "2018", "degree": "M.E. (Production Engineering)", "inst": "Jadavpur University, India", "cgpa": "8.38/10"},
    {"year": "2016", "degree": "B.Tech (Mechanical Engineering)", "inst": "MAKAUT, India", "cgpa": "9.19/10"},
]

EXPERIENCE = [
    {
        "role": "Senior Research Fellow — AI-Enhanced Powered Ankle-Foot Prosthetic System",
        "org": "Indian Institute of Technology Kharagpur",
        "date": "Jul 2021 – Present",
        "bullets": [
            "Embedded IoT & sensor fusion (ESP32, Raspberry Pi); terrain classification via LiDAR + IMU",
            "Multimodal gait control using 16-channel FSR insoles, IMUs and Maxon motors",
            "ML pipelines with SHAP explainability; >90% gait-phase accuracy",
            "Vision-based gait analysis (ViTs, YOLOv8, OpenPose, GEI); 96%+ accuracy on disorders",
            "Material selection + FEA in COMSOL for structural validation",
            "LLM-driven clinical decision support (CDS ProsthetiX; LangChain + Streamlit)",
            "Extensive sensor trials across terrains; reliability under varying loads",
        ],
    },
    {
        "role": "Project Mentor — Chanakya Fellowship",
        "org": "TIH Foundation for IoT & IoE (IIT Bombay) / DST, GoI",
        "date": "Feb 2024 – Present",
        "bullets": [
            "Mentored DST-funded end-to-end IoT prosthetic stack: embedded systems, real-time acquisition, control, and cloud",
            "Coordinated cross-functional teams; milestones, budgets, and translational impact",
        ],
    },
    {
        "role": "Teaching Assistant — NPTEL Courses",
        "org": "IIT Kharagpur",
        "date": "Jan 2021 – Present",
        "bullets": [
            "With Prof. D. K. Pratihar: Robotics, Fuzzy Logic, Optimization Tools",
            "Developed Python / MATLAB demos; student mentoring",
        ],
    },
    {
        "role": "Faculty — GATE (Mechanical)",
        "org": "Unacademy (EdTech)",
        "date": "Aug 2020 – Dec 2020",
        "bullets": [
            "Taught Manufacturing, Strength of Materials, Thermodynamics, Engineering Mathematics",
            "Delivered problem-solving sessions & mock tests for GATE aspirants",
        ],
    },
    {
        "role": "Project Assistant — Design Guidelines for Underground Coal Extraction",
        "org": "CSIR-CIMFR",
        "date": "Aug 2018 – Mar 2020",
        "bullets": [
            "Created CAD models + numerical simulations for deep seams (300m+)",
            "Processed geo-mining data for MATLAB optimization to improve mine safety",
        ],
    },
    {
        "role": "M.E. Thesis — Intelligent Advisory System for NTM Processes",
        "org": "Jadavpur University",
        "date": "Aug 2016 – Mar 2018",
        "bullets": [
            "Developed VBASIC expert system recommending optimal NTM parameters",
            "Validated system on multiple real-world case scenarios",
        ],
    },
    {
        "role": "B.Tech Thesis — Assistive System for Visually Impaired",
        "org": "MAKAUT",
        "date": "Aug 2015 – Mar 2016",
        "bullets": [
            "Arduino-based navigation system with ultrasonic + PIR sensors",
            "Integrated into wearable shoe, belt, and cap for obstacle detection",
        ],
    },
]

AWARDS = [
    "Chanakya Fellowship (DST/TIH-IoT), 2024–present",
    "Karyashala: RAAIBA-2022 (SERB/DST) — 7-day high-end workshop on AI for Biomedical Applications",
    "Institute Assistantship (MHRD) — PhD Research Scholar, IIT Kharagpur (2021–present)",
    "GATE Fellowship — Jadavpur University (2016–2018)",
    "Best Paper/Presentation — (add details)",
]


TALKS = [
    {"title": "Vision Transformers for Automated Gait Analysis", "venue": "InCACCT 2024", "link": "https://ieeexplore.ieee.org/document/10551002"},
]

PATENTS = [
    {
        "title": "A Compact and Powered Ankle‑Foot Prosthetic Device",
        "meta": "Indian Patent Application No. 202431037184 (Published & Under Examination)",
        "year": "2024",
        "inst": "IIT Kharagpur",
        "bullets": [
            "Real‑time foot height & ankle angle adjustments",
            "Spring‑loaded split forefoot for shock absorption & push‑off",
            "Hybrid actuation (active + passive) for stability and mobility",
        ],
        "link": "https://drive.google.com/drive/u/7/folders/1AYkEL0NrkHq8G8woTFXXk5bVwJaTIVLk"
    },
    {
        "title": "ProsthetiX‑AI — Clinical Decision Support for Ankle‑Foot Prosthetics",
        "meta": "Indian Copyright Application No. 9678/2025-CO/SW",
        "year": "2025",
        "inst": "IIT Kharagpur",
        "bullets": [
            "LLM + LangChain + Streamlit with explainable AI & K‑level logic",
            "Real‑time citation justification for clinical use",
        ],
        "link": "https://drive.google.com/drive/u/7/folders/1AYkEL0NrkHq8G8woTFXXk5bVwJaTIVLk"
    },
]

PUBLICATIONS = {
    "journals": [
        {"title": "Wearable sensor‑based intent recognition for adaptive control of intelligent ankle‑foot prosthetics", "venue": "Measurement: Sensors, 39, 101865 (Elsevier)", "year": 2025, "authors": "V. Kumar; D. K. Pratihar", "link": "https://www.sciencedirect.com/science/article/pii/S2665917425000595", "notes": "FSR + accelerometer; SBLSTM 96.3% acc.; 25 ms"},
        {"title": "Biomechanical material selection for ankle‑foot prosthetics: An ensemble MCDM‑FEA framework", "venue": "International Journal on Interactive Design and Manufacturing (Springer)", "year": 2025, "authors": "V. Kumar; D. K. Pratihar", "link": "https://link.springer.com/article/10.1007/s12008-025-02340-4"},
        {"title": "Mechatronic and AI‑driven framework for non‑invasive screening of knee abnormalities using multimodal sensors", "venue": "Computer Methods in Biomechanics and Biomedical Engineering", "year": 2024, "authors": "V. Kumar; M. V. Hrishikesh; M. Shijas; D. K. Pratihar", "link": "", "notes": "Accepted"},
        {"title": "Fuzzy logic‑based synchronization of trajectory planning and obstacle avoidance for RRP SCARA robot", "venue": "IJIDeM", "year": 2025, "authors": "V. Kumar; A. Mistri", "link": "https://link.springer.com/article/10.1007/s12008-024-02214-1"},
        {"title": "A SWARA‑CoCoSo‑based approach for spray painting robot selection", "venue": "Informatica 33(1) 35–54", "year": 2022, "authors": "V. Kumar; K. Kalita; P. Chatterjee; E. K. Zavadskas; S. Chakraborty", "link": "https://informatica.vu.lt/journal/INFORMATICA/article/1237/info"},
        {"title": "Teaching‑learning‑based parametric optimization of EDM", "venue": "Facta Universitatis: Mechanical Engineering 18(2) 281–300", "year": 2020, "authors": "V. Kumar; S. Diyaley; S. Chakraborty", "link": "https://casopisi.junis.ni.ac.rs/index.php/FUMechEng/article/view/6156/0"},
        {"title": "Grey‑fuzzy method‑based parametric analysis of AWJM on GFRP", "venue": "Sādhanā 45(1) 1–18", "year": 2020, "authors": "V. Kumar; P. P. Das; S. Chakraborty", "link": "https://link.springer.com/article/10.1007/s12046-020-01355-9"},
        {"title": "Machine learning prediction of erosion resistance of laser‑clad coatings", "venue": "Journal of Micromanufacturing", "year": 2025, "authors": "I. Mandal; V. Kumar; P. Saha", "link": "https://journals.sagepub.com/doi/full/10.1177/25165984251317028"},
        {"title": "Optimizing healthcare in the digital era: Fusion of IoT with other techniques", "venue": "EAI Endorsed Transactions on Internet of Things, 11", "year": 2025, "authors": "R. Singh; A. Chaudhary; V. Kumar", "link": "https://publications.eai.eu/index.php/IoT/article/view/6077"},
        {"title": "Heat checking as a failure mechanism of dies exposed to thermal cycles: A review", "venue": "Journal of Materials Research and Technology 26", "year": 2023, "authors": "P. Solgi; M. Chenarani; A. R. Eivani; M. Ghosh; V. Kumar; H. R. Jafarian", "link": "https://www.sciencedirect.com/science/article/pii/S223878542301699X"},
        {"title": "Experimental investigation and optimization of EDM parameters using grey‑fuzzy hybrids", "venue": "Materials 14(19)", "year": 2021, "authors": "A. Sharma; V. Kumar; et al.", "link": "https://www.mdpi.com/1996-1944/14/19/5820"},
        {"title": "Functionally graded adherents on failure of FRP socket joints", "venue": "Materials 14(21)", "year": 2021, "authors": "C. Prakash; V. Kumar; et al.", "link": "https://www.mdpi.com/1996-1944/14/21/6365"},
        {"title": "Intelligent decision model for NTM processes", "venue": "DMAME 4(1) 194–214", "year": 2021, "authors": "S. Chakraborty; V. Kumar", "link": "https://dmame-journal.org/index.php/dmame/article/view/154"},
        {"title": "All‑time best World XI Test cricket team using TOPSIS", "venue": "Decision Science Letters 8(1) 95–108", "year": 2018, "authors": "S. Chakraborty; V. Kumar; K. R. Ramakrishnan", "link": "https://growingscience.com/beta/dsl/2817-selection-of-the-all-time-best-world-xi-test-cricket-team-using-the-topsis-method.html"},
        {"title": "Grey fuzzy logic approach for cotton fibre selection", "venue": "IEI Series E 98(1) 1–9", "year": 2017, "authors": "S. Chakraborty; P. P. Das; V. Kumar", "link": "https://link.springer.com/article/10.1007/s40034-017-0099-7"}
    ],
    "conferences": [
        {"title": "Vision Transformer‑based pose estimation for automated gait analysis in ankle‑foot prosthetic design", "venue": "IEEE InCACCT 2024", "year": 2024, "authors": "V. Kumar; D. K. Pratihar", "link": "https://ieeexplore.ieee.org/document/10551002", "notes": "RTM Pose: MAE 19.75; R² 99.5%; 107.7 ms"},
        {"title": "Terrain recognition for intelligent powered ankle‑foot prosthetics using sEMG and ensemble learning", "venue": "IEEE INDICON 2024", "year": 2024, "authors": "V. Kumar; M. V. Hrishikesh; M. Shijas; D. K. Pratihar", "link": "https://ieeexplore.ieee.org/document/10958532?reason=concurrency", "notes": "Extra Trees 87% acc; F1=0.88"}
    ],
    "book_chapters": [
        {"title": "Comparative evaluation of deep learning techniques for multistage Alzheimer’s prediction from MRI", "venue": "in Biomedical Robots and Devices in Healthcare (Elsevier)", "year": 2025, "authors": "P. Gupta; P. Nahak; V. Kumar; D. K. Pratihar; K. Deb", "link": "https://www.sciencedirect.com/science/article/pii/B9780443222061000073"},
        {"title": "Advancing ankle–foot orthosis design through biomechanics, robotics, and additive manufacturing: A review", "venue": "in Biomedical Robots and Devices in Healthcare (    ],
    "book_chapters": [
        # {"title": "Chapter Title", "venue": "Book / Publisher", "year": 2023, "authors": "...", "link": "https://..."},
    ],
}

BOOKS = [
{
"title": "Biomedical Robots and Devices in Healthcare: Opportunities and Challenges for Future Applications",
"authors": "Iqbal, F., Gupta, P., Kumar, V., Pratihar, D. K.",
"year": "2024",
"publisher": "Elsevier Science & Technology",
"link": "https://www.sciencedirect.com/book/9780443222061/biomedical-robots-and-devices-in-healthcare",
"cover": "static/mypic/book1.jpg",
},
{
"title": "Advancing Healthcare Through Decision Intelligence: Machine Learning, Robotics, and Analytics in Biomedical Informatics",
"authors": "Dey, S., Kumar, V., Pratihar, D. K., Singh, V. P., Islam, S. M. N.",
"year": "2025",
"publisher": "Academic Press (Elsevier)",
"link": "https://www.sciencedirect.com/book/9780443264801/advancing-healthcare-through-decision-intelligence",
"cover": "static/mypic/book2.jpg",
},
{
"title": "Quantum Computing, Cyber Security and Cryptography",
"authors": "Goyal, S. B., Kumar, V., Islam, S. M. N., Ghai, D.",
"year": "2025",
"publisher": "Springer",
"link": "https://link.springer.com/book/10.1007/978-981-96-4948-8",
"cover": "static/mypic/book3.jpg",
},
]
SKILLS = {
    "ML/AI": ["Python", "TensorFlow", "PyTorch", "Scikit‑learn", "Pandas", "NumPy", "SHAP", "XGBoost", "SBLSTM"],
    "Vision": ["Vision Transformers", "YOLOv8", "RTM Pose", "OpenCV", "Grad‑CAM", "GEI"],
    "Embedded/IoT": ["ESP32", "Raspberry Pi", "Arduino", "IMU", "LiDAR", "FSR", "sEMG"],
    "Engg/Sim": ["MATLAB", "COMSOL", "FEA", "OpenSim", "CAD", "Optimization"],
    "Software": ["LangChain", "Streamlit", "Flask", "Git", "APIs", "DB design"],
    "Biomedical": ["Gait analysis", "Biomechanics", "Prosthetics", "CDSS", "Assistive Tech"],
}

# ------------------------------
# HTML (Jinja‑in‑string)
# ------------------------------

CSS = """
<style>
:root{--primary:#2c3e50;--accent:#3498db;--light:#ecf0f1;--text:#2c3e50;--muted:#7f8c8d}
*{box-sizing:border-box}body{font-family:Segoe UI,Tahoma,Arial,sans-serif;background:#f7f9fb;color:var(--text)}
.navbar{background:linear-gradient(135deg,var(--primary),var(--accent));box-shadow:0 2px 8px rgba(0,0,0,.1)}
.navbar a{color:#fff!important}
.hero{padding:90px 0;background:linear-gradient(135deg,var(--primary),var(--accent));color:#fff;text-align:center}
.hero img{width:200px;height:200px;border-radius:50%;border:5px solid #fff;object-fit:cover;box-shadow:0 8px 30px rgba(0,0,0,.25)}
.section{padding:64px 0}
.section-title{font-size:2rem;font-weight:800;text-align:center;margin:0 0 28px;position:relative}
.section-title:after{content:"";display:block;width:80px;height:4px;background:var(--accent);margin:12px auto 0;border-radius:2px}
.card{background:#fff;border-radius:14px;box-shadow:0 6px 16px rgba(0,0,0,.08);padding:20px}
.grid{display:grid;gap:18px}
.grid-3{grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
.badge{display:inline-block;background:#e8f3ff;color:#175ea8;padding:6px 10px;border-radius:999px;font-weight:600;font-size:.85rem;margin:2px}
.pub{border-left:4px solid var(--accent);padding:14px 16px;border-radius:8px;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.06)}
.book{display:flex;gap:14px}
.book img{width:88px;height:120px;object-fit:cover;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,.15)}
.footer{background:var(--primary);color:#fff;padding:40px 0;margin-top:80px;text-align:center}
.tab{display:inline-block;margin:0 8px 18px;padding:8px 14px;border-radius:999px;background:#eef3f7;cursor:pointer;font-weight:600}
.tab.active{background:#d9ecff}
.small{color:var(--muted);font-size:.95rem}
.btn{display:inline-block;background:linear-gradient(45deg,var(--accent),var(--primary));color:#fff;border:none;padding:12px 20px;border-radius:999px;font-weight:800;text-decoration:none}
.table{width:100%;border-collapse:collapse}
.table th{background:#e7f1fb;color:#12395e;padding:12px;text-align:left}
.table td{padding:12px;border-bottom:1px solid #eee}
</style>
"""

JS = """
<script>
function switchTab(name){
  document.querySelectorAll('[data-tab]').forEach(el=>{
    el.style.display = (el.dataset.tab===name)?'block':'none';
  });
  document.querySelectorAll('.tab').forEach(el=>{
    if(el.dataset.t===name){el.classList.add('active')} else {el.classList.remove('active')}
  });
}
window.addEventListener('DOMContentLoaded',()=>{switchTab('journals');});
</script>
"""

HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ BIO.full_name }} — {{ BIO.tagline }}</title>
  <meta name="description" content="{{ BIO.full_name }} — {{ BIO.tagline }} at {{ BIO.affiliation }}">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  {{ CSS|safe }}
  <script type="application/ld+json">{{ schema_json|safe }}</script>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark fixed-top">
  <div class="container"><a class="navbar-brand" href="#home">{{ BIO.full_name }}</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav"><span class="navbar-toggler-icon"></span></button>
    <div id="nav" class="collapse navbar-collapse">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item"><a class="nav-link" href="#about">About</a></li>
        <li class="nav-item"><a class="nav-link" href="#education">Education</a></li>
        <li class="nav-item"><a class="nav-link" href="#experience">Experience</a></li>
        <li class="nav-item"><a class="nav-link" href="#publications">Publications</a></li>
        <li class="nav-item"><a class="nav-link" href="#books">Books & Editorial</a></li>
        <li class="nav-item"><a class="nav-link" href="#awards">Awards</a></li>
        <li class="nav-item"><a class="nav-link" href="#contact">Contact</a></li>
      </ul>
    </div>
  </div>
</nav>

<section id="home" class="hero">
  <div class="container">
    <img src="data:image/png;base64,{{ PROFILE_IMG_B64 }}" alt="{{ BIO.full_name }}">
    <h1 class="mt-3 fw-bold">{{ BIO.full_name }}</h1>
    <p class="lead mb-1">{{ BIO.tagline }}</p>
    <p class="small">{{ BIO.affiliation }} • CGPA: {{ BIO.cgpa }}</p>
    <p class="small">Status: <strong>{{ BIO.status }}</strong></p>
    <div class="mt-3">
      <a class="btn" href="{{ BIO.scholar_url }}" target="_blank">Google Scholar</a>
      <a class="btn" href="{{ BIO.linkedin }}" target="_blank" style="margin-left:10px">LinkedIn</a>
      <a class="btn" href="{{ BIO.rg }}" target="_blank" style="margin-left:10px">ResearchGate</a>
      <a class="btn" href="/cv" style="margin-left:10px">Download CV</a>
    </div>
  </div>
</section>

<section id="about" class="section">
  <div class="container">
    <h2 class="section-title">About</h2>
    <div class="card">
      <p class="mb-2">Ph.D. scholar specializing in AI‑driven biomechatronic systems, intelligent prosthetics & wearable health technologies. I integrate multimodal sensors, embedded platforms, and ML for real‑time decision support in healthcare.</p>
      <div class="row g-3 mt-2">
        <div class="col-md-6"><strong>Email:</strong> {{ BIO.email }}<br><strong>Phone:</strong> {{ BIO.phone }}</div>
        <div class="col-md-6"><strong>Location:</strong> {{ BIO.location }}<br><strong>Open to:</strong> {{ BIO.status }}</div>
      </div>
    </div>
  </div>
</section>

<section id="education" class="section bg-light">
  <div class="container">
    <h2 class="section-title">Education</h2>
    <div class="card">
      <table class="table">
        <thead><tr><th>Year</th><th>Degree</th><th>Institute</th><th>CGPA</th></tr></thead>
        <tbody>
          {% for e in EDUCATION %}
          <tr><td><strong>{{ e.year }}</strong></td><td>{{ e.degree }}</td><td>{{ e.inst }}</td><td>{{ e.cgpa }}</td></tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
</section>

<section id="experience" class="section">
  <div class="container">
    <h2 class="section-title">Experience</h2>
    <div class="grid grid-3">
      {% for x in EXPERIENCE %}
      <div class="card">
        <h5 class="mb-0">{{ x.role }}</h5>
        <div class="small">{{ x.org }}</div>
        <div class="small mb-2"><em>{{ x.date }}</em></div>
        <ul class="mb-0">{% for b in x.bullets %}<li>{{ b }}</li>{% endfor %}</ul>
      </div>
      {% endfor %}
    </div>
  </div>
</section>

<section id="publications" class="section bg-light">
  <div class="container">
    <h2 class="section-title">Publications</h2>
    <div class="text-center">
      <span class="tab active" data-t="journals" onclick="switchTab('journals')">Journals</span>
      <span class="tab" data-t="conferences" onclick="switchTab('conferences')">Conferences</span>
      <span class="tab" data-t="book_chapters" onclick="switchTab('book_chapters')">Book Chapters</span>
    </div>

    {% for sec, items in PUBLICATIONS.items() %}
      <div data-tab="{{ sec }}" style="display:none">
        {% if not items %}
          <p class="small text-center">No entries yet.</p>
        {% else %}
          <div class="grid">
          {% for p in items %}
            <div class="pub">
              <div class="fw-bold">{{ p.title }}</div>
              <div class="small">{{ p.authors }} • <em>{{ p.venue }}</em> • {{ p.year }}</div>
              {% if p.notes %}<div class="small">{{ p.notes }}</div>{% endif %}
              {% if p.link %}<a class="btn mt-2" href="{{ p.link }}" target="_blank">View</a>{% endif %}
            </div>
          {% endfor %}
          </div>
        {% endif %}
      </div>
    {% endfor %}

    <p class="small mt-3 text-center">Full list on <a href="{{ BIO.scholar_url }}" target="_blank">Google Scholar</a>.</p>
  </div>
</section>

<section id="books" class="section">
  <div class="container">
    <h2 class="section-title">Books & Editorial</h2>
    <div class="grid grid-3">
      {% for b in BOOKS %}
      <div class="card book">
        <img src="{{ url_for('static', filename=b.cover.replace('static/','')) }}" alt="{{ b.title }} cover" onerror="this.src='https://via.placeholder.com/88x120?text=Cover'">
        <div>
          <div class="fw-bold">{{ b.title }}</div>
          <div class="small">{{ b.publisher }} • {{ b.year }}</div>
          <a class="btn mt-2" href="{{ b.link }}" target="_blank">Details</a>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</section>

<section id="awards" class="section bg-light">
  <div class="container">
    <h2 class="section-title">Awards • Mentoring • Talks</h2>
    <div class="grid grid-3">
      <div class="card">
        <h6 class="fw-bold">Awards</h6>
        <ul class="mb-0">{% for a in AWARDS %}<li>{{ a }}</li>{% endfor %}</ul>
      </div>
      <div class="card">
        <h6 class="fw-bold">Mentoring</h6>
        <ul class="mb-0">{% for m in MENTORING %}<li>{{ m }}</li>{% endfor %}</ul>
      </div>
      <div class="card">
        <h6 class="fw-bold">Talks</h6>
        <ul class="mb-0">{% for t in TALKS %}<li>{{ t.title }} — {{ t.venue }} {% if t.link %}<a href="{{ t.link }}" target="_blank">link</a>{% endif %}</li>{% endfor %}</ul>
      </div>
    </div>
  </div>
</section>

<section id="contact" class="section">
  <div class="container">
    <h2 class="section-title">Contact</h2>
    <div class="grid grid-3">
      <div class="card">
        <form id="contact-form" method="post" action="/contact">
          <div class="mb-2"><label class="form-label">Name</label><input class="form-control" name="name" required></div>
          <div class="mb-2"><label class="form-label">Email</label><input type="email" class="form-control" name="email" required></div>
          <div class="mb-2"><label class="form-label">Subject</label><input class="form-control" name="subject" required></div>
          <div class="mb-2"><label class="form-label">Message</label><textarea class="form-control" name="message" rows="5" required></textarea></div>
          <!-- honeypot -->
          <input type="text" name="hp_field" style="display:none">
          <button class="btn" type="submit">Send Message</button>
        </form>
      </div>
      <div class="card">
        <h6 class="fw-bold">Direct</h6>
        <p class="mb-1"><strong>Email:</strong> {{ BIO.email }}</p>
        <p class="mb-1"><strong>Phone:</strong> {{ BIO.phone }}</p>
        <p class="mb-1"><strong>Location:</strong> {{ BIO.location }}</p>
        <p class="small">Also see Google Scholar, LinkedIn, ResearchGate links at the top.</p>
      </div>
    </div>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <p class="mb-0">© {{ now.year }} {{ BIO.full_name }} • {{ BIO.tagline }}</p>
  </div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
{{ JS|safe }}
</body>
</html>
"""

# ------------------------------
# Routes
# ------------------------------

@app.route("/")
def home():
    schema = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": BIO["full_name"],
        "jobTitle": "PhD Scholar",
        "affiliation": BIO["affiliation"],
        "email": BIO["email"],
        "url": request.url_root.rstrip("/"),
        "sameAs": [BIO["scholar_url"], BIO["linkedin"], BIO["rg"]],
    }
    return render_template_string(
        HTML,
        CSS=CSS,
        JS=JS,
        BIO=BIO,
        EDUCATION=EDUCATION,
        EXPERIENCE=EXPERIENCE,
        PUBLICATIONS=PUBLICATIONS,
        BOOKS=BOOKS,
        AWARDS=AWARDS,
        MENTORING=MENTORING,
        TALKS=TALKS,
        PROFILE_IMG_B64=PROFILE_IMG_B64,
        now=datetime.utcnow(),
        schema_json=json.dumps(schema),
    )

@app.route("/api/publications")
def publications_api():
    return jsonify(PUBLICATIONS)

@app.route("/contact", methods=["POST"]) 
def contact():
    data = request.form or request.get_json(force=True, silent=True) or {}
    # spam honeypot
    if data.get("hp_field"):
        return jsonify({"success": True})
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    subject = (data.get("subject") or "").strip()
    message = (data.get("message") or "").strip()
    if not (name and email and subject and message):
        return jsonify({"success": False, "error": "Missing fields"}), 400
    try:
        msg = Message(subject=f"[VK Site] {subject}", recipients=[BIO["email"]])
        msg.body = f"""
From: {name} <{email}>
Subject: {subject}

{message}
--
Sent via vk-1403/VK site
"""
        mail.send(msg)
        return jsonify({"success": True})
    except Exception as e:
        logging.error(f"Mail error: {e}")
        return jsonify({"success": False, "error": "Email failed"}), 500

@app.route("/cv")
def serve_cv():
    # Place your CV at static/cv/Vidyapati_Kumar_CV.pdf
    path = os.path.join("static", "cv", "Vidyapati_Kumar_CV.pdf")
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return ("CV not found. Please add it at static/cv/Vidyapati_Kumar_CV.pdf", 404)

@app.errorhandler(404)
def nf(e):
    return ("Page not found", 404)

@app.errorhandler(500)
def se(e):
    logging.exception("Server error:")
    return ("Internal server error", 500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

