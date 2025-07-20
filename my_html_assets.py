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
# 🌟 Profile Summary
# -------------------------------
PROFILE_SUMMARY = """
Ph.D. candidate in Mechanical Engineering at IIT Kharagpur, specializing in AI-driven biomechatronic systems, advanced manufacturing, and multi-objective optimization. My research integrates machine learning, sensor fusion, and embedded systems for intelligent prosthetics, wearable health technologies, and process optimization. I have published peer-reviewed journal articles, contributed to edited books, and hold a patent and software copyright. With interdisciplinary expertise spanning biomedical engineering, robotics, and smart manufacturing, I aim to contribute to cutting-edge research in AI-enabled systems and real-world healthcare innovations through a postdoctoral position.
"""

# -------------------------------
# 🎓 Education
# -------------------------------
EDUCATION = [
    {"year": "Dec 2025 (Expected)", "degree": "Ph.D. Mechanical Engineering", "institute": "IIT Kharagpur, India", "cgpa": "8.5 / 10"},
    {"year": "2018", "degree": "M.E. Production Engineering", "institute": "Jadavpur University, India", "cgpa": "8.38 / 10"},
    {"year": "2016", "degree": "B.Tech Mechanical Engineering", "institute": "MAKAUT, India", "cgpa": "9.19 / 10"}
]

# -------------------------------
# 💼 Experience
# -------------------------------
EXPERIENCE = [
    {
        "title": "Senior Research Fellow – AI-Enhanced Powered Ankle-Foot Prosthetic System",
        "period": "Jul 2021 – Present",
        "organization": "IIT Kharagpur",
        "location": "Kharagpur, India",
        "details": [
            "Designed microcontroller-based sensor fusion platform (ESP32, Raspberry Pi).",
            "Developed multimodal control strategy for powered ankle-foot prosthesis.",
            "Implemented video-based gait analysis using Vision Transformers & YOLOv8.",
            "Validated system performance through extensive sensor-based trials."
        ]
    },
    {
        "title": "Project Mentor – TIH Foundation for IoT and IoE (IIT Bombay)",
        "period": "Feb 2024 – Present",
        "organization": "IIT Bombay & DST, Govt. of India",
        "location": "Kharagpur, India",
        "details": [
            "Leading IoT-enabled prosthetic system design for Chanakya Fellowship Project.",
            "Mentoring teams and coordinating hardware, firmware, and cloud integration."
        ]
    },
    {
        "title": "Teaching Assistant – NPTEL Courses",
        "period": "Jan 2021 – Present",
        "organization": "IIT Kharagpur",
        "location": "Kharagpur, India",
        "details": [
            "Assisted in Robotics, Fuzzy Logic, and Optimization Tools courses."
        ]
    }
]

# -------------------------------
# 📚 Publications (Sample)
# -------------------------------
PUBLICATIONS = {
    "AI & Machine Learning": [
        {"title": "Wearable sensor‑based intent recognition for adaptive control of intelligent ankle‑foot prosthetics", "journal": "Measurement: Sensors, Elsevier", "year": "2025", "link": "https://doi.org/10.xxxxx/measurement"},
        {"title": "Vision Transformer-based pose estimation for gait analysis", "journal": "IEEE ICCCT", "year": "2024", "link": "https://doi.org/10.xxxxx/ieee"}
    ],
    "Biomechatronics": [
        {"title": "Biomechanical material selection for ankle‑foot prosthetics: An ensemble MCDM‑FEA framework", "journal": "Springer IJIDeM", "year": "2025", "link": "https://doi.org/10.xxxxx/springer"}
    ],
    "IoT & Embedded Systems": [
        {"title": "ESP32-based prosthetic control system with real-time gait phase recognition", "journal": "ACM Transactions", "year": "2023", "link": "https://doi.org/10.xxxxx/acm"}
    ]
}

# -------------------------------
# 🏆 Awards
# -------------------------------
AWARDS = [
    "RAAIBA-2022 Workshop (NIT Rourkela, SERB DST)",
    "MHRD Institute Assistantship (PhD, IIT Kharagpur)",
    "GATE Fellowship (M.E. Jadavpur University)"
]

# -------------------------------
# ⚙️ Technical Skills
# -------------------------------
SKILLS = [
    "Python, C++, MATLAB, Arduino, ESP32, Raspberry Pi",
    "AI/ML: scikit-learn, PyTorch, TensorFlow, SHAP, LIME",
    "Computer Vision: OpenCV, YOLOv8, Vision Transformers",
    "Finite Element Analysis (FEA): COMSOL, ANSYS",
    "Sensor Fusion: EMG, IMU, FSR, Real-Time Control"
]
