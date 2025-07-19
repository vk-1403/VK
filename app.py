import os
import logging
from flask import Flask, render_template_string, request, jsonify
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

@app.route('/')
def index():
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

        return jsonify({'success': True, 'message': 'Thank you for your message! I will get back to you soon.'})
    except Exception as e:
        logging.error(f"Error processing contact form: {e}")
        return jsonify({'success': False, 'error': 'Failed to send message'}), 500

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
