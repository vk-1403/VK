import os
import logging
from flask import Flask, render_template_string, request, jsonify, send_from_directory
from flask_mail import Mail, Message
from my_html_assets import CSS_STYLES, JAVASCRIPT, HTML_TEMPLATE, get_profile_image_base64

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vidyapatikumar.me@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('GMAIL_APP_PASSWORD')  # Secure env var
app.config['MAIL_DEFAULT_SENDER'] = 'vidyapatikumar.me@gmail.com'

mail = Mail(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)


# Theme-wise publications
def get_publications():
    return {
        "AI & Machine Learning": [
            {
                "title": "Wearable sensor‑based intent recognition for adaptive control of intelligent ankle‑foot prosthetics",
                "journal": "Measurement: Sensors, Elsevier (2025)",
                "year": "2025",
                "link": "https://doi.org/10.xxxxx/measurement"
            },
            {
                "title": "Vision Transformer-based pose estimation for automated gait analysis in prosthetic design",
                "journal": "IEEE ICCCT (2024)",
                "year": "2024",
                "link": "https://doi.org/10.xxxxx/ieee"
            }
        ],
        "Biomechatronics": [
            {
                "title": "Biomechanical material selection for ankle‑foot prosthetics: An ensemble MCDM‑FEA framework",
                "journal": "Springer IJIDeM (2025)",
                "year": "2025",
                "link": "https://doi.org/10.xxxxx/springer"
            }
        ],
        "IoT & Embedded Systems": [
            {
                "title": "ESP32-based prosthetic control system with real-time gait phase recognition",
                "journal": "ACM Transactions (2023)",
                "year": "2023",
                "link": "https://doi.org/10.xxxxx/acm"
            }
        ]
    }


@app.route('/')
def index():
    try:
        profile_image = get_profile_image_base64()
        publications = get_publications()
        return render_template_string(
            HTML_TEMPLATE,
            title="Vidyapati Kumar - PhD Candidate | AI & Biomechatronics",
            css_styles=CSS_STYLES,
            javascript=JAVASCRIPT,
            profile_image=profile_image,
            publications=publications
        )
    except Exception as e:
        logging.error(f"Error rendering homepage: {e}")
        return "Internal Server Error", 500


@app.route('/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

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

        logging.info(f"Contact form submitted successfully by {name}")
        return jsonify({'success': True, 'message': 'Thank you for your message! I will get back to you soon.'})
    except Exception as e:
        logging.error(f"Error processing contact form: {e}")
        return jsonify({'success': False, 'error': 'Failed to send message'}), 500


@app.route('/cv')
def download_cv():
    """Serve the CV PDF file"""
    try:
        return send_from_directory('static', 'CV_VK_git.pdf', as_attachment=True)
    except Exception as e:
        logging.error(f"CV download error: {e}")
        return "CV not found", 404


@app.errorhandler(404)
def not_found(error):
    return "Page not found", 404


@app.errorhandler(500)
def server_error(error):
    logging.error(f"Server error: {error}")
    return "Internal server error", 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
