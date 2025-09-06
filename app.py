"""
Flask-based personal website for Vidyapati Kumar.

This is a complete rewrite of the earlier single file application with the goal
of providing a richer, more polished representation of the user's CV and
accomplishments.  The site aims to be a showcase for prospective employers
and collaborators while adhering to good accessibility practices and simple
deployment.  Data describing education, experience, patents, publications,
books, skills, certifications, awards and extracurricular activities are
defined near the top of the module so they can easily be updated without
touching the rest of the code.  All markup lives inside a single Jinja2
string (HTML) for ease of deployment on platforms such as Render.

If you wish to add your CV PDF, place it at ``static/cv/Vidyapati_Kumar_CV.pdf``.
The ``b64_image`` helper tries to read the author's portrait from
``static/mypic/VK.png``; if that file is missing it falls back to a simple
placeholder avatar generated from an SVG.
"""

import os
import json
import base64
import logging
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, send_file, url_for
from flask_mail import Mail, Message

# ----------------------------------------------------------------------------
# Application setup
# ----------------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "please-change-this-secret")

app.config.update(
    MAIL_SERVER=os.environ.get("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_PORT=int(os.environ.get("MAIL_PORT", 587)),
    MAIL_USE_TLS=os.environ.get("MAIL_USE_TLS", "true").lower() == "true",
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME", "vidyapatikumar.me@gmail.com"),
    # It is recommended to set either MAIL_PASSWORD or GMAIL_APP_PASSWORD in your
    # environment.  If neither is set the contact form will silently fail.
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD") or os.environ.get("GMAIL_APP_PASSWORD"),
    MAIL_DEFAULT_SENDER=os.environ.get("MAIL_DEFAULT_SENDER", "vidyapatikumar.me@gmail.com"),
)
mail = Mail(app)
logging.basicConfig(level=logging.INFO)

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def b64_image(path: str) -> str:
    """Return a base64 data URI for an image on disk or a fallback SVG.

    If ``path`` cannot be opened this function returns a simple SVG avatar
    encoded in base64.  This prevents broken images on the site.
    """
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception as exc:
        logging.warning(f"Image not found at {path}: {exc}")
        # Fallback SVG – a simple abstract avatar on a gradient background
        svg = (
            "<svg width='200' height='200' xmlns='http://www.w3.org/2000/svg'>"
            "<defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>"
            "<stop offset='0%' stop-color='#1A3262'/><stop offset='100%' stop-color='#2D7DD2'/></linearGradient></defs>"
            "<rect width='100%' height='100%' fill='url(#g)'/>"
            "<circle cx='100' cy='80' r='35' fill='white'/>"
            "<ellipse cx='100' cy='150' rx='55' ry='40' fill='white'/>"
            "</svg>"
        )
        return base64.b64encode(svg.encode()).decode("utf-8")

# Attempt to load a personal portrait.  Place your portrait at static/mypic/VK.png.
PROFILE_IMG_B64 = b64_image("static/mypic/VK.png")

# ----------------------------------------------------------------------------
# Data definitions – edit these lists/dicts to update the content on the site.
# ----------------------------------------------------------------------------
BIO = {
    "full_name": "Vidyapati Kumar",
    "tagline": "PhD Scholar • AI, Biomechatronics & Intelligent Prosthetics",
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
    {"year": "Dec 2025 (Expected)", "degree": "Ph.D. in Mechanical Engineering", "inst": "IIT Kharagpur, India", "cgpa": "8.5/10"},
    {"year": "2018", "degree": "M.E. in Production Engineering", "inst": "Jadavpur University, India", "cgpa": "8.38/10"},
    {"year": "2016", "degree": "B.Tech in Mechanical Engineering", "inst": "MAKAUT, India", "cgpa": "9.19/10"},
]

EXPERIENCE = [
    {
        "role": "Senior Research Fellow — AI‑Enhanced Powered Ankle‑Foot Prosthetic System",
        "org": "Indian Institute of Technology Kharagpur",
        "date": "Jul 2021 – Present",
        "bullets": [
            "Designed and built a microcontroller‑based sensor fusion platform using ESP32 and Raspberry Pi for real‑time terrain classification via LiDAR and IMU streams.",
            "Developed multimodal gait control strategies with 16‑channel FSR insoles, IMUs and Maxon motors to detect gait phases and drive adaptive actuation.",
            "Implemented comprehensive Python pipelines (pandas, NumPy, SciPy) for data processing, model training and evaluation; used SHAP values to interpret classification results and achieved >90% gait‑phase accuracy.",
            "Deployed vision‑based kinematic analysis using Vision Transformers, YOLOv8, OpenPose and custom background subtraction to produce Gait Energy Images; classification accuracy exceeded 96% for orthopedic pathologies.",
            "Performed multi‑criteria material selection and structural validation for prosthetic components via COMSOL finite element analysis.",
            "Developed an LLM‑driven clinical decision support tool (CDS ProsthetiX) using LangChain and Streamlit to provide personalised evidence‑based prosthetic recommendations.",
            "Conducted extensive sensor trials across diverse terrains and load conditions to validate reliability and robustness.",
        ],
    },
    {
        "role": "Project Mentor — Chanakya Fellowship",
        "org": "TIH Foundation for IoT & IoE (IIT Bombay) / DST, Government of India",
        "date": "Feb 2024 – Present",
        "bullets": [
            "Leading a DST‑funded project titled \"Development of Intelligent and User‑Friendly Prosthetic for Real‑World Applications\" under the Chanakya Fellowship Scheme.",
            "Mentoring design and deployment of an end‑to‑end IoT‑enabled prosthetic system involving embedded platforms, real‑time data acquisition, control integration and cloud back‑end.",
            "Coordinating cross‑functional teams across hardware, firmware and cloud layers; guiding prototyping, testing and version control while mentoring master’s and undergraduate students.",
            "Engaging with program managers and industry partners to ensure milestone delivery, budget compliance and translational impact in assistive technology.",
        ],
    },
    {
        "role": "Teaching Assistant — NPTEL Courses",
        "org": "Indian Institute of Technology Kharagpur",
        "date": "Jan 2021 – Present",
        "bullets": [
            "Assisted Prof. D. K. Pratihar in delivering NPTEL courses on Robotics, Fuzzy Logic and Optimisation Tools.",
            "Developed illustrative code examples in Python and MATLAB and provided mentorship to students.",
        ],
    },
    {
        "role": "Faculty — GATE (Mechanical)",
        "org": "Unacademy (EdTech)",
        "date": "Aug 2020 – Dec 2020",
        "bullets": [
            "Taught Manufacturing, Strength of Materials, Thermodynamics and Engineering Mathematics to GATE aspirants.",
            "Conducted problem‑solving sessions and mock tests to prepare candidates for the competitive exam.",
        ],
    },
    {
        "role": "Project Assistant — Design Guidelines for Underground Coal Extraction",
        "org": "CSIR‑Central Institute of Mining and Fuel Research",
        "date": "Aug 2018 – Mar 2020",
        "bullets": [
            "Developed CAD models and numerical simulations to optimise extraction parameters for deep seams (300 m+).",
            "Processed geo‑mining data and implemented MATLAB‑based optimisation algorithms to improve mine safety guidelines.",
        ],
    },
    {
        "role": "M.E. Thesis — Intelligent Advisory System for NTM Processes",
        "org": "Jadavpur University",
        "date": "Aug 2016 – Mar 2018",
        "bullets": [
            "Designed a VBASIC‑based expert system to recommend optimal parameters for non‑traditional machining (NTM) processes based on material and geometric inputs.",
            "Validated system performance across multiple real‑world case studies.",
        ],
    },
    {
        "role": "B.Tech Thesis — Assistive System for Visually Impaired Persons",
        "org": "Maulana Abul Kalam Azad University of Technology",
        "date": "Aug 2015 – Mar 2016",
        "bullets": [
            "Built an Arduino‑based navigation system using ultrasonic and PIR sensors integrated into wearable shoe, belt and cap for obstacle detection.",
            "Designed user interface and control logic to manage sensor alerts and provide reliable guidance to visually impaired users.",
        ],
    },
]

PATENTS = [
    {
        "title": "A Compact and Powered Ankle‑Foot Prosthetic Device",
        "meta": "Indian Patent Application No. 202431037184 (Published & Under Examination)",
        "year": "2024",
        "inst": "IIT Kharagpur",
        "bullets": [
            "Developed a prosthetic device that adjusts foot height and ankle angle in real time.",
            "Integrated a spring‑loaded split forefoot to enhance shock absorption and push‑off dynamics during gait.",
            "Engineered a hybrid actuation system (active + passive) to improve stability and mobility for transtibial amputees.",
        ],
        "link": "https://drive.google.com/drive/u/7/folders/1AYkEL0NrkHq8G8woTFXXk5bVwJaTIVLk",
    },
    {
        "title": "ProsthetiX‑AI — Clinical Decision Support for Ankle‑Foot Prosthetic Recommendations",
        "meta": "Indian Copyright Application No. 9678/2025‑CO/SW",
        "year": "2025",
        "inst": "IIT Kharagpur",
        "bullets": [
            "Designed and implemented a copyright‑registered clinical decision support tool for ankle‑foot prosthetic prescriptions.",
            "Powered by large language models, LangChain and Streamlit; integrates explainable AI, K‑level logic and real‑time academic citation justification for clinical use.",
        ],
        "link": "https://drive.google.com/drive/u/7/folders/1AYkEL0NrkHq8G8woTFXXk5bVwJaTIVLk",
    },
]

PUBLICATIONS = {
    # Selected journal publications with notes.  Additional journal publications are
    # included below under the "additional" key and will be rendered in a
    # separate section.
    "journals": [
        {
            "title": "Wearable sensor‑based intent recognition for adaptive control of intelligent ankle‑foot prosthetics",
            "venue": "Measurement: Sensors, 39, 101865 (Elsevier)",
            "year": 2025,
            "authors": "V. Kumar; D. K. Pratihar",
            "link": "https://www.sciencedirect.com/science/article/pii/S2665917425000595",
            "notes": "Developed intent recognition using FSR and accelerometer data; achieved 96.3% accuracy with SBLSTM; 25 ms inference.",
        },
        {
            "title": "Biomechanical material selection for ankle‑foot prosthetics: An ensemble MCDM‑FEA framework",
            "venue": "International Journal on Interactive Design and Manufacturing (Springer)",
            "year": 2025,
            "authors": "V. Kumar; D. K. Pratihar",
            "link": "https://link.springer.com/article/10.1007/s12008-025-02340-4",
            "notes": "Developed a hybrid MCDM‑FEA model to rank prosthetic materials based on mechanical strength, fatigue and damping.",
        },
        {
            "title": "Mechatronic and AI‑driven framework for non‑invasive screening of knee abnormalities using multimodal sensors",
            "venue": "Computer Methods in Biomechanics and Biomedical Engineering",
            "year": 2024,
            "authors": "V. Kumar; M. V. Hrishikesh; M. Shijas; D. K. Pratihar",
            "link": "",
            "notes": "Combined sEMG and goniometer data for early knee abnormality detection; achieved 92.3% cross‑validated accuracy with Extra Trees classifier and used SHAP for interpretability.",
        },
        {
            "title": "Fuzzy logic‑based synchronization of trajectory planning and obstacle avoidance for RRP SCARA robot",
            "venue": "International Journal on Interactive Design and Manufacturing (IJIDeM)",
            "year": 2025,
            "authors": "V. Kumar; A. Mistri",
            "link": "https://link.springer.com/article/10.1007/s12008-024-02214-1",
            "notes": "Introduced a fuzzy‑logic controller for coordinated trajectory planning and obstacle avoidance in SCARA robots.",
        },
        {
            "title": "A SWARA‑CoCoSo‑based approach for spray painting robot selection",
            "venue": "Informatica 33(1) 35–54",
            "year": 2022,
            "authors": "V. Kumar; K. Kalita; P. Chatterjee; E. K. Zavadskas; S. Chakraborty",
            "link": "https://informatica.vu.lt/journal/INFORMATICA/article/1237/info",
            "notes": "Applied SWARA and CoCoSo multi‑criteria decision‑making methods to select optimal spray painting robots.",
        },
        {
            "title": "Teaching‑learning‑based parametric optimization of EDM parameters",
            "venue": "Facta Universitatis: Mechanical Engineering 18(2) 281–300",
            "year": 2020,
            "authors": "V. Kumar; S. Diyaley; S. Chakraborty",
            "link": "https://casopisi.junis.ni.ac.rs/index.php/FUMechEng/article/view/6156/0",
            "notes": "Optimised EDM parameters using teaching‑learning‑based search; demonstrated improved machining performance.",
        },
        {
            "title": "Grey‑fuzzy method‑based parametric analysis of AWJM on GFRP composites",
            "venue": "Sādhanā 45(1) 1–18",
            "year": 2020,
            "authors": "V. Kumar; P. P. Das; S. Chakraborty",
            "link": "https://link.springer.com/article/10.1007/s12046-020-01355-9",
            "notes": "Performed grey‑fuzzy analysis for optimising abrasive water jet machining on glass fibre reinforced polymers.",
        },
        {
            "title": "Machine learning prediction of erosion resistance of laser‑clad coatings on martensitic stainless steel for steam turbine blades",
            "venue": "Journal of Micromanufacturing",
            "year": 2025,
            "authors": "I. Mandal; V. Kumar; P. Saha",
            "link": "https://journals.sagepub.com/doi/full/10.1177/25165984251317028",
            "notes": "Applied machine learning to predict erosion resistance of laser‑clad coatings; improved turbine blade longevity.",
        },
        {
            "title": "Optimizing healthcare in the digital era: Fusion of IoT with other techniques",
            "venue": "EAI Endorsed Transactions on Internet of Things, 11",
            "year": 2025,
            "authors": "R. Singh; A. Chaudhary; V. Kumar",
            "link": "https://publications.eai.eu/index.php/IoT/article/view/6077",
            "notes": "Reviewed integration of IoT with AI, blockchain and other technologies to enhance healthcare services.",
        },
        {
            "title": "Heat checking as a failure mechanism of dies exposed to thermal cycles: A review",
            "venue": "Journal of Materials Research and Technology 26",
            "year": 2023,
            "authors": "P. Solgi; M. Chenarani; A. R. Eivani; M. Ghosh; V. Kumar; H. R. Jafarian",
            "link": "https://www.sciencedirect.com/science/article/pii/S223878542301699X",
            "notes": "Comprehensive review of heat checking in dies subjected to cyclic thermal loads.",
        },
        {
            "title": "Experimental investigation and optimization of electric discharge machining process parameters using grey‑fuzzy hybrids",
            "venue": "Materials 14(19)",
            "year": 2021,
            "authors": "A. Sharma; V. Kumar; et al.",
            "link": "https://www.mdpi.com/1996-1944/14/19/5820",
            "notes": "Employed grey‑fuzzy techniques to optimise EDM parameters for improved performance and surface quality.",
        },
        {
            "title": "Functionally graded adherents on failure of FRP socket joints",
            "venue": "Materials 14(21)",
            "year": 2021,
            "authors": "C. Prakash; V. Kumar; et al.",
            "link": "https://www.mdpi.com/1996-1944/14/21/6365",
            "notes": "Investigated the influence of functionally graded adherents on the failure behaviour of fibre reinforced polymer socket joints.",
        },
        {
            "title": "Intelligent decision model for non‑traditional machining processes",
            "venue": "Decision Making: Applications in Management and Engineering 4(1) 194–214",
            "year": 2021,
            "authors": "S. Chakraborty; V. Kumar",
            "link": "https://dmame-journal.org/index.php/dmame/article/view/154",
            "notes": "Proposed an intelligent decision model to select optimal NTM processes based on multiple criteria.",
        },
        {
            "title": "Selection of the all‑time best World XI Test cricket team using the TOPSIS method",
            "venue": "Decision Science Letters 8(1) 95–108",
            "year": 2018,
            "authors": "S. Chakraborty; V. Kumar; K. R. Ramakrishnan",
            "link": "https://growingscience.com/beta/dsl/2817-selection-of-the-all-time-best-world-xi-test-cricket-team-using-the-topsis-method.html",
            "notes": "Applied TOPSIS to select the all‑time best World XI Test cricket team based on multiple performance metrics.",
        },
        {
            "title": "A grey fuzzy logic approach for cotton fibre selection",
            "venue": "Journal of The Institution of Engineers (India): Series E 98(1) 1–9",
            "year": 2017,
            "authors": "S. Chakraborty; P. P. Das; V. Kumar",
            "link": "https://link.springer.com/article/10.1007/s40034-017-0099-7",
            "notes": "Used grey‑fuzzy logic to optimise cotton fibre selection for improved textile quality.",
        },
    ],
    "conferences": [
        {
            "title": "Vision Transformer‑based pose estimation for automated gait analysis in ankle‑foot prosthetic design",
            "venue": "IEEE InCACCT 2024",
            "year": 2024,
            "authors": "V. Kumar; D. K. Pratihar",
            "link": "https://ieeexplore.ieee.org/document/10551002",
            "notes": "Benchmarked YOLOv8, DeepPose and RTM Pose models; achieved MAE = 19.75, R² = 99.5% and 107.7 ms inference time using RTM Pose.",
        },
        {
            "title": "Terrain recognition for intelligent powered ankle‑foot prosthetics using sEMG and ensemble learning models",
            "venue": "IEEE INDICON 2024",
            "year": 2024,
            "authors": "V. Kumar; M. V. Hrishikesh; M. Shijas; D. K. Pratihar",
            "link": "https://ieeexplore.ieee.org/document/10958532?reason=concurrency",
            "notes": "Developed terrain classification framework using sEMG signals from nine lower‑limb muscles; optimised Extra Trees classifier achieving 87% accuracy and 0.88 F1 score.",
        },
    ],
    "book_chapters": [
        {
            "title": "A research perspective on ankle–foot prosthetics designs for transtibial amputees",
            "venue": "Mechanical Engineering in Biomedical Applications (Wiley)",
            "year": 2024,
            "authors": "V. Kumar; P. Gupta; D. K. Pratihar",
            "link": "https://onlinelibrary.wiley.com/doi/10.1002/9781394175109.ch16",
            "notes": "Comprehensive review of transtibial prosthetic designs, materials and biomechanics; highlighted challenges and future directions in user‑adaptable, energy‑efficient designs.",
        },
        {
            "title": "Intelligent ankle‑foot prosthetics: From engineering fundamentals to integrated artificial intelligence systems",
            "venue": "Advancing Healthcare Through Decision Intelligence (Elsevier)",
            "year": 2025,
            "authors": "V. Kumar; R. R. Prakash; D. K. Pratihar",
            "link": "https://www.sciencedirect.com/science/article/pii/B9780443264801000084",
            "notes": "Presented an end‑to‑end overview of intelligent ankle–foot orthosis design integrating mechatronics, AI and sensor fusion; proposed a modular framework for intent‑adaptive control.",
        },
        {
            "title": "Comparative evaluation of deep learning techniques for multistage Alzheimer’s prediction from magnetic resonance images",
            "venue": "Biomedical Robots and Devices in Healthcare (Elsevier)",
            "year": 2025,
            "authors": "P. Gupta; P. Nahak; V. Kumar; D. K. Pratihar; K. Deb",
            "link": "https://www.sciencedirect.com/science/article/pii/B9780443222061000073",
            "notes": "Trained VGG‑16 on 12,800 augmented MRI images for multiclass Alzheimer’s staging; achieved 89.9% test accuracy with superior performance in mild dementia detection.",
        },
        {
            "title": "Advancing ankle–foot orthosis design through biomechanics, robotics and additive manufacturing: A review",
            "venue": "Biomedical Robots and Devices in Healthcare (Elsevier)",
            "year": 2025,
            "authors": "V. Kumar; P. Gupta; D. K. Pratihar",
            "link": "https://www.sciencedirect.com/science/article/pii/B9780443222061000061",
            "notes": "Reviewed biomechanics, additive manufacturing and control strategies for ankle–foot orthosis design; proposed future directions incorporating AI‑driven adaptation and soft robotics.",
        },
    ],
}

# Additional journal publications for extended reading; these are rendered in a
# collapsed details section in the Publications area.
PUBLICATIONS_ADDITIONAL = [
    {"title": "Application of grey‑fuzzy logic technique for parametric optimisation of non‑traditional machining processes", "venue": "Grey Systems: Theory and Application 8(1) 46–68", "year": 2017, "authors": "S. Chakraborty; P. P. Das; V. Kumar", "link": "https://www.emerald.com/insight/content/doi/10.1108/gs-08-2017-0028/full/html"},
    {"title": "Medical imaging and analysis of thermal necrosis during bone grinding: Implementation of NSGA‑III in healthcare", "venue": "Current Medical Imaging 20(1) 1–23", "year": 2024, "authors": "A. Babbar; V. Jain; V. Gupta; D. Gupta; V. Kumar; B. P. Pathri", "link": "https://www.sciencedirect.com/org/science/article/pii/S1573405624003370"},
]

BOOKS = [
    {
        "title": "Biomedical Robots and Devices in Healthcare: Opportunities and Challenges for Future Applications",
        "authors": "Iqbal, F.; Gupta, P.; Kumar, V.; Pratihar, D. K.",
        "year": "2024",
        "publisher": "Elsevier Science & Technology",
        "link": "https://www.sciencedirect.com/book/9780443222061/biomedical-robots-and-devices-in-healthcare",
        "cover": "mypic/book1.jpg",
    },
    {
        "title": "Advancing Healthcare Through Decision Intelligence: Machine Learning, Robotics, and Analytics in Biomedical Informatics",
        "authors": "Dey, S.; Kumar, V.; Pratihar, D. K.; Singh, V. P.; Islam, S. M. N.",
        "year": "2025",
        "publisher": "Academic Press (Elsevier)",
        "link": "https://www.sciencedirect.com/book/9780443264801/advancing-healthcare-through-decision-intelligence",
        "cover": "mypic/book2.jpg",
    },
    {
        "title": "Quantum Computing, Cyber Security and Cryptography",
        "authors": "Goyal, S. B.; Kumar, V.; Islam, S. M. N.; Ghai, D.",
        "year": "2025",
        "publisher": "Springer",
        "link": "https://link.springer.com/book/10.1007/978-981-96-4948-8",
        "cover": "mypic/book3.jpg",
    },
]

SKILLS = {
    "Programming & Frameworks": ["Python", "C++", "MATLAB", "Jupyter Notebook", "Google Colab"],
    "IoT & Embedded Systems": ["Arduino", "ESP32", "Raspberry Pi", "Sensor Fusion (EMG, IMU, FSR)", "Real‑Time Control"],
    "AI/ML & Data Science": ["scikit‑learn", "PyTorch", "TensorFlow", "SHAP", "LIME"],
    "Modeling & Simulation": ["Finite Element Analysis (FEA)", "COMSOL", "OpenSim", "CAD"],
    "Computer Vision & CAM Techniques": ["OpenCV", "scikit‑image", "Vision Transformers", "YOLOv8", "Grad‑CAM", "Attention Maps"],
    "Signal Processing": ["EMG/Goniometer/IMU/FSR Data Analysis", "Time‑Series Forecasting", "Statistical Testing"],
    "Tools & Others": ["Optimisation & MCDM", "Soft Computing", "Research‑Paper Writing", "Git", "APIs", "DB Design"],
}

CERTIFICATIONS = [
    {"year": "2020", "name": "Machine Learning", "provider": "Stanford University (Coursera)"},
    {"year": "2020", "name": "Introduction to Robotic Process Automation, Artificial Intelligence and Data Analytics", "provider": "Simplilearn"},
]

AWARDS = [
    "Chanakya Fellowship (DST/TIH‑IoT), 2024–present",
    "Karyashala: RAAIBA‑2022 (SERB/DST) — 7‑day high‑end workshop on AI for Biomedical Applications",
    "Institute Assistantship (MHRD) — PhD Research Scholar, IIT Kharagpur (2021–present)",
    "GATE Fellowship — Jadavpur University (2016–2018)",
]

EXTRA_CURRICULAR = [
    {"activity": "Equity & Mutual Fund Investing", "description": "Personal interest in financial markets; actively manage a portfolio with long‑term investments in mutual funds, stocks and IPOs."},
    {"activity": "Swimming", "description": "Passionate about swimming; regularly pursue it as a recreational activity for fitness and stress relief."},
]

MENTORING = [
    "Srinjoy — Terrain geometry estimation with RPLiDAR + Raspberry Pi for adaptive prosthetic control",
]

TALKS = [
    {"title": "Vision Transformers for Automated Gait Analysis", "venue": "InCACCT 2024", "link": "https://ieeexplore.ieee.org/document/10551002"},
]

# ----------------------------------------------------------------------------
# HTML, CSS and JavaScript templates
# ----------------------------------------------------------------------------
CSS = """
<style>
/* Colour palette – lightened for better contrast */
:root{--primary:#1a3a64;--accent:#2d7dd2;--light:#f7fafc;--text:#1a202c;--muted:#718096}
*{box-sizing:border-box}body{font-family:Segoe UI,Tahoma,Arial,sans-serif;background:var(--light);color:var(--text);margin:0;padding:0}
.navbar{background:linear-gradient(135deg,var(--primary),var(--accent));box-shadow:0 2px 8px rgba(0,0,0,.1)}
.navbar a{color:#fff!important;font-weight:600}
.hero{padding:80px 0;background:linear-gradient(135deg,var(--primary),var(--accent));color:#fff;text-align:center;position:relative}
.hero img{width:200px;height:200px;border-radius:50%;border:5px solid #fff;object-fit:cover;box-shadow:0 8px 30px rgba(0,0,0,.25)}
.section{padding:60px 0}
.section-title{font-size:1.75rem;font-weight:800;text-align:center;margin:0 0 24px;position:relative;color:var(--primary)}
.section-title:after{content:"";display:block;width:80px;height:4px;background:var(--accent);margin:12px auto 0;border-radius:2px}
.card{background:#fff;border-radius:14px;box-shadow:0 4px 12px rgba(0,0,0,.08);padding:20px}
.grid{display:grid;gap:18px}
.grid-3{grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
.badge{display:inline-block;background:#e8f3ff;color:#175ea8;padding:6px 10px;border-radius:999px;font-weight:600;font-size:.85rem;margin:2px}
.pub{border-left:4px solid var(--accent);padding:14px 16px;border-radius:8px;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.06)}
.book{display:flex;gap:14px}
.book img{width:88px;height:120px;object-fit:cover;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,.15)}
.footer{background:var(--primary);color:#fff;padding:40px 0;margin-top:80px;text-align:center}
.tab{display:inline-block;margin:0 8px 18px;padding:8px 14px;border-radius:999px;background:#eef3f7;cursor:pointer;font-weight:600;color:var(--text)}
.tab.active{background:#d9ecff;color:var(--primary)}
.small{color:var(--muted);font-size:.95rem}
.btn{display:inline-block;background:linear-gradient(45deg,var(--accent),var(--primary));color:#fff;border:none;padding:12px 20px;border-radius:999px;font-weight:800;text-decoration:none;transition:background .2s ease}
.btn:hover{background:linear-gradient(45deg,var(--primary),var(--accent))}
.table{width:100%;border-collapse:collapse}
.table th{background:#e7f1fb;color:#12395e;padding:12px;text-align:left}
.table td{padding:12px;border-bottom:1px solid #eee}
ul{padding-left:20px}
/* Toast */
.toast-msg{position:fixed;right:18px;bottom:18px;background:rgba(26,58,100,0.95);color:#fff;padding:12px 16px;border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.2);z-index:9999;transition:opacity .4s ease;}
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

// Toast helper
function showToast(msg) {
  const t = document.getElementById('toast');
  if (!t) return;
  t.textContent = msg;
  t.style.display = 'block';
  t.style.opacity = '1';
  setTimeout(() => {
    t.style.opacity = '0';
    setTimeout(() => { t.style.display = 'none'; t.style.opacity = '1'; }, 400);
  }, 2500);
}

document.addEventListener('DOMContentLoaded', () => {
  const f = document.getElementById('contact-form');
  if (!f) return;
  f.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(f);
    try {
      const res = await fetch('/contact', { method: 'POST', body: fd });
      const j = await res.json().catch(() => ({}));
      if (res.ok && j && j.success) {
        showToast('Message sent!');
        f.reset();
      } else {
        showToast(j.error || 'Failed to send. Please try again.');
      }
    } catch {
      showToast('Network error. Please try again.');
    }
  });
});
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
        <li class="nav-item"><a class="nav-link" href="#patents">Patents</a></li>
        <li class="nav-item"><a class="nav-link" href="#publications">Publications</a></li>
        <li class="nav-item"><a class="nav-link" href="#books">Books &amp; Editorial</a></li>
        <li class="nav-item"><a class="nav-link" href="#skills">Skills</a></li>
        <li class="nav-item"><a class="nav-link" href="#awards">Awards</a></li>
        <li class="nav-item"><a class="nav-link" href="#extra">Extra Curricular</a></li>
        <li class="nav-item"><a class="nav-link" href="#contact">Contact</a></li>
      </ul>
    </div>
  </div>
</nav>

<section id="home" class="hero">
  <div class="container">
    <img src="data:image/png;base64,{{ PROFILE_IMG_B64 }}" alt="{{ BIO.full_name }} portrait">
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
      <p class="mb-2">Ph.D. scholar specialising in AI‑driven biomechatronic systems, intelligent prosthetics & wearable health technologies. My research integrates machine learning, sensor fusion, embedded platforms and multi‑criteria optimisation to deliver real‑time decision support for next‑generation prosthetic devices.</p>
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

<section id="patents" class="section bg-light">
  <div class="container">
    <h2 class="section-title">Patents &amp; Copyrights</h2>
    <div class="grid">
      {% for p in PATENTS %}
      <div class="card">
        <h5 class="mb-0">{{ p.title }}</h5>
        <div class="small">{{ p.meta }} • {{ p.year }} • {{ p.inst }}</div>
        <ul class="mb-2">{% for b in p.bullets %}<li>{{ b }}</li>{% endfor %}</ul>
        {% if p.link %}<a class="btn" href="{{ p.link }}" target="_blank">Documents</a>{% endif %}
      </div>
      {% endfor %}
    </div>
  </div>
</section>

<section id="publications" class="section">
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

    <details class="mt-3">
      <summary>Additional Journal Publications</summary>
      <ul class="mt-2">
        {% for a in PUBLICATIONS_ADDITIONAL %}
        <li><strong>{{ a.title }}</strong> — <em>{{ a.venue }}</em> • {{ a.year }}</li>
        {% endfor %}
      </ul>
    </details>

    <p class="small mt-3 text-center">Full list on <a href="{{ BIO.scholar_url }}" target="_blank">Google Scholar</a>.</p>
  </div>
</section>

<section id="books" class="section bg-light">
  <div class="container">
    <h2 class="section-title">Books &amp; Editorial</h2>
    <div class="grid grid-3">
      {% for b in BOOKS %}
      <div class="card book">
        <img src="{{ url_for('static', filename=b.cover) }}" alt="Cover image for {{ b.title }}" onerror="this.src='https://via.placeholder.com/88x120?text=Cover'">
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

<section id="skills" class="section">
  <div class="container">
    <h2 class="section-title">Skills &amp; Certifications</h2>
    <div class="grid grid-3">
      {% for cat, items in SKILLS.items() %}
      <div class="card">
        <h6 class="fw-bold">{{ cat }}</h6>
        <ul class="mb-0">{% for i in items %}<li>{{ i }}</li>{% endfor %}</ul>
      </div>
      {% endfor %}
      <div class="card">
        <h6 class="fw-bold">Certifications</h6>
        <ul class="mb-0">{% for c in CERTIFICATIONS %}<li>{{ c.year }} — {{ c.name }} ({{ c.provider }})</li>{% endfor %}</ul>
      </div>
    </div>
  </div>
</section>

<section id="awards" class="section bg-light">
  <div class="container">
    <h2 class="section-title">Awards &amp; Achievements</h2>
    <div class="grid">
      <div class="card">
        <ul class="mb-0">{% for a in AWARDS %}<li>{{ a }}</li>{% endfor %}</ul>
      </div>
    </div>
  </div>
</section>

<section id="extra" class="section">
  <div class="container">
    <h2 class="section-title">Extra Curricular</h2>
    <div class="grid grid-3">
      {% for e in EXTRA_CURRICULAR %}
      <div class="card">
        <h6 class="fw-bold">{{ e.activity }}</h6>
        <p class="mb-0 small">{{ e.description }}</p>
      </div>
      {% endfor %}
    </div>
  </div>
</section>

<section id="contact" class="section bg-light">
  <div class="container">
    <h2 class="section-title">Contact</h2>
    <div class="grid grid-3">
      <div class="card">
        <form id="contact-form" method="post" action="/contact">
          <div class="mb-2">
            <label class="form-label" for="name">Name</label>
            <input class="form-control" id="name" name="name" required>
          </div>
          <div class="mb-2">
            <label class="form-label" for="email">Email</label>
            <input type="email" class="form-control" id="email" name="email" required>
          </div>
          <div class="mb-2">
            <label class="form-label" for="subject">Subject</label>
            <input class="form-control" id="subject" name="subject" required>
          </div>
          <div class="mb-2">
            <label class="form-label" for="message">Message</label>
            <textarea class="form-control" id="message" name="message" rows="5" required></textarea>
          </div>
          <!-- Honeypot anti‑spam field -->
          <input type="text" name="hp_field" style="display:none">
          <button class="btn" type="submit">Send Message</button>
        </form>
      </div>
      <div class="card">
        <h6 class="fw-bold">Direct</h6>
        <p class="mb-1"><strong>Email:</strong> {{ BIO.email }}</p>
        <p class="mb-1"><strong>Phone:</strong> {{ BIO.phone }}</p>
        <p class="mb-1"><strong>Location:</strong> {{ BIO.location }}</p>
        <p class="small">Also see Google Scholar, LinkedIn and ResearchGate links at the top.</p>
      </div>
    </div>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <p class="mb-0">© {{ now.year }} {{ BIO.full_name }} • {{ BIO.tagline }}</p>
  </div>
</footer>

<!-- Toast container (ARIA live region for accessibility) -->
<div id="toast" class="toast-msg" role="alert" aria-live="polite" style="display:none"></div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
{{ JS|safe }}
</body>
</html>
"""

# ----------------------------------------------------------------------------
# Flask routes
# ----------------------------------------------------------------------------
@app.route("/")
def home():
    # Schema.org Person markup for better SEO
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
        PATENTS=PATENTS,
        PUBLICATIONS=PUBLICATIONS,
        PUBLICATIONS_ADDITIONAL=PUBLICATIONS_ADDITIONAL,
        BOOKS=BOOKS,
        SKILLS=SKILLS,
        CERTIFICATIONS=CERTIFICATIONS,
        AWARDS=AWARDS,
        EXTRA_CURRICULAR=EXTRA_CURRICULAR,
        MENTORING=MENTORING,
        TALKS=TALKS,
        PROFILE_IMG_B64=PROFILE_IMG_B64,
        now=datetime.utcnow(),
        schema_json=json.dumps(schema),
    )

@app.route("/api/publications")
def publications_api():
    return jsonify({"publications": PUBLICATIONS, "additional": PUBLICATIONS_ADDITIONAL})

@app.route("/contact", methods=["POST"])
def contact():
    # Accept both form‑encoded and JSON payloads
    data = request.form or request.get_json(force=True, silent=True) or {}
    # Honeypot field (hidden) – if filled, treat as spam
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
        msg.body = f"""From: {name} <{email}>
Subject: {subject}

{message}
--
Sent via vk‑site contact form
"""
        mail.send(msg)
        return jsonify({"success": True})
    except Exception as exc:
        logging.error(f"Mail error: {exc}")
        return jsonify({"success": False, "error": "Email failed"}), 500

@app.route("/cv")
def serve_cv():
    # Serve CV PDF if present
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

